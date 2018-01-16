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

from ds import *
import ds

REPLICATION = 3

def fileToObj(path):
	objects=[]
	for f in glob.glob(path+"/*.csv"):
		fi = open(f,"r")
		flist = fi.readlines()
		for f in flist:
			line=f.split(",")
			if len(line) == 11:
				j = Job("o1",line[0],line[1],line[2],line[3],line[4])
				x = Results(j,line[6],line[7],line[8],line[9],line[10])
				objects.append(x)
			else:
				j = Job(line[0],line[1],line[2],line[3],line[4],line[5])
				x = Results(j,line[7],line[8],line[9],line[10],line[11])
				objects.append(x)
				
	return objects


def filterObj(objects):
	new = []
	for item in objects:
		#print item.nodes
		if item.job.benchmark != "pkifmm" and item.job.benchmark != "plifmm" and item.job.tool != "wpinAll" and item.job.tool != "wpinMain" and item.job.benchmark!= "amg" and item.job.benchmark != "hpgmg":
			if not (item.job.tool == "orig" and (item.job.compiler == "scorep" or item.job.compiler == "tau") and (item.job.benchmark == "hpgmg" or item.job.benchmark == "amg")):
				new.append(item)
	return new


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
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep].job.name
                        #print objlist[i*rep].rid
                        #print "********"
			printObject(objlist[i*3])
                        flag=0
		if objlist[i*rep+1].rid != "2" or objlist[i*rep+1].job.name != job:
                        print "ERROR checkReplication 2222"
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep+1].job.name
                        #print objlist[i*rep+1].rid
                        #print "********"
			printObject(objlist[i*3+1])
                        flag=0
		if objlist[i*rep+2].rid != "3" or objlist[i*rep+2].job.name != job:
                        print "ERROR checkReplication 3333"
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep+2].job.name
                        #print objlist[i*rep+2].rid
                        #print "********"
			printObject(objlist[i*3+2])
                        flag=0
	return flag

def checkReplication2(objlist):
        # Original Objects
        global REPLICATION
        rep = REPLICATION
	l = len(objlist)
        flag=1
	for i in range(0,l/rep):
                job = objlist[i*rep].job.name
		if objlist[i*rep].rid != "1" or objlist[i*rep].job.name != job :
                        print "ERROR checkReplication 1111"
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep].job.name
                        #print objlist[i*rep].rid
                        #print "********"
			printObject(objlist[i*3])
                        flag=0
		if objlist[i*rep+1].rid != "1" or objlist[i*rep+1].job.name != job:
                        print "ERROR checkReplication 2222"
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep+1].job.name
                        #print objlist[i*rep+1].rid
                        #print "********"
			printObject(objlist[i*3+1])
                        flag=0
		if objlist[i*rep+2].rid != "1" or objlist[i*rep+2].job.name != job:
                        print "ERROR checkReplication 3333"
                        #print "job1 = " + job
                        #print "job2 = " + objlist[i*rep+2].job.name
                        #print objlist[i*rep+2].rid
                        #print "********"
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
        statObjects = []
	for i in range(0,len(objects)/3):
                r1=objects[i*3].real
                r2=objects[i*3+1].real
                r3=objects[i*3+2].real
                s1=objects[i*3].size
                s2=objects[i*3+1].size
                s3=objects[i*3+2].size
		#print objects[i*3].job.name
                st = Statistics(objects[i*3].job,r1,r2,r3,s1,s2,s3)
                st.operations()
                statObjects.append(st)
        return statObjects

