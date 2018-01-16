# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: genIData.py
# Description: extract the runtime and read the size of generated traces for each experiment


import sys,subprocess
import glob
import os
import math
import random

runPath = "/pylon2/cc560up/staheri/workspace"
outPath = "/home/staheri/pintool/tracing/experiments/psc/idata"

def appoutCrashes(run):
	l = []
	path = runPath + "/" + run 
	for f in sorted(glob.glob(path+"/*/app_out/*.err.txt")):
		print f
		#print "Tool"
		tool = f.rpartition("/")[2].split(".")[1]
		#print tool
		#print "Node"
		node = f.rpartition("/")[2].split(".")[-4]
		#print node
		if not (tool == "callgrind" or node == "64") :
			if os.stat(f).st_size != 0:
				print "\t"+f
				l.append(f.rpartition("/")[2].rpartition(".")[0].rpartition(".")[0])
	#for item in l:
		#print item
	return l
	
	
def outputCrashes(run):
	l = []
	path = runPath + "/" + run 
	for f in sorted(glob.glob(path+"/*/*.output")):
		fi = open(f,"r")
		lines = fi.readlines()
		for line in lines:
			if line.startswith("job"):
				job = line.split(":")[-1].strip()
				#print f
				if lines.index(line)+4 <= len(lines) - 1:
					if not lines[lines.index(line)+2].startswith("real") or not lines[lines.index(line)+3].startswith("user") or not lines[lines.index(line)+4].startswith("sys"):
						l.append(job)
						#print f
						break
				else:
					l.append(job)
					#print f
					break
	return l

def findCrashes(run):
	ret = set()
	s = "Output Crashes\n"
	#for item in outputCrashes(run):
	#	s = s + item + "\n"
	#	ret.add(item)
	#print s
	s = "App Out Crashes\n"
	for item in outputCrashes(run):
	#	s = s + item + "\n"
	#	ret.add(item)
		print item
	
	#fout = open(outPath+"/"+run+"-crashed.csv" ,"w")
	#fout.write(s)
	#fout.close()
	return ret


def readRuntimes(run):
	print "Reading runtimes from .output files"
	path = runPath + "/" + run 
	crashed= outputCrashes(run)
	dic = {}
	s = ""
	for f in sorted(glob.glob(path+"/*/*.output")):
		fi = open(f,"r")
		print "From file " + f + ":"
		lines = fi.readlines()
		for line in lines:
			if line.startswith("job"):
				job = line.split(":")[-1].strip()
				if job not in crashed:
					real_t = lines[lines.index(line)+2].split("real")[-1].strip()
					real = (float(real_t.split("m")[0]) * 60 ) + float(real_t.split("m")[-1].split("s")[0])
					print "\t"+job + " : " + `real`
					dic[job] = real
				else:
					dic[job] = 0.0
	for key,val in sorted(dic.items()):
		s = s + key + "," + `val` + "\n"
	fout = open(outPath+"/"+run+"-runtime.csv","w")
	fout.write(s)
	fout.close()
	return dic


# Find size of traces of each run
def getSizeOfTraces(run):
	print "Getting size of traces"
	dic = {}
	path = runPath + "/" + run
	s = ""
	for folder in sorted(glob.glob(path+"/*/traces/*/")):
		tot = 0
		for dirpath,dirnames,filenames in os.walk(folder):
			for f in filenames:
				fp = os.path.join(dirpath,f)
				tot = tot + os.path.getsize(fp)
			print "Size of " + folder + " is " + `tot` + "\n"
        	dic[folder.split("/")[-2]] = tot
	for key,val in sorted(dic.items()):
		s = s + key + "," + `val` + "\n"
	fout = open(outPath+"/"+run+"-size.csv","w")
	fout.write(s)
	fout.close()
	return dic
	
def decompress(run):
	print "Measuring Decompression Ratio:"
	crashed=findCrashes(run)
	ret = {}
	path = runPath + "/" + run
	#print path
	#print glob.glob(path+"/*")
	for tool in ["pinMain","pinAll"]:
		for folder in glob.glob(path+"/"+tool+"/traces/*"):
			print folder
			key = folder.rpartition("/")[2]
			if key not in crashed:
				sample=0
				lof = sorted (glob.glob(folder+"/*.info"))
				#print lof
				if key.split(".")[7] == "1":
					sample = 4
				if key.split(".")[7] == "4":
					sample = 12
				if key.split(".")[7] == "16":
					sample = 32
				if key.split(".")[7] == "64":
					sample = 64
				#print "SAMPLE"
				#print len(lof)
				#print sample
				randLof = random.sample(lof,sample)
				for f in randLof:
					trace_common = f.rpartition(".")[0]
					#print "\t"+f
					for ft in sorted(glob.glob(trace_common+".0")):
						#print "\t\t"+ft
						exe="./tr20"
						trace = " "+ft+" "
						command = exe+trace
						print command
						print "before"
						process = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
						s, err = process.communicate()
						if not s.split("\n")[0].startswith("com") or not s.split("\n")[1].startswith("unc") or not s.split("\n")[2].startswith("ratio"):
							print "error"
							continue
						else:
							ret[ft] = s.split("\n")[2].split(":")[-1]
						print "after"
	s = ""
	for key,val in sorted(ret.items()):
		s = s + key + "," + val + "\n"
	fout = open(outPath+"/"+run+"-cratio.csv","w")
	fout.write(s)
	fout.close()
	return ret

if len(sys.argv) != 2:
	print "USAGE:\n\t " +sys.argv[0]+" run"
	sys.exit(-1)

run=sys.argv[1]

getSizeOfTraces(run)
#findCrashes(run)
readRuntimes(run)
#decompress(run)

