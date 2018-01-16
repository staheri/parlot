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
import toml
from sets import Set
from tabulate import tabulate

from ds2 import *
import ds2



def readConfKeygen(conf):
	config_file=open(conf)
	config=toml.loads(config_file.read())
	keys = []
	for srv in config["servers"]:
		for tool in config["tools"]:
			for flag in config["optFlags"]:
				for comp in config["compilers"]:
					for bm in config["benchmarks"]:
						for app in config["nasApps"]:
							for inp in config["nasClasses"]:
								for topo in config["topo"]:
									key = srv+"."+tool+"."+flag+"."+comp+"."+bm+"."+app+"."+inp+"."+topo
									keys.append(key)
	#for it in keys:
		#print it
	#print len(keys)
	return keys

def readTabKeys(conf):
	config_file=open(conf)
	config=toml.loads(config_file.read())
	keys = []
	for srv in config["servers"]:
		for tool in config["tools"]:
			for flag in config["optFlags"]:
				for comp in config["compilers"]:
					for bm in config["benchmarks"]:
						for inp in config["nasClasses"]:
							for topo in config["topo"]:
								key = srv+"."+tool+"."+flag+"."+comp+"."+bm+".all."+inp+"."+topo
								keys.append(key)
	#for it in keys:
		#print it
	#print len(keys)
	return keys



def readiData(run):
	data = {}
	idata = ["crashed","cratio","runtime","size"]
	for item in idata:
		fi = open(ds2.idataPath+"/"+run+"-"+item+".csv","r")
		temp = {}
		tmp = []
		if item == "crashed":
			for line in fi.readlines():
				tmp.append(line)
			data[item] = tmp
		else:
			for line in fi.readlines():
				#print line
				l = line.split(",")
				temp[l[0]]=float(l[1].strip())
			data[item] = temp
	return data

	
def genObject(allData,keys,run):
	objects={}
	data=allData[run]
	crashed=[k[:-3] for k in data["crashed"]]
	print run + " Crashed"
	for item in crashed:
		print "\t"+item
	for key in keys:
		runtimes=[v for k,v in data["runtime"].items() if key in k]
		sizes=[v for k,v in data["size"].items() if key in k]
		cratios=[v for k,v in data["cratio"].items() if key in k]
		
		if len(runtimes) != 0 and len(sizes) != 0 and key not in crashed:
			#print key
			#print data["crashed"]
			obj1 = integrate_objects(key,runtimes,sizes,cratios)
			objects[key]=obj1
	#for key,val in sorted(objects.items()):
		#print key
		#printObject(val)
	return objects

def genStat(objects):
	for key in objects.keys():
		base = ""
		ks = key.split(".")
		for i in range (0, len(ks)):
			if i == 1:
				base = base + "orig."
			elif i == len(ks) - 1 :
				base = base + ks[i]
			else:
				base = base + ks[i] + "."
		if base in objects.keys():
			objects[key].stat(objects[base])
		#for key,val in sorted(objects.items()):
			#print key
			#printObject(val)
	return objects
		
def genCols(objects,keys,tabKeys):
	columns = {}
	items = ["sd","bw","rt","sz","cr",]
	apps = ["bt","cg","ep","ft","is","lu","mg","sp"]
	for item in items:
		temp_dic = {}
		for tkey in sorted(tabKeys):
			l = []
			tk = tkey.split(".")
			for app in apps:
				nkey = ""
				for i in range(0,len(tk)):
					if i == 5:
						nkey = nkey + app + "."
					elif i == len(tk) - 1 :
						nkey = nkey + tk[i]
					else:
						nkey = nkey + tk[i] + "."
				if nkey in objects.keys():
					if item == "sd" or item == "bw":
						l.append("{0:.2f}".format(objects[nkey].stat_med[item]))
					elif item == "sz":
						l.append("{0:.2f}".format(objects[nkey].sz_med))
					elif item == "rt":
						l.append("{0:.2f}".format(objects[nkey].rt_med))
					else:
						l.append("{0:.2f}".format(objects[nkey].cr_med))
				else:
					l.append(-1)
					#gengMeanCol(l)
			temp_dic[tkey] = l
		columns[item] = temp_dic
	
	#for key,val in sorted(columns.items()):
	#	print key
	#	for k,v in sorted(val.items()):
	#		print "\t"+k
	#		for item in v:
	#			print "\t\t"+`item`
	return columns

def parseOrder(order,tools,inputs,nodes):
	l = []
	if len(order) != 3:
		print "Table Error: Length of Order is " + `len(order)`
		sys.exit(-1)
	else:
		for item in list(order):
			if item == 't':
				l.append(tools)
			elif item == 'i':
				l.append(inputs)
			elif item == 'n':
				l.append(nodes)
			else:
				print "Table Error: item not in [t i n]. item: " + item
				sys.exit(-1)
	return l

