#!/usr/bin/env python

# Author: Saeed Taheri, University of Utah, staheri@cs.utah.edu, 2017, All rights reserved
# Code: genJobsub-catByTopo.py
# Description: generates job submission scripts to run on Stampede (categorizes jobs by the configuration
# topology of nodes/processes {1/16,4/64,16/256,64/1024}

import toml
import argparse
import glob
import sys,subprocess

listOfBenchmarks = []
listOfTools = []

if len(sys.argv) != 4:
	print "USAGE:\n\t " +sys.argv[0]+" config-file pathToJobSub experiment_name"
	sys.exit(-1)

#CONFIG_FILE = "config.toml"
CONFIG_FILE = sys.argv[1]
#pathToJobSub = "/work/02309/staheri/jobSub/ex1classifiedByTopo"
pathToJobSub = sys.argv[2]
#exp_name = "ex1.classifiedByTopo"
exp_name = sys.argv[3]

numberOfRuns=3

# A structure to hold the information reading from config files about benchmarks

class Benchmark:
	def __init__(self,benchmark,compiler,app,topo,exec_file,input_args,to_copy,module,env_var,task,node,time):
		self.benchmark = benchmark
		self.compiler  = compiler
		self.app       = app
		self.topo      = topo
		self.exec_file = exec_file
		self.input_args= input_args
		self.to_copy   = to_copy
		self.module    = module
		self.env_var   = env_var
		self.task      = task
		self.node      = node
		self.time      = time

# A structure to hold the information reading from config files about tools
class Tool:
	def __init__(self,tool,command,module,env_var,needed_files,path):
		self.tool = tool
		self.command = command
		self.module = module
		self.env_var = env_var
		self.needed_files = needed_files
		self.path = path


# Taking out the last section of the path (job)
def ext(s):
	return s.rsplit("/")[-1]	

# Insert the Stampede-related configuration to the final output
def s_stampede_config(jobName,nodes,time):
	if "pin" in jobName:
		s="#!/bin/bash\n#SBATCH -A Nixing-Scale-Bugs\n#SBATCH -J ddt\n#SBATCH -o ddt.%j\n"
	else:
		s="#!/bin/bash\n#SBATCH -A Nixing-Scale-Bugs\n#SBATCH -J "+jobName+"\n#SBATCH -o "+jobName+".%j\n"
	s=s+"#SBATCH -N "+nodes+"\n#SBATCH -n "+`int(nodes)*16`+"\n#SBATCH -p normal\n#SBATCH -t "+time+"\n"
	return s

# Tagging items for classification purposes
def tagItems():
	for item in listOfBenchmarks:	
		if item.benchmark == "nas":
			if item.compiler == "mpicc":		
				item.tag = 1
			if item.compiler == "tau":
				item.tag = 2
			if item.compiler == "scorep":
				item.tag = 3
		if item.benchmark == "hpgmg":
			if item.compiler == "mpicc":
				item.tag = 4
			if item.compiler == "tau":
				item.tag = 5
			if item.compiler == "scorep":
				item.tag = 6
		if item.benchmark == "amg":
			if item.compiler == "mpicc":
				item.tag = 7
			if item.compiler == "tau":
				item.tag = 8
		if item.benchmark == "pkifmm":
			if item.compiler == "mpicc":
				item.tag = 9
	for item in listOfTools:
		if item.tool == "orig":
			item.tag = 1
		if item.tool == "pinMain":
			item.tag = 2
		if item.tool == "pinAll":
			item.tag = 3
		if item.tool == "tau_exec":
			item.tag = 4
		if item.tool == "callgrind":
			item.tag = 5

# Insert the common part of all scripts to the final output
def s_common(jobName):
	s = "EXPERIMENT="+exp_name+"\n"
	s = s + "JOB="+jobName+"\n"
	s = s + "COMMON_DIR=$SCRATCH/experiments\n"
	s = s + "TRACE_DIR=$COMMON_DIR/$EXPERIMENT/traces\n"
	s = s + "APPOUT_DIR=$COMMON_DIR/$EXPERIMENT/app_out\n"
	s = s + "EXEC_DIR=$COMMON_DIR/$EXPERIMENT/$JOB/execu\n"
	s = s + "WORK_DIR=$COMMON_DIR/$EXPERIMENT/$JOB\n"
	return s

