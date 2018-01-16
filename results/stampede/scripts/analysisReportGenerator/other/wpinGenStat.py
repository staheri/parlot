# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: wpinGenStat.py
# Description: generates the report of wpin experiments


import sys,subprocess
import glob
import os
class Experiment:
	def __init__(self,tl,cm,bm,ap,nd,prcs,id,real,user,sys,size):
		self.tool=tl
		self.compiler=cm
		self.benchmark = bm
		self.app=ap
		self.nodes=nd
		self.procs=prcs
		self.rid=id
		self.real=float(real)
		self.user=float(user)
		self.sys=float(sys)
		self.size=float(size)

class Slowdown:
	def __init__(self,tl,cm,bm,ap,nd,prcs,sd):
		self.tool=tl
		self.compiler=cm
		self.benchmark = bm
		self.app=ap
		self.nodes=nd
		self.procs=prcs
		self.slowdown=sd

def fileToObj(path):
	objects=[]
	for f in glob.glob(path+"/*.csv"):
		fi = open(f,"r")
		flist = fi.readlines()
		for fd in flist:
			line=fd.split(",")
			if len(line) != 11:
				continue
			x = Experiment(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10])
			objects.append(x)
	return objects

def wpinFileToObj(fid):
	objects=[]
	fi = open(fid,"r")
	flist = fi.readlines()
	for f in flist:
		line=f.split(",")
		if len(line) != 11:
			continue
		x = Experiment(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10])
		objects.append(x)
	return objects	

def printObject(obj):
	s = ""
	s = s + obj.tool + " , "
	s = s + obj.compiler + " , "  
	s = s + obj.benchmark + " , "  
	s = s + obj.app + " , "
	s = s + obj.nodes + " , "
	s = s + obj.procs + " , "
	s = s + obj.rid + " , "  
	s = s + `obj.real` + " , "  
	s = s + `obj.user` + " , "  
	s = s + `obj.sys` + " , "  
	s = s + `obj.size` + "\n"
	print s 

def checkReplication(objlist):
	l = len(objlist)
	for i in range(0,l/3):
		if objlist[i*3].rid != "1":
			printObject(objlist[i*3])
		if objlist[i*3+1].rid != "2":
			printObject(objlist[i*3+1])
		if objlist[i*3+2].rid != "3":
			printObject(objlist[i*3+2])
	print "done!"

def sorting(objects):
#objectsByTool = sorted(objects, key=lambda x: (x.tool,x.nodes))
	objectsByRid = sorted(objects, key=lambda x: x.rid)
	objectsByApp = sorted(objectsByRid, key=lambda x: x.app)
	objectsByBench = sorted(objectsByApp, key=lambda x: x.benchmark)
	objectsByComp = sorted(objectsByBench, key=lambda x: x.compiler)
	objectsByNodes = sorted(objectsByComp, key=lambda x: x.nodes)
	objectsByTool = sorted(objectsByNodes, key=lambda x: x.tool)
	return objectsByTool

def scalableSorting(objects):
#objectsByTool = sorted(objects, key=lambda x: (x.tool,x.nodes))
	#objectsByRid = sorted(objects, key=lambda x: x.rid)
	objectsByNodes = sorted(objects, key=lambda x: int(x.nodes))
	objectsByApp = sorted(objectsByNodes, key=lambda x: x.app)
	objectsByBench = sorted(objectsByApp, key=lambda x: x.benchmark)
	objectsByComp = sorted(objectsByBench, key=lambda x: x.compiler)
	#objectsByNodes = sorted(objectsByComp, key=lambda x: x.nodes)
	objectsByTool = sorted(objectsByComp, key=lambda x: x.tool)
	return objectsByTool

def averaging(objects):
	avgObjects = []
	for i in range(0,len(objects)/3):
		size = (objects[i*3].size + objects[i*3+1].size + objects[i*3+2].size)/3
		real = (objects[i*3].real + objects[i*3+1].real + objects[i*3+2].real)/3
		user = (objects[i*3].user + objects[i*3+1].user + objects[i*3+2].user)/3
		sys = (objects[i*3].sys + objects[i*3+1].sys + objects[i*3+2].sys)/3
		x = Experiment(objects[i*3].tool,objects[i*3].compiler,objects[i*3].benchmark,objects[i*3].app,objects[i*3].nodes,objects[i*3].procs,"0",real,user,sys,size)
		avgObjects.append(x)
	return avgObjects


def compressionRatioReport(objects,wpinObjects):
	s = "experiment,compression ratio,slowdown\n"
	o1 = {}
	o2 = {}
	t1 = {}
	t2 = {}
	for obj in objects:
		job = obj.tool + "." + obj.compiler + "." + obj.benchmark + "." + obj.app + "." + obj.nodes + "." + obj.procs
		o1[job]=obj.size
		t1[job]=obj.real
	for obj in wpinObjects:
		job = obj.tool + "." + obj.compiler + "." + obj.benchmark + "." + obj.app + "." + obj.nodes + "." + obj.procs
		o2[job]=obj.size
		t2[job]=obj.real
	r1 = {}
	r2 = {}
	for key,val in sorted(o2.items()):
		job = key.split(".")
		tl = job[0]
		if tl == "wpinMain":
			newKey = "pinMain"+ "." + job[1] + "." + job[2] + "." + job[3] + "." + job[4] + "." + job[5]
		elif tl == "wpinAll":
			newKey = "pinAll"+ "." + job[1] + "." + job[2] + "." + job[3] + "." + job[4] + "." + job[5]
		r1[key] = o2[key]/o1[newKey]
		r2[key] = t2[key]/t1[newKey]
	for key,val in sorted(r1.items()):
		s = s + key + "," + "{0:.2f}".format(r1[key]) + "," + "{0:.2f}".format(r2[key]) + "\n"
	fi = open("wpinReport.csv","w")
	fi.write(s)
	fi.close()

if len(sys.argv) != 3:
	print len(sys.argv)
	print "USAGE:\n\t " +sys.argv[0]+" pathToCSV wpinCSV"
	sys.exit(-1)

path = sys.argv[1]
wpinCSV = sys.argv[2]


objects = fileToObj(path)
wpinObjects = wpinFileToObj(wpinCSV)

objectsByTool = sorting(objects)
wpinObjectsByTool = sorting(wpinObjects)

checkReplication(objects)
checkReplication(wpinObjects)

checkReplication(objectsByTool)
checkReplication(wpinObjectsByTool)

print "##############################"


#for obj in objectsByTool:
#	printObject(obj)

avgObjects = averaging(objectsByTool)
wpinAvgObjects = averaging(wpinObjectsByTool)

#for obj in avgObjects:
#	printObject(obj)

scaleObjects = scalableSorting(avgObjects)
wpinScaleObjects = scalableSorting(wpinAvgObjects)

for obj in wpinScaleObjects:
	printObject(obj)


compressionRatioReport(scaleObjects,wpinScaleObjects)

#scaleReport(filterObj(scaleObjects))
#calcSlowdown(filterObj(scaleObjects))
