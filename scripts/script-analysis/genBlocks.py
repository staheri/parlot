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
ds2.idataPath = "/home/staheri/pintool/tracing/experiments/psc/idata"

#runs=["01","02","03","04","05","06","07","08","09","10","11","12"]
#runs=["02","03","05","06","07","08","11","12","13"]
#runs=["00","01","02","03","04","05"]
runs=["m1"]
keys = readConfKeygen(conf)
appKeys = allAppKeys(conf)
tbs = readTableKeys("tables.toml")



allData=readiData()
allObjects = genStat(genObject(allData,keys))
allColumns = genCols(allObjects,keys,appKeys)


#able (allColumns,tbs["t1"])
#able (allColumns,tbs["t2"])
#able (allColumns,tbs["t3"])
#able (allColumns,tbs["t4"])
#table (allColumns,tbs["t5"])

detailReport(allColumns,tbs["dm1"])
detailReport(allColumns,tbs["dm2"])
detailReport(allColumns,tbs["dm3"])
detailReport(allColumns,tbs["dm4"])
detailReport(allColumns,tbs["dm5"])
detailReport(allColumns,tbs["dm6"])
detailReport(allColumns,tbs["dm7"])
detailReport(allColumns,tbs["dm8"])


detailReport(allColumns,tbs["da1"])
detailReport(allColumns,tbs["da2"])
detailReport(allColumns,tbs["da3"])
detailReport(allColumns,tbs["da4"])
detailReport(allColumns,tbs["da5"])
detailReport(allColumns,tbs["da6"])
detailReport(allColumns,tbs["da7"])
detailReport(allColumns,tbs["da8"])