def oreport(statObjects):
	ns=["1","4"]
	apps=["bt","cg","ep","ft","is","lu","mg","sp"]
	tls=["pinMain","pinAll","orig"]
	
	# Add data into a map <key: statObject.job.name, val: the whole object
	dic={}
	for obj in statObjects:
		job = obj.job.name
		print "***"
		print job
		dic[job]=obj
	
	# Generating desired columns of report
	ret = {}
	for n in ns:
		for ts in tls:
			for ap in apps:
				k1 = "wo."+ts+".mpicc.nas."+ap+"."+n
				k2 = "o1."+ts+".mpicc.nas."+ap+"."+n
				k3 = "o2."+ts+".mpicc.nas."+ap+"."+n
				k4 = "o3."+ts+".mpicc.nas."+ap+"."+n

				l = []
				print k1
				print k2
				print k3
				print k4
				l.append("{0:.2f}".format(dic[k1].rdata["min"]))
				l.append("{0:.2f}".format(dic[k2].rdata["min"]))
				l.append("{0:.2f}".format(dic[k3].rdata["min"]))
				l.append("{0:.2f}".format(dic[k4].rdata["min"]))
				
				l.append("{0:.2f}".format(dic[k1].rdata["max"]))
				l.append("{0:.2f}".format(dic[k2].rdata["max"]))
				l.append("{0:.2f}".format(dic[k3].rdata["max"]))
				l.append("{0:.2f}".format(dic[k4].rdata["max"]))
				
				l.append("{0:.2f}".format(dic[k1].rdata["med"]))
				l.append("{0:.2f}".format(dic[k2].rdata["med"]))
				l.append("{0:.2f}".format(dic[k3].rdata["med"]))
				l.append("{0:.2f}".format(dic[k4].rdata["med"]))
				
				l.append("{0:.2f}".format(dic[k1].rdata["avg"]))
				l.append("{0:.2f}".format(dic[k2].rdata["avg"]))
				l.append("{0:.2f}".format(dic[k3].rdata["avg"]))
				l.append("{0:.2f}".format(dic[k4].rdata["avg"]))
				
				k1p = "wo.orig.mpicc.nas."+ap+"."+n
				k2p = "o1.orig.mpicc.nas."+ap+"."+n
				k3p = "o2.orig.mpicc.nas."+ap+"."+n
				k4p = "o3.orig.mpicc.nas."+ap+"."+n
				
				l.append("{0:.2f}".format( dic[k1].rdata["avg"]/dic[k1p].rdata["avg"]  ))
				l.append("{0:.2f}".format( dic[k2].rdata["avg"]/dic[k2p].rdata["avg"]  ))
				l.append("{0:.2f}".format( dic[k3].rdata["avg"]/dic[k3p].rdata["avg"]  ))
				l.append("{0:.2f}".format( dic[k4].rdata["avg"]/dic[k4p].rdata["avg"]  ))

				l.append("{0:.2f}".format( dic[k1].rdata["med"]/dic[k1p].rdata["med"]  ))
				l.append("{0:.2f}".format( dic[k2].rdata["med"]/dic[k2p].rdata["med"]  ))
				l.append("{0:.2f}".format( dic[k3].rdata["med"]/dic[k3p].rdata["med"]  ))
				l.append("{0:.2f}".format( dic[k4].rdata["med"]/dic[k4p].rdata["med"]  ))

				l.append("{0:.2f}".format( dic[k1].sdata["avg"]))
				l.append("{0:.2f}".format( dic[k2].sdata["avg"]))
				l.append("{0:.2f}".format( dic[k3].sdata["avg"]))
				l.append("{0:.2f}".format( dic[k4].sdata["avg"]))
				
				ret[ts+"."+ap+"."+n]=l
	s = ""
	for n in ns:
		ss = `n`+"\nTool,App,Min,,,,Max,,,,Med,,,,Avg,,,,SD(avg),,,,SD(med),,,,Size,,,,\n"
		for ts in tls:
			for ap in apps:
				ss = ss + ts + "," + ap + ","
				for item in ret[ts+"."+ap+"."+n]:
					ss = ss + item + ","
				ss = ss + "\n"
		ss = ss + "\n\n"
		s = s + ss
	fo = open(ds.outpre+"_os.csv","w")
	fo.write(s)
	fo.close()

def tempFunc(statObjects):	
        s = "App,1,,,4,,\n"
	s = s + ",1,2,3,1,2,3\n"
	apps = ["bt","cg","ep","ft","is","lu","mg","sp"]
	cons = ["1","4","16","64"]
	objects = {}
	for item in statObjects:
		if (item.job.tool == "orig" or item.job.tool == "pinAll"  or item.job.tool == "pinMain" )  and item.job.compiler == "mpicc" and item.job.benchmark == "nas" and (item.job.app in apps) and (item.job.conf in cons) and item.job.flag == "o1":
			objects[item.job.name]=item
	for key,val in sorted(objects.items()):
		print "test"
		print key
		s = s + key + "," + "{0:.2f}".format(objects[key].r[0]) + "," + "{0:.2f}".format(objects[key].r[1]) + ","+ "{0:.2f}".format(objects[key].r[2]) + ","
		s = s + "\n"
	ff = open(ds.outpre+"_pure.csv","w")
	ff.write(s)
	ff.close()			
