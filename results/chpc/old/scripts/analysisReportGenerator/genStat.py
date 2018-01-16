# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: genStat.py
# Description: Generates the statistic report


from ops import *
import ds
import argparse

parser = argparse.ArgumentParser(description="Scripts for generting reports")
parser.add_argument("--scr",action='store_true')
parser.add_argument("--wpin",action='store_true')
parser.add_argument("--npin",action='store_true')
parser.add_argument("--pin",action='store_true')
parser.add_argument("--median",action='store_true',help="if you want the median instead of average")
parser.add_argument("--minimum",action='store_true',help="if you want the shortest runtime instead of average")
parser.add_argument("--var",action='store_true',help="if you want to generate the variablity report")
parser.add_argument("--sznrt",action='store_true',help="if you want to generate the size and runtime report")
parser.add_argument("--sd",action='store_true',help="if you want to generate the slowdown report")
parser.add_argument("--detsd",action='store_true',help="if you want to generate the detail stats of slowdown report")
parser.add_argument("--pure",action='store_true',help="if you want to generate the detail stats of pure runs")
parser.add_argument("--output",type=str,action='store',help="the output prefix of generated reports")
parser.add_argument("--datapath",type=str,action='store',help="path to data(csv)")


args=parser.parse_args()

ds.init()
ds.outpre=args.output

if args.pin:
        
        objects = sorting(filterObj(fileToObj(args.datapath)))
        if checkReplication(objects) :
                statObjects = genStatObjects(objects)
        else:
                print "Error Replication"
                sys.exit(1)
        
        if args.var:
                # Generating the report of variance and variability
                varReport(statObjects)

        if args.sd:
                # Generating the slowdown report with median or average
                if args.median:
                        sdReport(statObjects,2)
                elif args.minimum:
                        sdReport(statObjects,3)
		else:
			sdReport(statObjects,1)
        if args.sznrt:
                # Generating the size and runtime report
                if args.median:
                        sznrtReport(scalableSorting(statObjects),2)
		elif args.minimum: 
			sznrtReport(scalableSorting(statObjects),3)
                else:
                        sznrtReport(scalableSorting(statObjects),1)                        
        if args.detsd:
                # Generating the each pair slowdown report
                detsdReport(statObjects)
	if args.pure:
		tempFunc(statObjects)
		#pureReport(statObjects)

if args.wpin:
	objects = sorting(fileToObj(args.datapath))
        if checkReplication(objects) :
                statObjects = genStatObjects(objects)
        else:
                print "Error Replication"
                sys.exit(1)
	if args.median:
		wpinReport(statObjects,2)
	elif args.minimum:
		wpinReport(statObjects,3)
	else:
		wpinReport(statObjects,1)
if args.npin:
	objects = sorting(fileToObj(args.datapath))
        if checkReplication(objects) :
                statObjects = genStatObjects(objects)
        else:
                print "Error Replication"
                sys.exit(1)
	if args.median:
		npinReport(statObjects,2)
	elif args.minimum:
		npinReport(statObjects,3)
	else:
		npinReport(statObjects,1)


if args.scr:
	objects = genStatObjects(sorting(fileToObj(args.datapath)))
#	objects = sorting(fileToObj(args.datapath))
	print "kirrrrr"
	print len(objects)
	oreport(objects)
	tempFunc(objects)
#	for obj in objects:
		#printStatObject(obj)
#		printObject(obj)
