
import sys,subprocess
import glob
import os
import math

def fileTo(f):
        objects=[]
        fi = open(f,"r")
        flist = fi.readlines()
	ret={}
        for line in flist:
            ln=line.split(",")
            key = ln[1]+"."+ln[2]+"."+ln[3]+"."+ln[5]+"."+ln[7]
	    val = ln[10]
	    print key
	    print val
	    ret[key]=val
	return ret 
	    
data=fileTo("avg-comp-ratio-pin.csv")

apps=["bt","cg","ep","ft","is","lu","mg","sp"]
reps=["1","2","3"]
nodes=["1","4","16","64"]
tools = ["pinMain","pinAll"]

s=""
for tool in tools:
	fout=open("compRatio."+tool+".csv","w")
	s=""
	for app in apps:
		for node in nodes:
			avg=0
		
			#print key + "." +" 1********"
			for rep in reps:
				key = tool+".nas."+app+"."+node+"."+rep
				print key
				print data[key]
				avg = avg + float(data[key])
			avg = avg/3
			s = s + "{0:.2f}".format(avg) + ","
		s = s + "\n"
	fout.write(s)
	fout.close()