# Generates and inserts the body of job (modules,executables,repitations,...)
def s_body(tl,bm):
	s = "# CREATING OUTPUT DIR\n"
	s = s + "mkdir -p $APPOUT_DIR\n"
	s = s + "# LOADING APPROPRIATE MODULES\n"
	
	for item in bm.module :
		s = s + "module load "+item+"\n"
	for item in tl.module :
		s = s + "module load "+item+"\n"
	
	s = s + "# SETTING APPROPRIATE ENVIRONMENT VARIABLES\n"
	for item in bm.env_var :
		s = s + "export "+item+"\n"
	for item in tl.env_var :
		s = s + "export "+item+"\n"
	s = s + "# SETTING PATH FOR TOOLS\n"
	for item in tl.path :
		s = s + "export PATH=$PATH:" + item + "\n"
	s=s+"\n\n####################### RUNS ###########################\n\n"
	for i in range (1,numberOfRuns+1):
		s = s+"\n\n#********************* RUN "+`i`+" *********************#\n\n"
		s = s + "\n#COPYING EXECUTABLES AND INPUT FILES\n\n"
		s = s + "mkdir -p $COMMON_DIR/$EXPERIMENT/$JOB/execu\n"
		s = s + "cp " + bm.exec_file + " $EXEC_DIR\n\n"
		# Copy needed files for benchmark
		s = s + "\n#COPY NEEDED FILES FOR BENCHMARK\n"
		for tc in bm.to_copy:
			s = s + "cp " + tc + " $WORK_DIR\n"
								
		# Copy needed files for tool
		s = s + "\n#COPY NEEDED FILES FOR TOOL\n"
		for nf in tl.needed_files:
			s = s + "cp " + nf + " $WORK_DIR\n"
		s = s + "\n# CREATE A DIRECTORY FOR TRACES OF EACH RUN\n"
		s = s + "\nmkdir -p $TRACE_DIR/$JOB."+bm.app+"."+`i`+"\n"
		s = s + "\n#File Permission\n\nchmod -R 755 $WORK_DIR\n"
		s = s +"\ncd $WORK_DIR\n"
		s = s + "\necho job:$JOB."+bm.app+"."+`i`+"\n"
		s = s + tl.command + " execu/"+ext(bm.exec_file)+" "+bm.input_args+" 1> $APPOUT_DIR/$JOB."+bm.app+"."+`i`+".txt 2> $APPOUT_DIR/$JOB."+bm.app+"."+`i`+".err.txt\n"
		s = s + "\n# CLEAN UP WORK DIR\n"
		s = s + "rm -rf $COMMON_DIR/$EXPERIMENT/$JOB/execu\n"
		# Remove needed files
		for tc in bm.to_copy:
			s = s + "rm "+ext(tc)+"\n"

		for nf in tl.needed_files:
			s = s + "rm "+ext(nf)+"\n"
		
		s = s + "mv $WORK_DIR/* $TRACE_DIR/$JOB."+bm.app+"."+`i`+"/\n\n"
		#s = s + "rm -rf $WORK_DIR/* \n\n"
		i = i + 1
	return s
	
	
# Generate the final SLURM script
def genScript(tol,bmk,comp,nod):
	jobName = tol+"."+bmk+"."+comp+"."+nod
	print jobName
	if bmk == "pkifmm":
		if nod == "16" or nod =="64":	
			if tol == "callgrind":
				s = s_stampede_config(jobName,nod,"48:00:00")
			else:
				s = s_stampede_config(jobName,nod,"24:00:00")
		else:
			s = s_stampede_config(jobName,nod,"08:00:00")
	else :
		if nod == "16":
			s = s_stampede_config(jobName,nod,"48:00:00")
		elif nod == "64":
			s = s_stampede_config(jobName,nod,"48:00:00")
		else:
			s = s_stampede_config(jobName,nod,"02:00:00")
	s = s + s_common(jobName)
	for tl in [x for x in listOfTools if x.tool == tol]:
		for bm in [x for x in listOfBenchmarks if x.benchmark == bmk and x.node == nod and x.compiler == comp]:
			s = s + s_body(tl,bm)
	sub = open (pathToJobSub+"/"+jobName+".slurm","w")
	sub.write(s)
	sub.close()
	
# Reads the configuration file and store the values in the Data Structure
def readConfig(conf):
		config_file=open(conf)
		config=toml.loads(config_file.read())
		for k,v in config["instool"].items():
			newTool = Tool(k,v["command"],v["module"],v["env_var"],v["needed_files"],v["path"])
			listOfTools.append(newTool)
		for benchmark,compilers in config["benchmarks"].items():
			for compiler,apps in compilers["compiler"].items():
				for app,topologies in apps["apps"].items():
					for topo_num,v in topologies["topo"].items():
						newBench = Benchmark(benchmark,compiler,app,topo_num,v["exec_file"],v["input_args"],v["to_copy"],v["module"],v["env_var"],v["n_task"],v["n_node"],v["wall_time"])
						listOfBenchmarks.append(newBench)

						
						
						
	

	
if __name__ == '__main__':
	readConfig(CONFIG_FILE)
	#tagItems()
	cc = ["1","4","16","64"]
	#cc = ["16","64"]
	#cc=["64"]
	#cc = ["1"]
	for i in cc:
		#genScript("orig","nas","mpicc",i)
		#genScript("orig","nas","scorep",i)
		#genScript("orig","nas","tau",i)
		#genScript("orig","hpgmg","mpicc",i)
		#genScript("orig","hpgmg","scorep",i)
		#genScript("orig","hpgmg","tau",i)
		#genScript("orig","amg","mpicc",i)
		#genScript("orig","amg","tau",i)
		#genScript("orig","pkifmm","mpicc",i)
		#genScript("pinMain","nas","mpicc",i)
		#genScript("pinMain","hpgmg","mpicc",i)
		#genScript("pinMain","amg","mpicc",i)
		#genScript("pinMain","pkifmm","mpicc",i)
		#genScript("pinAll","nas","mpicc",i)
		#genScript("pinAll","hpgmg","mpicc",i)
		#genScript("pinAll","amg","mpicc",i)
		#genScript("pinAll","pkifmm","mpicc",i)
		genScript("npinMain","nas","mpicc",i)
               # genScript("wpinMain","hpgmg","mpicc",i)
               # genScript("wpinMain","amg","mpicc",i)
                #genScript("wpinMain","pkifmm","mpicc",i)
                genScript("npinAll","nas","mpicc",i)
               # genScript("wpinAll","hpgmg","mpicc",i)
               # genScript("wpinAll","amg","mpicc",i)
                #genScript("wpinAll","pkifmm","mpicc",i)
		#genScript("tau_exec","nas","mpicc",i)
		#genScript("tau_exec","hpgmg","mpicc",i)
		#genScript("tau_exec","amg","mpicc",i)
		#genScript("tau_exec","pkifmm","mpicc",i)
		#genScript("callgrind","nas","mpicc",i)
		#genScript("callgrind","hpgmg","mpicc",i)
		#genScript("callgrind","amg","mpicc",i)
		#genScript("callgrind","pkifmm","mpicc",i)
		