def pureReport(statObjects):
	s = "App,1,,,4,,,16,,,64,,\n"
	s = s + ",1,2,3,1,2,3,1,2,3,1,2,3\n"
	apps = ["bt","cg","ep","ft","is","lu","mg","sp"]
	cons = ["1","4","16","64"]
	objects = {}
	for item in statObjects:
		if item.job.tool == "orig"  and item.job.compiler == "mpicc" and item.job.benchmark == "nas" and (item.job.app in apps) and (item.job.conf in cons):
			objects[item.job.name]=item
	for ap in apps:
		s = s + ap + ","
		for co in cons:
			base = "o1.orig.mpicc.nas."+ap+"."+co
			s = s + "{0:.2f}".format(objects[base].r[0]) + "," + "{0:.2f}".format(objects[base].r[1]) + ","+ "{0:.2f}".format(objects[base].r[2]) + ","
		s = s + "\n"
	ff = open(ds.outpre+"_pure.csv","w")
	ff.write(s)
	ff.close()
	
def varReport(statObjects):
        # type of objects: Statistics
        s = "Experiment,Runtime Variance, Runtime Ratio, Size Variance, Size Ratio\n"
        for item in statObjects:
                #exp = item.job.tool+"."+item.job.compiler+"."+item.job.benchmark+"."+item.job.app+"."+item.job.nodes+"."+item.job.procs
                s = s + item.job.name + ","+"{0:.2f}".format(item.rdata["variance"]) + "," + "{0:.2f}".format(item.rdata["ratio"]) + "," + "{0:.2f}".format(item.sdata["variance"]) + "," + "{0:.2f}".format(item.sdata["ratio"])+"\n"
                #s = s + exp + ","+"{0:.2f}".format(item.rdata["variance"]) + "," + "{0:.2f}".format(item.rdata["ratio"]) + "," + "{0:.2f}".format(item.sdata["variance"]) + "," + "{0:.2f}".format(item.rdata["ratio"])+"\n"
        ff = open(ds.outpre+"_variablity.csv","w")
        ff.write(s)
        ff.close()
        
def sznrtReport(statObjects,mode):
        #type of Objects: Scalable-sorted Statistics
	s_runtime = "Experiment,16,64,256,1024\n"
	s_size = "Experiment,16,64,256,1024\n"
	for i in range (0,len(statObjects)/4):
		item1 = statObjects[i*4]
		item2 = statObjects[i*4+1]
		item3 = statObjects[i*4+2]
		item4 = statObjects[i*4+3]
		job = item1.job.name.rpartition(".")[0]
		if item1.job.conf != "1" or item2.job.conf != "4" or item3.job.conf != "16" or item4.job.conf != "64" or item2.job.name.rpartition(".")[0] != job or item3.job.name.rpartition(".")[0] != job or item4.job.name.rpartition(".")[0] != job:
			print "ERROR in sznrt Report"
			print job
                        printStatObject(item1)
                        printStatObject(item2)
                        printStatObject(item3)
                        printStatObject(item4)
                if mode == 1:
                        met="avg"
                elif mode == 2:
                        met="med"
		else:
			met="min"
		s_runtime=s_runtime+job+","+"{0:.2f}".format(item1.rdata[met])+","+"{0:.2f}".format(item2.rdata[met])+","+"{0:.2f}".format(item3.rdata[met])+","+"{0:.2f}".format(item4.rdata[met])+"\n"
		s_size = s_size+job+","+"{0:.2f}".format(item1.sdata[met]/1024)+","+"{0:.2f}".format(item2.sdata[met]/1024)+","+"{0:.2f}".format(item3.sdata[met]/1024)+","+"{0:.2f}".format(item4.sdata[met]/1024)+"\n"
	fr = open(ds.outpre+"_runtime.csv","w")
	fs = open(ds.outpre+"_size.csv","w")
	fr.write(s_runtime)
	fs.write(s_size)
	fr.close()
	fs.close()

