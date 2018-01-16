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

class decompression_Results:
	def __init__(self,j,id,dsize):
		self.job=j
                self.conf=j.conf
		self.rid=id
		self.dsize=float(dsize)
                
class integrate_objects():
	def __init__(self,key,runtimes,sizes,cratios):
		self.key = key
		self.runtimes = sorted(runtimes)
		self.sizes = sorted([sz * 1.0 / 1024  for sz in sizes ])
		self.cratios = sorted(cratios)
		self.rt_med = self.runtimes[(len(self.runtimes) - 1) / 2] if len(self.runtimes) != 0 else 0.0
		self.rt_min = self.runtimes[0] if len(self.runtimes) != 0 else 0.0
		self.rt_max = self.runtimes[-1] if len(self.runtimes) != 0 else 0.0
		self.rt_avg = self.avg(self.runtimes)
		self.sz_med = self.sizes[(len(self.sizes) - 1) / 2] if len(self.sizes) != 0 else 0.0
		self.sz_min = self.sizes[0] if len(self.sizes) != 0 else 0.0
		self.sz_max = self.sizes[-1] if len(self.sizes) != 0 else 0.0
		self.sz_avg = self.avg(self.sizes)
		self.cr_med = self.cratios[(len(self.cratios) - 1) / 2] if len(self.cratios) != 0 else 0.0
		self.cr_min = self.cratios[0] if len(self.cratios) != 0 else 0.0
		self.cr_max = self.cratios[-1] if len(self.cratios) != 0 else 0.0
		self.cr_avg = self.avg(self.cratios)
		self.stat_med={"sd":0.0,"bw":0.0}
		self.stat_avg={"sd":0.0,"bw":0.0}
		
	def avg(self,list):
		sum = 0
		if len(list) != 0:
			for el in list:
				sum = sum + el
			return (sum*1.0)/(len(list)*1.0)
		else:
			return 0.0
	def stat(self,base):
		self.stat_med["sd"] = (self.rt_med * 1.0 )/(base.rt_med * 1.0)
		self.stat_avg["sd"] = (self.rt_avg * 1.0 )/(base.rt_avg * 1.0)
		cores = int(self.key.split(".")[-1])*16
		self.stat_avg["bw"] = ( (self.sz_avg * 1.0) / cores ) / self.rt_avg
		self.stat_med["bw"] = ( (self.sz_med * 1.0) / cores ) / self.rt_med

def init():
	global idataPath
	global outPath
	idataPath=""
	outPath=""
