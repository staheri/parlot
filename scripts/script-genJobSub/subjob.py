#!/usr/bin/env python

# Author: Saeed Taheri, University of Utah, staheri@cs.utah.edu, 2017, All rights reserved
# Code: subjob.py
# Description: submit and maintain jobs

import toml
import os
import glob
import sys,subprocess
import time



def readStatusFile(f):
	dic = {}
	fi = open(f,"r")
	for ll in fi.readlines():
		l=ll.split(",")
		#print l
		dic[l[0]]=l[1]+","+l[2]+","+l[3]
	return dic
	

def updateDic(fi,qu):
	result={}
	for key,val in sorted(fi.items()):
		vals = val.split(",")
		if key not in qu.keys():
			#print key+" : "+ vals[0] + " Completed !! "
			result[key]=vals[0]+",Comp,"+vals[2].strip()
		elif key in qu.keys():
			if val != qu[key]:
				#print key+ " : "+ vals[0] + " Pending or Running !! "
				result[key]=vals[0]+","+qu[key].split(",")[1]+","+qu[key].split(",")[2]
			else:
				#print key+" : "+ vals[0] + " Still Pending !! "
				result[key]=val
	return result

def updateJobStatusFile(f):
	command = "squeue -u staheri"
	qu={}
	process = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
	si, err = process.communicate()
	jobs = si.split("\n")
	for kk in jobs[1:]:
		j = kk.split()
		#print j
		if len(j) != 0:
			qu[j[0]]=j[2]+","+j[4]+","+j[7]
	sfile=readStatusFile(f)
	res=updateDic(sfile,qu)
	fout=open(f+".tmp","w")
	sout=""
	for key,val in res.items():
		#print key
		#print val
		sout = sout + key + "," + val + "\n"
	fout.write(sout)
	fout.close()
	process = subprocess.Popen(["rm "+f], stdout=subprocess.PIPE,shell=True)
	si, err = process.communicate()
	process = subprocess.Popen(["mv "+f+".tmp "+f], stdout=subprocess.PIPE,shell=True)
	si, err = process.communicate()
	if (len(jobs) == 2):
		print "All Jobs Completed.\nExiting..."
		sys.exit(1)
		

def subjob(runPath,runName):
	cur_dir = os.getcwd()

	#fin = open(runPath+"/"+runName+".jobStatus.txt","a+")

	lisOfFolders= [name for name in os.listdir(runPath) if os.path.isdir(os.path.join(runPath, name))]

	for exp in lisOfFolders:	
		os.chdir(runPath+"/"+exp)
		for f in sorted(glob.glob(runPath+"/"+exp+"/*.slurm")):
			process = subprocess.Popen(["sbatch "+f], stdout=subprocess.PIPE,shell=True)
			si, err = process.communicate()
			jobid = si.split()[3]
			st = jobid + "," + f.rpartition("/")[2].rpartition(".")[0] + ",pending,none\n"
			print st
                        
			fin = open(runPath+"/"+runName+".jobStatus.txt","a+")
			fin.write(st)
			fin.close()
                        print "added to file " + runPath+"/"+runName+".jobStatus.txt"
		updateJobStatusFile(runPath+"/"+runName+".jobStatus.txt")
	os.chdir(cur_dir)
	

if len(sys.argv) != 2:
	print "USAGE:\n\t " +sys.argv[0]+" run"
	sys.exit(-1)

runName = sys.argv[1]
runPath = "/pylon2/cc560up/staheri/workspace/"+runName
subjob(runPath,runName)

t_end = time.time() + 60 * 7
while time.time() < t_end:
	updateJobStatusFile(runPath+"/"+runName+".jobStatus.txt")
	time.sleep(5)
