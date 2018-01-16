# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: ops.py
# Description: operations of report generating

import sys,subprocess
import glob
import os
import math

from ds2 import *
import ds2

REPLICATION = 3

def fileToObj(path):
	objects=[]
	for ft in glob.glob(path):
		fi = open(ft,"r")
		flist = fi.readlines()
		for f in flist:
			line=f.split(",")
                        print "fileToObj:"
			print "\t line: "+f
			if len(line) == 11:
				j = Job("o1",line[0],line[1],line[2],line[3],line[4])
                                
				x = Results(j,line[6],line[7],line[8],line[9],line[10])
				objects.append(x)
			else:
                                print "elseeeeee"
				j = Job(line[0],line[1],line[2],line[3],line[4],line[5])
				x = Results(j,line[7],line[8],line[9],line[10],line[11])
				objects.append(x)
				
	return objects



def printObject(obj):
	s = ""
	s = s + obj.job.name + ","
	s = s + obj.rid + " , "  
	s = s + `obj.real` + " , "  
	s = s + `obj.user` + " , "  
	s = s + `obj.sys` + " , "  
	s = s + `obj.size` + "\n"
	print s


def printStatObject(obj):
        s = ""
        s = s + obj.job.name + " , "
        s = s + "{0:.2f}".format(obj.r[0]) + " * "
        s = s + "{0:.2f}".format(obj.r[1]) + " * "
        s = s + "{0:.2f}".format(obj.r[2]) + " * "
        s = s + "{0:.2f}".format(obj.s[0]) + " * "
        s = s + "{0:.2f}".format(obj.s[1]) + " * "
        s = s + "{0:.2f}".format(obj.s[2]) + "\n"
        print s

def checkReplication(objlist):
        # Original Objects
        global REPLICATION
        rep = REPLICATION
	l = len(objlist)
        flag=1
	for i in range(0,l/rep):
                job = objlist[i*rep].job.name
		if objlist[i*rep].rid != "1" or objlist[i*rep].job.name != job :
                        print "ERROR checkReplication 1111"
			printObject(objlist[i*3])
                        flag=0
		if objlist[i*rep+1].rid != "2" or objlist[i*rep+1].job.name != job:
                        print "ERROR checkReplication 2222"
			printObject(objlist[i*3+1])
                        flag=0
		if objlist[i*rep+2].rid != "3" or objlist[i*rep+2].job.name != job:
                        print "ERROR checkReplication 3333"
			printObject(objlist[i*3+2])
                        flag=0
	return flag


def sorting(objects):
#objectsByTool = sorted(objects, key=lambda x: (x.tool,x.nodes))
	objectsByRid = sorted(objects, key=lambda x: x.rid)
	objectsByApp = sorted(objectsByRid, key=lambda x: x.job.app)
	objectsByBench = sorted(objectsByApp, key=lambda x: x.job.benchmark)
	objectsByComp = sorted(objectsByBench, key=lambda x: x.job.compiler)
	objectsByNodes = sorted(objectsByComp, key=lambda x: int(x.conf))
	objectsByTool = sorted(objectsByNodes, key=lambda x: x.job.tool)
	objectsByFlag = sorted(objectsByTool, key=lambda x: x.job.flag)
	return objectsByFlag

def scalableSorting(objects):
#objectsByTool = sorted(objects, key=lambda x: (x.tool,x.nodes))
	#objectsByRid = sorted(objects, key=lambda x: x.rid)
	objectsByNodes = sorted(objects, key=lambda x: int(x.job.conf))
	objectsByApp = sorted(objectsByNodes, key=lambda x: x.job.app)
	objectsByBench = sorted(objectsByApp, key=lambda x: x.job.benchmark)
	objectsByComp = sorted(objectsByBench, key=lambda x: x.job.compiler)
	#objectsByNodes = sorted(objectsByComp, key=lambda x: x.nodes)
	objectsByTool = sorted(objectsByComp, key=lambda x: x.job.tool)
	return objectsByTool


def genStatObjects(objects):
	# type of objects: Original
	checkReplication(objects)
	data={}
        
	for i in range(0,len(objects)/3):
                r1=objects[i*3].real
                r2=objects[i*3+1].real
                r3=objects[i*3+2].real
                s1=objects[i*3].size
                s2=objects[i*3+1].size
                s3=objects[i*3+2].size
                print "Object 1\n"
		printObject(objects[i*3])
                print "Object 2\n"
		printObject(objects[i*3+1])
                print "Object 3\n"
		printObject(objects[i*3+2])
                st = Statistics(objects[i*3].job,r1,r2,r3,s1,s2,s3)
                st.operations()
                print "Stat Object\n"
		printStatObject(st)
		jobName = objects[i*3].job.name
		print "KEYYYY\n\t" + jobName
		data[jobName]=st
        return data


def genBlocks(data,metric,tool,mode,ipc,ips,outpath):
	#type of Objects: Scalable-sorted Statistics
	apps=["bt","cg","ep","ft","is","lu","mg","sp"]
	nodes=["1","4","16"]
	s = ""
	for app in apps:
		for node in nodes:
			key = "o1."+tool+".mpicc.nas."+app+"."+node
			obj = data[key]
			res = 0.0
			#print "Key:\n\t"+key
			if metric == "size":
				res = data[key].sdata[mode]
			elif metric == "runtime":
                                print "** GEN BLocks **\nkey"
                                print key
                                
				res = data[key].rdata[mode]
                                print data[key].r[0]
                                print data[key].r[1]
                                print data[key].r[2]
                                print res
			elif metric == "slowdown":
				t = key.split(".")
				base = "o1.orig."+ t[2] + "." + t[3] + "." + t[4] + "." + t[5]
				#print data[key].rdata[mode]
                                #print "key:\n\t"
				print "Base:\n\t"+base
				#print data[base].rdata[mode]
				res = data[key].rdata[mode]/data[base].rdata[mode]
			elif metric == "ts":
				res = data[key].sdata[mode]
				if ips:
					if data[key].rdata[mode] != 0:
						res = res / data[key].rdata[mode]
					else:
						res = 0
				if ipc:
					res = res / (int(data[key].job.conf)*16)
			else:
				print "error!"
				break
			

			s = s + "{0:.2f}".format(res)+","
                        print s
		s = s[:-1] + "\n"
	print s
	if metric == "ts":
		fon = outpath+"/"+metric+"."+tool+"."+mode+"."+`ipc`+"."+`ips`+".csv"
	else:
		fon = outpath+"/"+metric+"."+tool+"."+mode+".csv"
	fout=open(fon,"w")
	fout.write(s)
	fout.close
	

        

