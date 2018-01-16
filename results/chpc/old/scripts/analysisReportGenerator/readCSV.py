
# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: readCsv.py
# Description: Reads from the CSV files


import sys,subprocess
import glob
import os


if len(sys.argv) != 2:
	print len(sys.argv)
	print "USAGE:\n\t " +sys.argv[0]+" CSV-file"
	sys.exit(-1)

f = sys.argv[1]
fi = open(f,"r")
flist = fi.readlines()
dic = {}
for i in range(0,len(flist)/3):
	line = flist[i*3].split(",")
	job = line[0]+"."+line[1]+"."+line[2]+"."+line[3]+"."+line[4]+"."+line[5]
	size = (float(flist[i*3].split(",")[10]) + float(flist[(i*3)+1].split(",")[10]) + float(flist[(i*3)+2].split(",")[10]))/3
	real = (float(flist[i*3].split(",")[7]) + float(flist[(i*3)+1].split(",")[7]) + float(flist[(i*3)+2].split(",")[7]))/3
	user = (float(flist[i*3].split(",")[8]) + float(flist[(i*3)+1].split(",")[8]) + float(flist[(i*3)+2].split(",")[8]))/3
	sys =  (float(flist[i*3].split(",")[9]) + float(flist[(i*3)+1].split(",")[9]) + float(flist[(i*3)+2].split(",")[9]))/3
	dic[job] = [real,user,sys,size]

stat = {}
for key,val in dic.items():
	if key.split(".")[0] == "orig" and key.split(".")[1] == "mpicc":
		continue
	else:
		if key.split(".")[0] == "orig" and key.split(".")[1] != "mpicc":
			t = key.split(".")
			base = t[0] + ".mpicc." + t[2] + "." + t[3] + "." + t[4] + "." + t[5]
			stat[key] = [float("{0:.2f}".format(dic[key][0]/dic[base][0])),float("{0:.2f}".format(dic[key][1]/dic[base][1])),float("{0:.2f}".format(dic[key][2]/dic[base][2])),float("{0:.2f}".format(dic[key][3]/1024.0))]  
		else:
			t = key.split(".")
			base = "orig."+ t[1] + "." + t[2] + "." + t[3] + "." + t[4] + "." + t[5]
			print "key > " + key
			print "base > " + base
			stat[key] = [float("{0:.2f}".format(dic[key][0]/dic[base][0])),float("{0:.2f}".format(dic[key][1]/dic[base][1])),float("{0:.2f}".format(dic[key][2]/dic[base][2])),float("{0:.2f}".format(dic[key][3]/1024.0))]  

#s = "Tool,Compiler,Benchmark,App,Nodes,Processes,Slowdown(real)(s),Slowdown(use)(s),Slowdown(sys)(s),Trace Size\n"
#s1 = ""
#s2 = ""
#for key,val in sorted(stat.items()):
#	print key
#	print val
#	t = key.split(".")
#	if t[5] == "16":
#		s1 = s1 + t[0] + "," + t[1] + "," + t[2] + "," + t[3] + "," + t[4] + "," + t[5] + "," + `val[0]` + "," + `val[1]` + "," + `val[2]` + "," + `val[3]` + "\n"
#	if t[5] == "64":
#		s2 = s2 + t[0] + "," + t[1] + "," + t[2] + "," + t[3] + "," + t[4] + "," + t[5] + "," + `val[0]` + "," + `val[1]` + "," + `val[2]` + "," + `val[3]` + "\n"

s = "Tool,App,Slowdown(real)(s),Trace Size(MB)\n"
s1 = ""
s2 = ""
for key,val in sorted(stat.items()):
	print key
	print val
	t = key.split(".")
	if t[5] == "16":
		if t[0] == "orig":
			s1 = s1 + t[1] + "," + t[3] + "," + `val[0]` + "," + `val[3]` + "\n"
		else:
			s1 = s1 + t[0] + "," + t[3] + "," + `val[0]` + "," + `val[3]` + "\n"
	if t[5] == "64":
		if t[0] == "orig":
			s2 = s2 + t[1] + "," + t[3] + "," + `val[0]` + "," + `val[3]` + "\n"
		else:
			s2 = s2 + t[0] + "," + t[3] + "," + `val[0]` + "," + `val[3]` + "\n"


fo = open("stat.csv","w")
fo.write(s+s1+"\n\n"+s2)
fo.close()
