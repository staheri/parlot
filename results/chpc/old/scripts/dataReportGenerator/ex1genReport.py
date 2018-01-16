import sys,subprocess
import os
import glob

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
		if int(key_s[5]) == replication:		
			s=s+tool+","+comp+","+bm+","+app+","+`nodes`+","+`procs`+","+`realT/replication`+","+`userT/replication`+","+`(sizeT/replication)/1024.0`+"\n"
	fo = open(fname+"-avg.csv","w")
	fo.write(s)
	fo.close()

def writeDataToFile(dict,fname):
	s = "Tool,Compiler,Benchmark,Application,#nodes,#processes,Rep ID,Runtime(s)-real,Runtime(s)-user,Runtime(s)-sys,Size(KB)\n"
	for key,val in sorted(dict.items()):
		key_s=key.split(".")
		tool = key_s[0]
		bm = key_s[1]
		comp = key_s[2]
		app = key_s[4]
		nodes = int(key_s[3])
		procs = 16 * nodes
		realT = val[0]
		userT = val[1]
		sysT = val[2]
		sizeT = val[3]
		s=s+tool+","+comp+","+bm+","+app+","+`nodes`+","+`procs`+","+key_s[5]+","+`realT`+","+`userT`+","+`sysT`+","+`sizeT/1024.0`+"\n"
	fi = open(fname+".csv","w")
	fi.write(s)
	fi.close()

def getSizeOfTraces(path):
        dic1={}
        for folder in sorted(glob.glob(path+"/*/")):
                tot = 0
                for dirpath,dirnames,filenames in os.walk(folder):
                        for f in filenames:
                                fp = os.path.join(dirpath,f)
                                tot = tot + os.path.getsize(fp)
                dic1[folder.split("/")[-2]] = tot
        return dic1


dsize=getSizeOfTraces("/work/02309/staheri/experiments/ex1.classifiedByTopo/traces")
dic = {}
for f in sorted(glob.glob("/work/02309/staheri/jobSub/ex1classifiedByTopo/*.84*")):
        if "orig.amg.tau" in f :
                continue
        t = f.split(".")
        l1 = []
        #print t
        ss = ""
        for i in range(0,len(t)-1):
                ss = ss + t[i]+"."
        s = ss + "slurm"
        #print s
        fi = open(s,"r")
        for line in fi.readlines():
                if ".txt" in line:
                        l1.append(ss.split("/")[-1]+line.split("$JOB.")[-1].split(".txt")[0].strip())
        fi = open(f,"r")
        flist = fi.readlines()
        for i in range (0,(len(flist)/4)):
                l = []
                job = l1[i]
                real_t =  flist[i*4+1].split("real")[-1].strip()
                real = (float(real_t.split("m")[0]) * 60 ) + float(real_t.split("m")[-1].split("s")[0])
                l.append(real)
                user_t =  flist[i*4+2].split("user")[-1].strip()
                user = (float(user_t.split("m")[0]) * 60 ) + float(user_t.split("m")[-1].split("s")[0])
                l.append(user)
                sys_t =  flist[i*4+3].split("sys")[-1].strip()
                syst = (float(sys_t.split("m")[0]) * 60 ) + float(sys_t.split("m")[-1].split("s")[0])
                l.append(syst)
                dic[job]=l
i = 0
print "size : " + `len(dsize.items())`
print "time : " + `len(dic.items())`

for key,val in sorted(dsize.items()):
	if key in list(dic):
		print "key is in"
		t = dic[key]
		t.append(val)
		dic[key]=t
		print key + ":" + `dic[key]`
	else:
		print "NO KEY !"
		dic[key]=[0.0,0.0,0.0,val]
		print key + ":" + `dic[key]`
writeDataToFile(dic,"ex1")
genCSV(dic,"ex1")

  #      i = i + 1
#print "***************"
#for key,val in sorted(dic.items()):
#        print key
#	
 #       i = i - 1
#print i
#dsize.update(dic)
#for key,val in sorted(dsize.items()):
#	print key
#	print val
