# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: genStat.py
# Description: Generates the statistic report


from ops2 import *
import ds2
import argparse


if len(sys.argv) != 3:
	print "USAGE:\n\t " +sys.argv[0]+" input-path output-path"
	sys.exit(-1)

inpath=sys.argv[1]
outpath=sys.argv[2]



modes=["med"]


############################# size and runtim blocks ##############################################

#tools=["orig","devParLotMain","devParLotAll","npinMain","npinAll","pinMain","pinAll","callgrind"]
tools=[]

objects = sorting(fileToObj(inpath))

data = genStatObjects(objects)

#metrics = ["runtime"]
metrics = ["size","runtime"]
for metric in metrics:
	for tool in tools:
		for mode in modes:
			print metric+"."+tool+"."+mode
                        print "kire khar"
			genBlocks(data,metric,tool,mode,0,0,outpath)


print "KIRRRRRRRRRRRRRRRRRR"
#################################### Slowdown blocks ##########################################



#tools=["npinMain","devParLotMain","devParLotAll","npinAll","pinMain","pinAll","callgrind"]
tools=[]
objects = sorting(fileToObj(inpath))

data = genStatObjects(objects)

metric = "slowdown"
for tool in tools:
	for mode in modes:
		print metric+"_"+tool+"_"+mode
		genBlocks(data,metric,tool,mode,0,0,outpath)


#################################### Trace Size blocks #################################################

tools=["pinMain","pinAll","callgrind"]
#tools=[]
metric = "ts"
for tool in tools:
	for mode in modes:
                print metric+"_"+tool+"_"+mode
                genBlocks(data,metric,tool,mode,1,1,outpath)
