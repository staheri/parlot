# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: genStat.py
# Description: Generates the statistic report


from ops2 import *
from ds2 import *
import ds2
import argparse

if len(sys.argv) != 2:
	print "USAGE:\n\t " +sys.argv[0]+" key-config"
	sys.exit(-1)

conf=sys.argv[1]

ds2.init()
ds2.idataPath = "/uufs/chpc.utah.edu/common/home/u0993036/pintool/tracing/experiments/chpc/idata"

#runs=["01","02","03","04","05","06","07","08","09","10","11","12"]
#runs=["02","03","05","06","07","08","11","12","13"]
runs=["09","10","11","12"]
#runs=["09"]
keys = readConfKeygen(conf)
tabKeys = readTabKeys(conf)

allData={}
for r in runs:
	allData["run-"+r] = readiData("run-"+r)

allObjects={}
allColumns={}
for r in runs:
	allObjects["run-"+r] = genStat(genObject(allData,keys,"run-"+r))
	allColumns["run-"+r] = genCols(allObjects["run-"+r],keys,tabKeys)

	
run   = "run-09"
stat  = "sd"
tools = ["orig","pinMain","pinAll"]
#inputs= ["A","B","C","W"]
inputs= ["C"]
nodes = ["1","4"]
order = "itn"
#table(allColumns,run,stat,tools,inputs,nodes,order,"","")


run   = "run-09"
stat  = "sd"
tools = ["orig","pinMain","pinAll"]
inputs= ["A","B","C","W"]
nodes = ["1","4"]
order = "tni"
#table(allColumns,run,stat,tools,inputs,nodes,order,"","")

run   = "run-09"
stat  = "bw"
tools = ["orig","pinMain","pinAll"]
inputs= ["A","B","C","W"]
nodes = ["1","4"]
order = "tni"
#table(allColumns,run,stat,tools,inputs,nodes,order,"","")

run   = "run-09"
stat  = "cr"
tools = ["orig","pinMain","pinAll"]
inputs= ["A","B","C","W"]
nodes = ["1","4"]
order = "tni"
#table(allColumns,run,stat,tools,inputs,nodes,order,"","")


run   = "run-09"
stat  = "rt"
inputs= ["C"]
nodes = ["1","4"]
which = "Main"

detailReport(allColumns,stat,inputs,nodes,which)

#detailReport()

