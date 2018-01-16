#include <cstdlib>
#include <cstdio>
#include <cstdlib>
#include <cstdio>
#include <cassert>
#include <cstring>
#include <string>
#include <utility>
#include <map>
#include <cxxabi.h>
using std::map;
using std::pair;
using std::string;

#define version 17

typedef unsigned char uint1;
typedef unsigned short uint2;
typedef unsigned int uint4;
typedef unsigned long long uint8;

static const uint2 maxstacksize = 4096;
static const uint1 hsizelg2 = 12;
static const uint2 hsize = 1 << hsizelg2;
static const uint1 psizelg2 = 16;
static const uint4 psize = 1 << psizelg2;
static const uint2 psizem1 = psize - 1;

#define Q(x) #x
#define QUOTE(x) Q(x)


static uint2 hbuf[hsize];
static uint2 pbuf[psize];



void readFile(const char name[], uint8& length,int flg)
{
  //printf("INSIDE READFILE NAME: %s\n",name);
  FILE* f = fopen(name, "rb");  assert(f != NULL);
  fseek(f, 0, SEEK_END);
  
  uint8 csize = ftell(f);  assert(csize > 0);
  //printf("csize %hu\n",csize);
  uint1* cbuf = new uint1[csize];
  fseek(f, 0, SEEK_SET);
  length = fread(cbuf, sizeof(uint1), csize, f);  assert(length == csize);
  fclose(f);

  uint8 bytes = 0;
  uint8 cpos = 0;
  while (cpos < csize) {
    uint1 bitpat = cbuf[cpos++];
    for (uint1 b = 0; b < 8; b++) {
      if (bitpat & (1 << b)) {
	cpos++;
      }
    }
    if (cpos == csize - 1) {
      bytes += cbuf[cpos++] * 2;
    } else {
      bytes += 8;
    }
  }
  uint1* bbuf = new uint1[bytes + 6];
  uint8 bpos = 0;
  cpos = 0;
  while (cpos < csize - 1) {
    uint1 bitpat = cbuf[cpos++];
    for (uint1 b = 0; b < 8; b++) {
      if (bitpat & (1 << b)) {
	bbuf[bpos++] = cbuf[cpos++];
      } else {
	bbuf[bpos++] = 0;
      }
    }
  }
  delete [] cbuf;

  uint2* dbuf = (uint2*)malloc(8192 * sizeof(uint2));  assert(dbuf != NULL);
  uint8 dcap = 8192;
  uint8 dpos = 0;

  bool iscount;
  uint2 ppos = 0;
  uint2 lpos = 0;
  uint2 hash = 0;
  uint8 tpos = 0;

  memset(hbuf, 0, hsize * sizeof(hbuf[0]));
  memset(pbuf, 0, psize * sizeof(pbuf[0]));

  uint8 words = bytes / 2;
  uint2* tbuf = (uint2*)bbuf;
  while (tpos < words) {
    lpos = hbuf[hash];
    iscount = (pbuf[(lpos - 3) & psizem1] == pbuf[(ppos - 3) & psizem1]) &&
      (pbuf[(lpos - 2) & psizem1] == pbuf[(ppos - 2) & psizem1]) &&
      (pbuf[(lpos - 1) & psizem1] == pbuf[(ppos - 1) & psizem1]);
    if (iscount) {
      uint2 count = tbuf[tpos++];
      for (uint2 i = 0; i < count; i++) {
	uint2 value = pbuf[lpos];
	if (dpos == dcap) {
	  dcap *= 2;
	  dbuf = (uint2*)realloc(dbuf, dcap * sizeof(uint2));  assert(dbuf != NULL);
	}
	dbuf[dpos++] = value;
	lpos = (lpos + 1) & psizem1;
	hbuf[hash] = ppos;
	hash = ((hash << (hsizelg2 / 3)) ^ value) % hsize;
	pbuf[ppos] = value;
	ppos = (ppos + 1) & psizem1;
      }
    }

    if (tpos < words) {
      uint2 value = tbuf[tpos++];
      if (dpos == dcap) {
	dcap *= 2;
	dbuf = (uint2*)realloc(dbuf, dcap * sizeof(uint2));  assert(dbuf != NULL);
      }
      dbuf[dpos++] = value;
      hbuf[hash] = ppos;
      hash = ((hash << (hsizelg2 / 3)) ^ value) % hsize;
      pbuf[ppos] = value;
      ppos = (ppos + 1) & psizem1;
    }
  }

  length = dpos;
  if (csize != 0 && flg == 1) {
    //    printf("-uncompressed(uint2):\t\t %d\n", 2 * dpos);
    printf("com: %d\n", csize);
    // printf("-compression ratio(uint2):\t\t %hu\n", (2.0 * dpos) / csize);    
    printf("unc: %d\n", 2 * dpos);
    //printf("-compressed(float):\t\t %.2f\n", csize);    
    printf("ratio: %.2f\n", (2.0 * dpos) / csize);
  }
  delete [] bbuf;
  //return dbuf;
}

int main(int argc, char* argv[])
{
  if (argc != 2) {
    printf("usage: %s tracefile\n", argv[0]);
    return -1;
  }

  //string* info = readInfo(argv[1]);


  uint8 length;


  /*  uint2* data ;
  data = readFile(argv[1], length,1);
  //printf("%s contains %lld events\n", argv[1], length);
  free(data);
  */


  readFile(argv[1], length,1);
  
  
  
  return 0;
}


