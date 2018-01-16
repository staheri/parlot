# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: appOutSizeChecker.py
# Description: Check the size of application outputs to see if they failed or not


import sys,subprocess
import glob
import os



replication = 5
corePerNode = 16


def appOutSizeChecker(path):
	l = []
	print "appout"
	for f in glob.glob(path+"//app_out/*.err.txt"):
		if os.stat(f).st_size != 0:
			print f
			l.append(f.rpartition("/")[2])
	return l

def outputChecker(path):
	l = []
	print "output"
	for f in sorted(glob.glob(path+"/*.output")):
		flag = True
		fi = open(f,"r")
		lines = fi.readlines()
                for item in lines:
                        if "error" in item or "TIME" in item or "cannot" in item:
                                l.append(f.rpartition("/")[2])
                                print f
                                break
		for i in range (0,(len(lines)/5)):
			if "job:" not in lines[i*5] or "real" not in lines[i*5+2] or "user" not in lines[i*5+3] or "sys" not in lines[i*5+4] or len(lines) != replication * 5:
				l.append(f.rpartition("/")[2])
				print f
				break
	return l

def crashedOnes(pathFrom,pathTo):
	crashed_appOut = appOutSizeChecker(pathFrom)
	crashed_output = outputChecker(pathFrom)
	s = "Crashed stderr\n"
	for item in sorted(crashed_appOut):
		s = s + item + "\n"
	s = s + "Crashed .outputs\n"
	for item in sorted(crashed_output):
		s = s + item + "\n"	
	fo = open(pathTo+"/info/"+expName+".idata.crashed.csv","w")
	fo.write(s)
	fo.close()
	
def getSizeOfTraces(path):
	dic = {}
	#print "PATH: " + path
	for folder in sorted(glob.glob(path+"/traces/*/")):
		#print folder
		tot = 0
		for dirpath,dirnames,filenames in os.walk(folder):
			for f in filenames:
				fp = os.path.join(dirpath,f)
				tot = tot + os.path.getsize(fp)
			#print "Size of " + folder + " is " + `tot` + "\n"
			#print folder.split("/")[-2]
        	dic[folder.split("/")[-2]] = tot
	return dic

def readRuntimes(path):
	dic = {}
	for f in glob.glob(path+"/*.output"):
		fi = open(f,"r")
		flist = fi.readlines()
		for i in range (0,(len(flist)/5)):
			l = []
			job = flist[i*5].split(":")[-1].strip()
			real_t =  flist[i*5+2].split("real")[-1].strip()
			real = (float(real_t.split("m")[0]) * 60 ) + float(real_t.split("m")[-1].split("s")[0])
			l.append(real)
			user_t =  flist[i*5+3].split("user")[-1].strip()
			user = (float(user_t.split("m")[0]) * 60 ) + float(user_t.split("m")[-1].split("s")[0])
			l.append(user)
			sys_t =  flist[i*5+4].split("sys")[-1].strip()
			syst = (float(sys_t.split("m")[0]) * 60 ) + float(sys_t.split("m")[-1].split("s")[0])
			l.append(syst)
			#print job
			#print l
			dic[job]=l
	return dic

def mergeRTSZ(rtDic,szDic):
	for key,val in rtDic.items():
		if key in szDic.keys():
			val.append(szDic[key])
			szDic.pop(key)
		else:
			val.append(0.0)
		assert(len(val)==4)
		rtDic[key]=val
	print len(szDic)
	if len(szDic) != 0:
		for key,val in szDic.items():
			rtDic[key]=[0.0,0.0,0.0,val]
	return rtDic


def writeSizeToFile(sz,pathTo,expName):
	fo = open(pathTo+"/info/"+expName+".idata.size.csv","w")
	s = ""
	for key,val in sorted(sz.items()):
		s = s + key + "," + `val` + "\n"
	fo.write(s)
	fo.close()

def readSizeFromFile(f):
	fo = open(f,"r")
	lines = fo.readlines()
	dic={}
	for line in lines:
		dic[line.partition(",")[0]]=float(line.partition(",")[2].strip())
	return dic

def writeDataToFile(data,pathTo,expName):
	fo = open(pathTo+"/"+expName+".idata.csv","w")
	s = ""
	for key,val in sorted(data.items()):
		s = s + key + ","
		for item in val:
			s = s + `item` + ","
		s = s + "\n"
	fo.write(s)
	fo.close()


if len(sys.argv) != 5:
	print len(sys.argv)
	print "USAGE:\n\t " +sys.argv[0]+" expName in_path out_path sizeFromFile(0/1) "
	sys.exit(-1)

expName = sys.argv[1]
pathFrom = sys.argv[2]
pathTo = sys.argv[3]
sff = sys.argv[4]

# Generates a file contains all crashed experiments of current experiment
crashedOnes(pathFrom,pathTo)

# Reading traces sizes either from previously generated file or measuring the actual traces sizes (bytes)
if sff == "0":
	sz = getSizeOfTraces(pathFrom)
	writeSizeToFile(sz,pathTo,expName)
else:
	sz = readSizeFromFile(pathTo+"/info/"+expName+".idata.size.csv")

# Read runtimes from .output files
rt = readRuntimes(pathFrom)

# Merge runtimes and sizes to data (dic)
data = mergeRTSZ(rt,sz)

# Write data to idata files
writeDataToFile(data,pathTo,expName)