def genColKey(o1,o2,o3,it1,it2,it3):
	if o1 == 't':
		if o2 == 'i':
			if o3 == 'n':
				key = "chpc."+it1+".o1.mpicc.nas.all."+it2+"."+it3
			else:
				print o1+o2+o3
				print "error"
		elif o2 == 'n':
			if o3 == 'i':
				key = "chpc."+it1+".o1.mpicc.nas.all."+it3+"."+it2
			else:
				print o1+o2+o3
				print "error"
		else:
			print o1+o2+o3
			print "error"
	elif o1 == 'i':
		if o2 == 't':
			if o3 == 'n':
				key = "chpc."+it2+".o1.mpicc.nas.all."+it1+"."+it3
			else:
				print o1+o2+o3
				print "error"
		elif o2 == 'n':
			if o3 == 't':
				key = "chpc."+it3+".o1.mpicc.nas.all."+it1+"."+it2
			else:
				print o1+o2+o3
				print "error"
		else:
			print o1+o2+o3
			print "error"
	elif o1 == 'n':
		if o2 == 'i':
			if o3 == 't':
				key = "chpc."+it3+".o1.mpicc.nas.all."+it2+"."+it1
			else:
				print o1+o2+o3
				print "error"
		elif o2 == 't':
			if o3 == 'i':
				key = "chpc."+it2+".o1.mpicc.nas.all."+it3+"."+it1
			else:
				print o1+o2+o3
				print "error"
		else:
			print o1+o2+o3
			print "error"
	else:
		print o1+o2+o3
		print "error"
	return key



def perCore(mat,nodes):
	ret = []
	for j in range(0,len(mat[0])):
		t = []
		for i in range(0,len(mat)):
			t.append(float(mat[i][j]) / (float(nodes[i]) * 16 ))
		ret.append("{0:.2f}".format(sum(t) / float(len(t)) * 1000))
	return ret
def matAvg(mat):
	ret = []
	for j in range(0,len(mat[0])):
		t = []
		for i in range(0,len(mat)):
			t.append(float(mat[i][j]))
		ret.append("{0:.2f}".format(sum(t) / float(len(t))))
	return ret
def table(allColumns,run,stat,tools,inputs,nodes,order,lastrow,lastcol):

	print "Run: "+run+"\tStat: "+stat+"\nTools:"
	print tools
	print "Inputs:"
	print inputs
	print "Nodes:"
	print nodes
	
	apps=["bt","cg","ep","ft","is","lu","mg","sp","GM"]
	mat = []
	rowIDs=[]
	koList = parseOrder(order,tools,inputs,nodes)
	if len(koList) != 3 :
		print "Table Error: Length of KoList is " + `len(koList)`
		sys.exit(-1)
	else:
		for it1 in koList[0]:
			for it2 in koList[1]:
				ravg = []
				for it3 in koList[2]:
					key = genColKey(list(order)[0],list(order)[1],list(order)[2],it1,it2,it3)
					rowIDs.append(key.split(".")[1]+"."+key.split(".")[6]+"."+key.split(".")[7])
					gm = reduce(lambda x,y: float(x)*float(y),allColumns[run][stat][key])**(1.0/len(allColumns[run][stat][key]))
					print key
					print "GeoMean: " + `gm`
					print allColumns[run][stat][key]
					tll = allColumns[run][stat][key]
					tll.append("{0:.2f}".format(gm))
					#print allColumns[run][stat][key].append("{0:.2f}".format(gm))
					print tll
					mat.append(tll)
					ravg.append(tll)
					#mat.append(allColumns[run][stat][key])
				rowIDs.append("AVG")
				mat.append(matAvg(ravg))
				#if list(order)[1] == 't' and list(order)[2] == 'n':
				#	rowIDs.append("per Core")
				#	mat.append(perCore(ravg,koList[2]))
	#print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="plain",numalign="left")
	#print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="simple",numalign="right")
	#print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="grid",numalign="right")
	#for i  in range (0,len(mat)):
	#	print mat[i]
	print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="fancy_grid",numalign="right")
	#print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="latex",numalign="right")
	#print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="latex_raw",numalign="right")
		

def printObject(obj):
	s = ""
	s = s + "\nSize Avg\t\t\t" + `obj.sz_avg`
	s = s + "\nSize Med\t\t\t" + `obj.sz_med`
	s = s + "\nRuntime Avg\t\t\t" + `obj.rt_avg`
	s = s + "\nRuntime Med\t\t\t" + `obj.rt_med`
	s = s + "\nSlowdown Avg\t\t\t" + `obj.stat_avg["sd"]`
	s = s + "\nSlowdown Med\t\t\t" + `obj.stat_med["sd"]`
	s = s + "\nComp Ratio Avg\t\t\t" + `obj.cr_avg`
	s = s + "\nComp Ratio Med\t\t\t" + `obj.cr_med`
	print s



def detailReport(allColumns,stat,inputs,nodes,which):
	tools = ["npin","dpin","pin","wpin"]
	toolRun = {"npin":"run-10","dpin":"run-10","hpin":"run-11","pin":"run-09","wpin":"run-12"}
	mat = []
	rowIDs=[]
	apps=["bt","cg","ep","ft","is","lu","mg","sp","GM"]
	for inp in inputs:
		for node in nodes:
			for tool in tools:
				key = "chpc."+tool+which+".o1.mpicc.nas.all."+inp+"."+node
				rowIDs.append(key.split(".")[1]+"."+key.split(".")[6]+"."+key.split(".")[7])
				run = toolRun[tool]
				gmt = reduce(lambda x,y: float(x)*float(y),allColumns[run][stat][key])
				if gmt > 0:
					gm = gmt**(1.0/len(allColumns[run][stat][key]))
				else:
					gm = 0
				tll = allColumns[run][stat][key]
				tll.append("{0:.2f}".format(gm))
				print tll
				mat.append(tll)
	print tabulate(mat,headers=apps,showindex=rowIDs,tablefmt="fancy_grid",numalign="right")