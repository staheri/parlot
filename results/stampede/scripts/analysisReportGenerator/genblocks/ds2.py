# Author: Saeed Taheri
#         University of Utah
#         staheri@cs.utah.edu
#         2017, All rights reserved
# Code: ds2.py
# Description: Data Structures and initialization of report generating 


import sys,subprocess
import glob
import os
import math
#from sets import Set


REPLICATION = 3

class Job:
        def __init__(self,fl,tl,cm,bm,ap,conf):
                # CONF is the number of nodes [1,4,16,64]
		self.flag=fl
		self.tool=tl
		self.compiler=cm
		self.benchmark = bm
		self.app=ap
                self.conf=conf
                self.name=fl+"."+tl+"."+cm+"."+bm+"."+ap+"."+conf

class Results:
	def __init__(self,j,id,real,user,sys,size):
		self.job=j
                self.conf=j.conf
		self.rid=id
		self.real=float(real)
		self.user=float(user)
		self.sys=float(sys)
		self.size=float(size)

class decompression_Results:
	def __init__(self,j,id,dsize):
		self.job=j
                self.conf=j.conf
		self.rid=id
		self.dsize=float(dsize)
                
class Statistics():
        def __init__(self,job,r1,r2,r3,s1,s2,s3):
                self.job = job
                self.r=[]
                self.s=[]
                self.r.append(r1)
                self.r.append(r2)
                self.r.append(r3)
                self.s.append(s1)
                self.s.append(s2)
                self.s.append(s3)
                self.rdata={}
                self.sdata={}
                self.sd=0
        def operations(self):
                self.s.sort()
                self.r.sort()
                self.rdata["min"]=self.r[0]
                self.rdata["max"]=self.r[2]
                self.rdata["med"]=self.r[1]
                self.rdata["avg"]=(self.r[0]+self.r[1]+self.r[2])/3.0
                ravg=self.rdata["avg"]
                #if ravg == 0:
                        #printObject(self.exp)
                #self.rdata["ratio"]=(self.rdata["max"]-self.rdata["min"])/ravg
                #self.rdata["variance"] = (math.pow((ravg-self.r[0]),2)+math.pow((ravg-self.r[1]),2)+math.pow((ravg-self.r[2]),2))/3.0
                self.sdata["min"]=self.s[0]
                self.sdata["max"]=self.s[2]
                self.sdata["med"]=self.s[1]
                self.sdata["avg"]=(self.s[0]+self.s[1]+self.s[2])/3.0
                savg=self.sdata["avg"]
                if savg != 0:
                        #printObject(self.exp)
                        self.sdata["ratio"]=(self.sdata["max"]-self.sdata["min"])/savg
                        self.sdata["variance"] = (math.pow((savg-self.s[0]),2)+math.pow((savg-self.s[1]),2)+math.pow((savg-self.s[2]),2))/3.0
                else:
                        # FOR ORIGINAL RUNS WHICH DOES NOT HAVE TRACES (size=0)
                        self.sdata["ratio"]=0
                        self.sdata["variance"]=0
        
def init():
        global outpre
        outpre=""