def wpinReport(statObjects,mode):
	met = ""
        if mode == 1:
		met = "avg"
	elif mode == 2:
		met = "med"
	else:
		met = "min"
	# Add neeced objects of statObjects to a map
	# key: Job name, val: [sdata[met],rdata[met]]
	objects={}
        for obj in statObjects:
		if obj.job.tool == "wpinMain" or obj.job.tool == "wpinAll" or obj.job.tool == "pinMain" or obj.job.tool == "pinAll":
			job = obj.job.name
			#print job
			l = []
			l.append(obj.sdata[met])
			l.append(obj.rdata[met])
			objects[job]=l
	# Generate the report text
	repLines=[]
	repLines.append("Experiment,Compression Ratio,Slowdown")
	for job,val in sorted(objects.items()):
		#print job
		if "wpin" in job:
			base = job[1:]
			cratio = objects[job][0] / objects[base][0]
			slowdown = objects[job][1] / objects[base][1]
			repLines.append(job+"," + "{0:.2f}".format(cratio) + "," + "{0:.2f}".format(slowdown))
	s = ""
	for line in sorted(repLines):
		s = s + line + "\n"
        fi = open(ds.outpre+"_wpin.csv","w")
        fi.write(s)
        fi.close()

def npinReport(statObjects,mode):
	# type of objects: Statistics

	met = ""
        if mode == 1:
		met = "avg"
	elif mode == 2:
		met = "med"
	else:
		met = "min"

	# Add neeced objects of statObjects to a map
	# key: Job name, val: rdata[met]
	objects={}
	experiments_list = []
        for obj in statObjects:
		if obj.job.tool == "npinMain" or obj.job.tool == "npinAll" or obj.job.tool == "pinMain" or obj.job.tool == "pinAll" or (obj.job.tool == "orig" and obj.job.compiler == "mpicc"):
			job = obj.job.name
			l= obj.rdata[met]
			objects[job]=l
			tt = job.split(".")
			ex = ""
			for i in range(1,len(tt)):
				if i == len(tt) - 1:
					ex = ex + tt[i]
				else:
					ex = ex + tt[i] + "."
			experiments_list.append(ex)
	experiments = set(experiments_list)
	# Generate the report text
	repLines=[]
	repLines.append("Experiment,Slowdown PIN-None (Main), Slowdown PIN (Main),Slowdown PIN-None (All), Slowdown PIN (All)")
	for ex in sorted(experiments):
		sdnoneMain = objects["npinMain."+ex]/ objects["orig."+ex]
		sdnoneAll  = objects["npinAll."+ex]/ objects["orig."+ex]
		sdMain     = objects["pinMain."+ex]/ objects["orig."+ex]
		sdAll      = objects["pinAll."+ex]/ objects["orig."+ex]
		repLines.append(ex+"," + "{0:.2f}".format(sdnoneMain) + "," + "{0:.2f}".format(sdMain) + "," + "{0:.2f}".format(sdnoneAll) + "," + "{0:.2f}".format(sdAll))
	s = ""
	for line in sorted(repLines):
		s = s + line + "\n"
        fi = open(ds.outpre+"_npin.csv","w")
        fi.write(s)
        fi.close()


