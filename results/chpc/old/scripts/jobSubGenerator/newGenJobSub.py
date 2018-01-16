#!/usr/bin/env python

# Author: Saeed Taheri, University of Utah, staheri@cs.utah.edu, 2017, All rights reserved
# Code: newGenSub.py
# Description: generates job submission scripts to run on Stampede for NAS applications with different flags {1/16,4/64,16/256,64/1024}

import toml
import argparse
import glob
import sys,subprocess

listOfBenchmarks = []
listOfTools = []

if len(sys.argv) != 5:
	print "USAGE:\n\t " +sys.argv[0]+" config-file pathToJobSub experiment_name tool"
	sys.exit(-1)

CONFIG_FILE = sys.argv[1]
pathToJobSub = sys.argv[2]
exp_name = sys.argv[3]
tll= sys.argv[4]
numberOfRuns=1

# A structure to hold the information reading from config files about benchmarks
class Benchmark:
	def __init__(self,flag,benchmark,compiler,app,topo,exec_file,module,env_var,task,node,time):
		self.flag      = flag
		self.benchmark = benchmark
		self.compiler  = compiler
		self.app       = app
		self.topo      = topo
		self.exec_file = exec_file
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
	s=s+"#SBATCH -N "+nodes+"\n#SBATCH -n "+`int(nodes)*16`+"\n#SBATCH -p normal\n#SBATCH -t "+time+"\n#SBATCH --mail-user=staheri@cs.utah.edu\n#SBATCH --mail-type=ALL\n"
	return s


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

def s_chpc_config(jobName,nodes,time,account,partition):
        s = "#!/bin/bash\n"
        s = s + "#SBATCH -A "+account+"\n"
        s = s + "#SBATCH -p "+partition+"\n"
        s = s + "#SBATCH -N "+nodes+"\n"
        s = s + "#SBATCH -n "+`int(nodes)*16`+"\n"
        s = s + "#SBATCH -t "+time+"\n"
        s = s + "#SBATCH -o "+jobName+".%j.output \n"
        s = s + "#SBATCH -e "+jobName+".%j.output \n"
        s = s + "#SBATCH --mail-user=staheri@cs.utah.edu\n"
        s = s + "#SBATCH --mail-type=ALL\n"
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
		#s = s + "\n#COPY NEEDED FILES FOR BENCHMARK\n"
		#for tc in bm.to_copy:
	#		s = s + "cp " + tc + " $WORK_DIR\n"
								
		# Copy needed files for tool
		s = s + "\n#COPY NEEDED FILES FOR TOOL\n"
		for nf in tl.needed_files:
			s = s + "cp " + nf + " $WORK_DIR\n"
		s = s + "\n# CREATE A DIRECTORY FOR TRACES OF EACH RUN\n"
		s = s + "\nmkdir -p $TRACE_DIR/$JOB."+bm.app+"."+`i`+"\n"
		s = s + "\n#File Permission\n\nchmod -R 755 $WORK_DIR\n"
		s = s +"\ncd $WORK_DIR\n"
		s = s + "\necho job:$JOB."+bm.app+"."+`i`+"\n"
		#s = s + tl.command + " execu/"+ext(bm.exec_file)+" 1> /dev/null 2> /dev/null \n"
		s = s + tl.command + " execu/"+ext(bm.exec_file)+" 1> $APPOUT_DIR/$JOB."+bm.app+"."+`i`+".txt 2> $APPOUT_DIR/$JOB."+bm.app+"."+`i`+".err.txt\n"
		s = s + "\n# CLEAN UP WORK DIR\n"
		s = s + "rm -rf $COMMON_DIR/$EXPERIMENT/$JOB/execu\n"
		# Remove needed files
		#for tc in bm.to_copy:
		#	s = s + "rm "+ext(tc)+"\n"

		for nf in tl.needed_files:
			s = s + "rm "+ext(nf)+"\n"
		if not ("npin" in tl.tool or ( tl.tool == "orig" and bm.compiler == "mpicc" )): 
			s = s + "mv $WORK_DIR/* $TRACE_DIR/$JOB."+bm.app+"."+`i`+"/\n\n"
		i = i + 1
	return s
	
	
# Generate the final SLURM script
def genScript(tol,bmk,comp,nod,app,flag):
	jobName = flag+"."+tol+"."+bmk+"."+app+"."+comp+"."+nod
	print jobName
	if "wpin" in tol:
		s = s_chpc_config(jobName,nod,"06:00:00","owner-guest","kingspeak-guest")
	else:
		s = s_chpc_config(jobName,nod,"05:00:00","owner-guest","kingspeak-guest")
	s = s + s_common(jobName)
	for tl in [x for x in listOfTools if x.tool == tol]:
		for bm in listOfBenchmarks:
