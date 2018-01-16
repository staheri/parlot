/*
Pin tool for generating compressed call traces of multithreaded programs.

This tool captures all functions, including functions from libraries.  It
corrects the trace by inserting missing returns and uses an incremental
implementation of the "LZa3 | ZE" compressiong algorithm to compress the
trace information on-the-fly before emitting it.

Copyright (c) 2016, Texas State University. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted for academic, research, experimental, or personal use provided
that the following conditions are met:

   * Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
   * Neither the name of Texas State University nor the names of its
     contributors may be used to endorse or promote products derived from this
     software without specific prior written permission.

For all other uses, please contact the Office for Commercialization and Industry
Relations at Texas State University <http://www.txstate.edu/ocir/>.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Authors: Sindhu Devale and Martin Burtscher
*/


#include <cstdlib>
#include <cstdio>
#include <string.h>
#include <unistd.h>
#include "pin.H"
#include "portability.H"

#define version 17

typedef unsigned char uint1;
typedef unsigned short uint2;
typedef unsigned int uint4;
typedef unsigned long uint8;

static const uint1 maxthreads = 64;
static const uint2 maxstacksize = 4096;
static const uint1 hsizelg2 = 12;
static const uint2 hsize = 1 << hsizelg2;
static const uint1 psizelg2 = 16;
static const uint4 psize = 1 << psizelg2;
static const uint2 psizem1 = psize - 1;
static const uint2 csize = 256;  //small fwrite increments

static struct ThreadData {
  bool iscount;  // is most recent value in tbuf a count
  uint2 ppos;  // current position in pbuf
  uint2 lpos;  // last similar position in pbuf
  uint2 hash;  // hash of last few values
  uint1 tpos;  // current position in tbuf
  uint4 cpos;  // current position in cbuf
  uint2 tos;  // top of stack
  FILE* file;
  uint2 tbuf[4];  // temporary buffer for intermediate values
  uint1 cbuf[csize];  // compressed byte buffer
  uint2 hbuf[hsize];  // hash table of last similar position
  uint2 pbuf[psize];  // cyclic pattern buffer
  uint2 stack[maxstacksize];  // stack holding function IDs
  uint8 sp[maxstacksize];  // SP addresses
} td[maxthreads];

static string fnameprefix;
static FILE* info = NULL;

#define Q(x) #x
#define QUOTE(x) Q(x)
#define errorif(cond, msg) if (cond) {fprintf(stderr, "ERROR: %s\n", msg); exit(-1);}

static void write(struct ThreadData* const d, const uint2 value)
{
  if (d->tpos == 4) {
    d->tpos = 0;

    uint1* buf = (uint1*)(d->tbuf);
    const uint2 pos = d->cpos;
    d->cpos++;
    uint1 bitpat = 0;
    for (uint1 b = 0; b < 8; b++) {
      const uint1 val = buf[b];
      if (val != 0) {
        bitpat |= 1 << b;
        d->cbuf[d->cpos] = val;
        d->cpos++;
      }
    }
    d->cbuf[pos] = bitpat;

    if (d->cpos > csize - 9) {
      fwrite(d->cbuf, 1, d->cpos, d->file);
      d->cpos = 0;
    }
  }

  d->tbuf[d->tpos] = value;
  d->tpos++;
}

static void output(const THREADID tid, const uint2 value)
{
  struct ThreadData* d = &td[tid];

  if ((d->iscount) && (d->pbuf[d->lpos] == value) && (d->tbuf[d->tpos - 1] < (uint2)65535)) {
    d->lpos = (d->lpos + 1) & psizem1;
    d->tbuf[d->tpos - 1]++;
  } else {
    if (d->iscount) {
      write(d, value);
      d->iscount = false;
    } else {
      d->lpos = d->hbuf[d->hash];
      d->iscount = (d->pbuf[(d->lpos - 3) & psizem1] == d->pbuf[(d->ppos - 3) & psizem1]) &&
                   (d->pbuf[(d->lpos - 2) & psizem1] == d->pbuf[(d->ppos - 2) & psizem1]) &&
                   (d->pbuf[(d->lpos - 1) & psizem1] == d->pbuf[(d->ppos - 1) & psizem1]);
      if (d->iscount) {
        if (d->pbuf[d->lpos] == value) {
          d->lpos = (d->lpos + 1) & psizem1;
          write(d, 1);
        } else {
          write(d, 0);
          write(d, value);
          d->iscount = false;
        }
      } else {
        write(d, value);
      }
    }
  }

  d->hbuf[d->hash] = d->ppos;
  d->hash = ((d->hash << (hsizelg2 / 3)) ^ value) % hsize;
  d->pbuf[d->ppos] = value;
  d->ppos = (d->ppos + 1) & psizem1;
}