def sdReport(statObjects,mode):
        # type of objects: Statistics

        # Add avg(or med) runtime into a map <key: statObject.job.name, val: avg runtime or med runtime
	dic={}
	for obj in statObjects:
                #printObject(obj)
		job = obj.job.name
                if mode == 1:
		        dic[job]=obj.rdata["avg"]
                elif mode == 2:
                        dic[job]=obj.rdata["med"]
		else:
			dic[job]=obj.rdata["min"]

        # Calculating Slowdown                
        sd={}
	for key,val in sorted(dic.items()):
		if key.split(".")[0] == "orig" and key.split(".")[1] == "mpicc":
			continue
		else:
			if key.split(".")[0] == "orig" and key.split(".")[1] != "mpicc":
				t = key.split(".")
				base = t[0] + ".mpicc." + t[2] + "." + t[3] + "." + t[4]
				sd[key] = "{0:.2f}".format(dic[key]/dic[base])  
			else:
				t = key.split(".")
				base = "orig."+ t[1] + "." + t[2] + "." + t[3] + "." + t[4]
				sd[key] = "{0:.2f}".format(dic[key]/dic[base])

                                
        # Adding slowdown of each job to its Stat Objects
        for item in statObjects:
                # To avoid orig.mpicc
                if item.job.name in sd.keys():
                        item.sd = sd[item.job.name]
                        
        # Scalable sorting and generating the file
	sortedSdObjects = scalableSorting(statObjects)
	s = "Experiment,16,64,256,1024\n"
	for i in range(0,len(sortedSdObjects)/4):
		item1 = sortedSdObjects[i*4]
		item2 = sortedSdObjects[i*4+1]
		item3 = sortedSdObjects[i*4+2]
		item4 = sortedSdObjects[i*4+3]
		job = item1.job.name.rpartition(".")[0]
                # Double Check the scalable sorting
                if item1.job.conf != "1" or item2.job.conf != "4" or item3.job.conf != "16" or item4.job.conf != "64" or item2.job.name.rpartition(".")[0] != job or item3.job.name.rpartition(".")[0] != job or item4.job.name.rpartition(".")[0] != job:
			print "ERROR in Calc Slowdown"
			print job
                # To avoid 0 slowdowns
                if job+".1" in sd.keys():
		        s=s+job+","+item1.sd+","+item2.sd+","+item3.sd+","+item4.sd+"\n"
	fs = open(ds.outpre+"_slowdown.csv","w")
	fs.write(s)
	fs.close()


def detsdReport(statObjects):
        # type of objects: Statistics objects
        
        #this function is for analyzing the one-on-one slowdown ratios. Input: List of statistics objects, Output: A CSV file with some stats 

        # Add the list of runtimes into a map <key: statObject.job.name, val: [r1,r2,r3]
        dic={}
        for obj in statObjects:
                l=[]
                for rt in obj.r:
                        l.append(rt)
                dic[obj.job.name]=l
        # Calculating the one-on-one slowdown (9) and insert the list of slowdowns to a map(stat)
        stat={}
	for key,val in dic.items():
                # We are doing it only for NAS benchmark
		if (key.split(".")[0] == "orig" and key.split(".")[1] == "mpicc") or (key.split(".")[2] != "nas"):
			continue
		else:
			if key.split(".")[0] == "orig" and key.split(".")[1] != "mpicc":
				t = key.split(".")
				base = t[0] + ".mpicc." + t[2] + "." + t[3] + "." + t[4] 
                                sl =[]
                                for i in range(0,len(dic[key])):
                                        for j in range(0,len(dic[base])):
                                                sl.append(dic[key][i]/dic[base][j])
                                                
				stat[key] = sl  
			else:
				t = key.split(".")
				base = "orig."+ t[1] + "." + t[2] + "." + t[3] + "." + t[4]
				sl = []
                                for i in range(0,len(dic[key])):
                                        for j in range(0,len(dic[base])):
                                                sl.append(dic[key][i]/dic[base][j])
                                stat[key] = sl
        out="Job,sd1,sd2,sd3,sd4,sd5,sd6,sd7,sd8,sd9,percentage,AVG of Slowdowns\n"
	for key,val in sorted(stat.items()):
                # calculating how many times out of nine the slowdown is below 1
                #out = out+key.split(".")[0]+","+key.split(".")[3]
                #LTO: # of slowdowns Less Than One
                lto=0
                sum = 0
                inner_out=""
                for item in val:
                        inner_out=inner_out+"{0:.2f}".format(item)+","
                        if float(item) <= 1.0 :
                                lto = lto + 1
                        sum = sum + float(item)
                if lto/9.0 != 0:
                        out = out + key + ","
                        #out = out+key.split(".")[0]+"."+key.split(".")[1]+","+key.split(".")[4]
                        out = out +inner_out+"{0:.2f}".format(lto/9.0) + "," + "{0:.2f}".format(sum/9.0)+"\n"
        fs = open(ds.outpre+"_detail-slowdown.csv","w")
	fs.write(out)
	fs.close()