#			print "BM " +  bm.flag
#			print "BMK " + flag
#			q1 = flag+"_"+tol+"_"+bmk+"_"+app+"_"+comp+"_"+nod
#			q2 = bm.flag+"_"+tl.tool+"_"+bm.benchmark+"_"+bm.app+"_"+bm.compiler+"_"+bm.node
#			if q1 == q2:
#				print "KIRRRRRRRRRRRRRRRRRRRRRRRR"
#			print "\t"+flag+"_"+tol+"_"+bmk+"_"+app+"_"+comp+"_"+nod
#			print "***************"
#			print "\t"+bm.flag+"_"+tl.tool+"_"+bm.benchmark+"_"+bm.app+"_"+bm.compiler+"_"+bm.node
#			print "***************"
			if bm.benchmark == bmk and bm.node == nod and bm.compiler == comp and bm.app == app and bm.flag == flag:
				#print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
				s = s + s_body(tl,bm)
	sub = open (pathToJobSub+"/"+jobName+".slurm","w")
	sub.write(s)
	sub.close()


# Generate execution path for NAS
def genExecPath(common,flags,comp,top,app):
	s = common+flags + "/"
	if comp == "mpicc":
		s = s + "orig-"+top+"/"+app+"."+top
	else:
		s = s + comp+"-"+top+"/"+app+"."+top
	return s


# Reads the configuration file and store the values in the Data Structure
def readConfig(conf):
	config_file=open(conf)
	config=toml.loads(config_file.read())
	for k,v in config["instool"].items():
                
	       	newTool = Tool(k,v["command"],v["module"],v["env_var"],v["needed_files"],v["path"])
	       	listOfTools.append(newTool)

	for l,a in config["benchmarks"].items():		
		for n,cd in config["compilers"].items():
			for i,e in config["nasapps"].items():
				for j,fg in config["topo"].items():
					for k,x in config["nasflags"].items():
                                                ex = genExecPath(a["path"],k,n,fg["n_task"],e["file"])
                                                newBench=Benchmark(k,l,n,i,j,ex,cd["module"],cd["env_var"],fg["n_task"],fg["n_node"],"01:00:00")
                                                listOfBenchmarks.append(newBench)
						
	
if __name__ == '__main__':
	readConfig(CONFIG_FILE)
	#tagItems()
        #cc = ["64"]
	cc = ["1","4","16","64"]
	#cc = ["2","3","5","6","7","8"]
	nasApps=["bt","cg","ep","ft","is","lu","mg","sp"]
        #nasApps=["bt","ep","lu","ft","is"]
#	nasApps=["mg"]
	flags=["o1"]
#	flags=["o2","o3"]
#	cc = ["16","64"]
	#cc=["64"]
	#cc = ["1"]
#	for item in listOfBenchmarks:
#		jobName = item.flag+"."+item.benchmark+"."+item.app+"."+item.compiler+"."+item.node
#		print jobName
	for i in cc:
		for j in nasApps:
                        for k in flags:
                                genScript(tll,"nas","mpicc",i,j,k)
#                                genScript("pinAll","nas","mpicc",i,j,k)
#                                genScript("hpinMain","nas","mpicc",i,j,k)
#                                genScript("hpinAll","nas","mpicc",i,j,k)
#                                genScript("npinMain","nas","mpicc",i,j,k)
#                                genScript("npinAll","nas","mpicc",i,j,k)
#                                genScript("orig","nas","mpicc",i,j,k)
#		genScript("hpinAll","nas","mpicc",i,j,k)
#		genScript("devParLotAll","nas","mpicc",i,j,k)
#		genScript("devParLotMain","nas","mpicc",i,j,k)
#		genScript("npinMain","nas","mpicc",i,j,k)
#	genScript("npinAll","nas","mpicc",i,j,k)
		#genScript("wpinMain","nas","mpicc",i,j,k)
		#genScript("wpinAll","nas","mpicc",i,j,k)
#		genScript("tau_exec","nas","mpicc",i,j,k)
#		genScript("callgrind","nas","mpicc",i,j,k)
#	genScript("wpinAll","nas","mpicc","16","ep","o2")
#	genScript("wpinAll","nas","mpicc","16","ep","o3")
#	genScript("wpinAll","nas","mpicc","16","mg","o3")
#genScript("orig","nas","scorep",i,j,k)
#genScript("orig","nas","tau",i,j,k)