VOID PIN_FAST_ANALYSIS_CALL enter(THREADID tid, UINT32 x, ADDRINT spval)
{
  uint2 ts = td[tid].tos;
  while ((ts > 1) && (td[tid].sp[ts - 1] <= spval)) {
    ts--;
    output(tid, 0);
  }

  td[tid].sp[ts] = spval;
  td[tid].stack[ts++] = x;
  errorif(ts >= maxstacksize, "stack overflow");
  output(tid, x);
  td[tid].tos = ts;
}

VOID PIN_FAST_ANALYSIS_CALL leave(THREADID tid, UINT32 x, ADDRINT spval)
{
  uint2 ts = td[tid].tos;
  while ((ts > 1) && (td[tid].sp[ts - 1] <= spval) && (td[tid].stack[ts - 1] != x)) {
    ts--;
    output(tid, 0);
  }
  if ((ts > 1) && (td[tid].sp[ts - 1] <= spval) && (td[tid].stack[ts - 1] == x)) {
    ts--;
    output(tid, 0);
  }
  td[tid].tos = ts;
}

VOID Routine(RTN rtn, VOID* v)
{
  static UINT32 id = 1;
  static string previmg = " ";

  errorif(id >= 65535, "too many functions");
  const char* rtnname = RTN_Name(rtn).c_str();
  const string img = IMG_Name(SEC_Img(RTN_Sec(rtn)));
  if (previmg == img) {
    fprintf(info, "%s\n", rtnname);
  } else {
    previmg = img;
    const char* imgname = img.c_str();
    fprintf(info, "+\n%s\n%s\n", imgname, rtnname);
  }

  RTN_Open(rtn);
  RTN_InsertCall(rtn, IPOINT_BEFORE, (AFUNPTR)enter, IARG_FAST_ANALYSIS_CALL, IARG_THREAD_ID, IARG_UINT32, id, IARG_REG_VALUE, REG_STACK_PTR, IARG_END);
  RTN_InsertCall(rtn, IPOINT_AFTER, (AFUNPTR)leave, IARG_FAST_ANALYSIS_CALL, IARG_THREAD_ID, IARG_UINT32, id, IARG_REG_VALUE, REG_STACK_PTR, IARG_END);
  RTN_Close(rtn);

  id++;
}

VOID ThreadStart(THREADID tid, CONTEXT* ctxt, INT32 flags, VOID* v)
{
  errorif(tid >= maxthreads, "too many threads");
  string filename = fnameprefix + decstr(tid);

  td[tid].iscount = false;
  td[tid].ppos = 0;
  td[tid].lpos = 0;
  td[tid].hash = 0;
  td[tid].tpos = 0;
  td[tid].cpos = 0;
  td[tid].tos = 1;
  td[tid].file = fopen(filename.c_str(), "wb");
  errorif(td[tid].file == NULL, "could not open output file");
  td[tid].stack[0] = 0;
  td[tid].sp[0] = 0;
  memset(td[tid].hbuf, 0, hsize * sizeof(td[tid].hbuf[0]));
  memset(td[tid].pbuf, 0, psize * sizeof(td[tid].pbuf[0]));
}

VOID ThreadFini(THREADID tid, const CONTEXT* ctxt, INT32 code, VOID* v)
{
  struct ThreadData* d = &td[tid];

  if (d->tpos > 0) {
    uint1* buf = (uint1*)(d->tbuf);
    const uint2 pos = d->cpos;
    d->cpos++;
    uint1 bitpat = 0;
    for (uint1 b = 0; b < d->tpos * 2; b++) {
      const uint1 val = buf[b];
      if (val != 0) {
        bitpat |= 1 << b;
        d->cbuf[d->cpos] = val;
        d->cpos++;
      }
    }
    d->cbuf[pos] = bitpat;
  }
  d->cbuf[d->cpos] = d->tpos;
  d->cpos++;

  fwrite(d->cbuf, 1, d->cpos, d->file);
  fclose(d->file);
  d->file = NULL;
}

int main(int argc, char* argv[])
{
  printf("PinTracer %s (%s)\n", QUOTE(version), __FILE__);
  printf("Copyright (c) 2016 Texas State University\n\n");

  char hostname[32];
  gethostname(hostname, 31);
  int i = 0;
  while ((i < 31) && (hostname[i] != '.')) i++;
  hostname[i] = 0;
  fnameprefix = "/tmp/Hdbg.";
  fnameprefix += QUOTE(version);
  fnameprefix += ".";
  fnameprefix += "stampede";
  fnameprefix += "." + decstr(getpid_portable()) + ".";

  string filename = fnameprefix + "info";
  info = fopen(filename.c_str(), "wt");
  errorif(info == NULL, "could not open info file");

  PIN_InitSymbols();
  errorif(PIN_Init(argc, argv), "pin failed to initialize");

  PIN_AddThreadStartFunction(ThreadStart, 0);
  PIN_AddThreadFiniFunction(ThreadFini, 0);
  RTN_AddInstrumentFunction(Routine, 0);

  PIN_StartProgram();
  return 0;
}
