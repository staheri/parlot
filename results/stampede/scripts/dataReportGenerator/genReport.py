# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: genReport.py
# Description: extract the runtime and read the size of generated traces for each experiment, write the data in CSV format.


import sys,subprocess
import glob
import os

replication = 3
corePerNode = 16

def genCSV(dict,fname):
	s = "Tool,Compiler,Benchmark,Application,#nodes,#processes,avg Runtime(s)-real,avg Runtime(s)-user, avg Size(KB)\n"
	flags = {}
	for key,val in sorted(dict.items()):
		key_s=key.split(".")
		if key_s[0]+"."+key_s[1]+"."+key_s[2]+"."+key_s[4]+"."+key_s[3] in flags.keys():
			realT = realT + val[0]
			userT = userT + val[1]
			sizeT = sizeT + val[3]
		else:
			tool = key_s[0]
			bm = key_s[1]
			comp = key_s[2]
			app = key_s[4]
			nodes = int(key_s[3])
			procs = corePerNode * nodes
			realT = val[0]
			userT = val[1]
			sizeT = val[3]
			flags[tool+"."+bm+"."+comp+"."+app+"."+`nodes`] = 1
		print "KEYS " + key_s[5]
		if int(key_s[5]) == replication:
			s=s+tool+","+comp+","+bm+","+app+","+`nodes`+","+`procs`+","+`realT/replication`+","+`userT/replication`+","+`(sizeT/replication)/1024.0`+"\n"
	fo = open(fname+"-avg.csv","w")
	fo.write(s)
	fo.close()
	
	
def writeDataToFile(dict,fname):
	s = "Flag,Tool,Compiler,Benchmark,Application,#nodes,#processes,Rep ID,Runtime(s)-real,Runtime(s)-user,Runtime(s)-sys,Size(KB)\n"
	s = ""
	for key,val in sorted(dict.items()):
		print "inside Write"
		print key
		for tt in dict[key]:
			print "\t" + `tt`
		key_s=key.split(".")
		
		flag = key_s[0]
		tool = key_s[1]
		bm = key_s[2]
		comp = key_s[4]
		app = key_s[3]
		nodes = int(key_s[5])
		procs = 16 * nodes
		realT = val[0]
		userT = val[1]
		sysT = val[2]
		sizeT = float(val[3])
		s=s+flag+","+tool+","+comp+","+bm+","+app+","+`nodes`+","+`procs`+","+key_s[7]+","+`realT`+","+`userT`+","+`sysT`+","+`sizeT/1024.0`+"\n"


#		tool = key_s[0]
#		bm = key_s[1]
#		comp = key_s[3]
#		app = key_s[2]
#		nodes = int(key_s[4])
#		procs = 16 * nodes
#		realT = val[0]
#		userT = val[1]
#		sysT = val[2]
#		sizeT = float(val[3])
#		s=s+tool+","+comp+","+bm+","+app+","+`nodes`+","+`procs`+","+key_s[6]+","+`realT`+","+`userT`+","+`sysT`+","+`sizeT/1024.0`+"\n"
	fi = open(fname+".csv","w")
	fi.write(s)
	fi.close()

def getSizeOfTraces(path):
	dic = {}
	print "PATH: " + path
	for folder in sorted(glob.glob(path+"/*/")):
		print folder
		tot = 0
		for dirpath,dirnames,filenames in os.walk(folder):
			for f in filenames:
				fp = os.path.join(dirpath,f)
				tot = tot + os.path.getsize(fp)
		#print "Size of " + folder + " is " + `tot` + "\n"
        	dic[folder.split("/")[-2]] = tot
	return dic
def readSizeFile(f):
	fi = open(f,"r")
	dic = {}
	lines = fi.readlines()
	for line in lines:
		l = line.split(",")
		dic[l[0]]=float(l[1].strip())
	return dic
def readRuntimes(file):
	fi = open(file,"r")
	dic = {}
	flist = fi.readlines()
	for i in range (0,(len(flist)/5)):
		l = []
		print "file"
		print file
		job = flist[i*5].split(":")[-1].strip()
		print "job"
		print job
		real_t =  flist[i*5+2].split("real")[-1].strip()
		real = (float(real_t.split("m")[0]) * 60 ) + float(real_t.split("m")[-1].split("s")[0])
		l.append(real)
		user_t =  flist[i*5+3].split("user")[-1].strip()
		user = (float(user_t.split("m")[0]) * 60 ) + float(user_t.split("m")[-1].split("s")[0])
		l.append(user)
		sys_t =  flist[i*5+4].split("sys")[-1].strip()
		syst = (float(sys_t.split("m")[0]) * 60 ) + float(sys_t.split("m")[-1].split("s")[0])
		l.append(syst)
		dic[job]=l
	return dic


if len(sys.argv) != 4:
	print len(sys.argv)
	print "USAGE:\n\t " +sys.argv[0]+" path-to-runtimes path-to-traces experimentName"
	sys.exit(-1)

pathToRuntimes = sys.argv[1]
pathToTraces = sys.argv[2]
exName = sys.argv[3]

dall={}
for f in glob.glob(pathToRuntimes):
	dall.update(readRuntimes(f))
dsize = getSizeOfTraces(pathToTraces)
fsize = open(exName+"_size.csv","w")
sz = ""
for key,val in sorted(dsize.items()):
	sz = sz + key + "," + `dsize[key]` + "\n"
fsize.write(sz)
fsize.close()

dsize=readSizeFile(exName+"_size.csv")

print "size : " + `len(dsize.items())`
print "time : " + `len(dall.items())`

#if len(dsize.items()) >= len(dall.items()):
for key,val in sorted(dsize.items()):
	if key in list(dall):
		print "KIR"
		t = dall[key]
		t.append(val)
		dall[key]=t
		print "\t" + key
		#print "\t\t" + `len(dall[key])`
		print t
	else:
		print "kir 222"
		dall[key]=[0.0,0.0,0.0,val]
	
#else:
print "############################################################################################################"
for key,val in sorted(dall.items()):
	if key in list(dsize):
		t = []
		for item in val:
			t.append(item)	
		t.append(dsize[key])
		dall[key]=t
	else:
		t = []
		for item in val:
			t.append(item)
		t.append(0.0)
		dall[key]=t

#for key,val in sorted(dall.items()):
#	print key
#	for item in dall[key]:
#		print "\t" + `item`

writeDataToFile(dall,exName)
#genCSV(dall,exName)
