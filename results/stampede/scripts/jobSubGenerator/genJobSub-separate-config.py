#!/usr/bin/env python
import toml
import argparse
import glob
import sys,subprocess

def ext(s):
	return s.rsplit("/")[-1]

def argumentParser():
	parser = argparse.ArgumentParser()


CONFIG_FILE = "config.toml"
config_file=open(CONFIG_FILE)
config=toml.loads(config_file.read())

pathToJobSub = "/work/02309/staheri/jobSub/noFlyInstrumentation/"

numberOfRuns=3
jobName=""

exp_name = "noFlyInstrumentation"
for tool,tool_properties in config["instool"].items():
	#print tool
	for benchmark,compilers in config["benchmarks"].items():
		for compiler,apps in compilers["compiler"].items():
			if ( (tool == "orig" ) or ( compiler == "mpicc" and (tool == "pinMain" or tool == "pinAll" or tool == "callgrind" or tool == "tau_exec")) ):
				for app,topologies in apps["apps"].items():
					for exnum,properties in topologies["topo"].items():
						s = ""
						jobName = tool+"."+benchmark +"."+ compiler +"."+ app +"."+ properties["n_node"] +"."+ properties["n_task"]
						command = tool_properties["command"]
						# Add sbatch config
						s=s+"#!/bin/bash\n#SBATCH -A Nixing-Scale-Bugs\n#SBATCH -J "+jobName+"\n#SBATCH -o "+jobName+".%j\n"
						s=s+"#SBATCH -N "+properties["n_node"]+"\n#SBATCH -n "+properties["n_task"]+"\n#SBATCH -p normal\n#SBATCH -t "+properties["wall_time"]+"\n"
						
						#write directories
						s = s + "\n\nEXPERIMENT = " +exp_name+"\n\nJOB = "+jobName+"\n\n"
						s = s + "COMMON_DIR = $WORK/experiments\n\nTRACE_DIR = $COMMON_DIR/$EXPERIMENT/traces\n\nAPPOUT_DIR = $COMMON_DIR/$EXPERIMENT/app_out\n\n"
						s = s + "EXEC_DIR = $COMMON_DIR/$EXPERIMENT/$JOB/exec\n\nWORK_DIR = $COMMON_DIR/$EXPERIMENT/$JOB\n\n#LOAD NEEDED MODULES\n\n"
						#write env vars
						
						# Add needed modules for benchmark 
						for env in properties["module"]:
							s = s + "module load " + env + "\n"
						
						# Add needed modules for tool 
						for env in tool_properties["module"]:
							s = s + "module load " + env + "\n"
						s = s + "\n#EXPORT ENV VARS\n\n"
						
						# Add needed env vars for benchmark
						for mod in properties["env_var"]:
							s = s + "export " + mod + "\n"
						
						# Add needed env vars for tool
						for mod in tool_properties["env_var"]:
							s = s + "export " + mod + "\n"
						
						# Add tool path to $PATH
						for pth in tool_properties["path"]:
							s = s + "export PATH=$PATH:" + pth + "\n"
			
						s=s+"\n\n####################### RUNS ###########################\n\n"
						i = 1
						while (i != numberOfRuns+1):
							s = s+"\n\n#********************* RUN "+`i`+" *********************#\n\n"
							s = s + "\n#COPYING EXECUTABLES AND INPUT FILES\n\nmkdir -p $COMMON_DIR/$EXPERIMENT/$JOB/exec\n\ncp " + properties["exec_file"] + " $EXEC_DIR\n\n"
							
							# Copy needed files for benchmark
							s = s + "\n#COPY NEEDED FILES FOR BENCHMARK\n"
							for tc in properties["to_copy"]:
								s = s + "cp " + tc + " $WORK_DIR\n"
								
							# Copy needed files for tool
							s = s + "\n#COPY NEEDED FILES FOR TOOL\n"
							for nf in tool_properties["needed_files"]:
								s = s + "cp " + nf + " $WORK_DIR\n"
							s = s + "\n# CREATE A DIRECTORY FOR TRACES OF EACH RUN\n"
							s = s + "\nmkdir -p $TRACE_DIR/$JOB."+`i`+"\n"
							s = s + "\n#File Permission\n\nchmod -R 755 $WORK_DIR\n\n"
							s = s +"\ncd $WORK_DIR\n\n"
							s = s + command + " exec/"+ext(properties["exec_file"])+" "+properties["input_args"]+" &> $APPOUT_DIR/$JOB."+`i`+".txt\n\nrm -rf exec\n\ncp -r . $TRACE_DIR/$JOB."+`i`+"\n\nrm -rf *" 
							i = i + 1
						s = s + "\n\n##################### FINAL CLEAN UP ##########################\n\nrm -rf $COMMON_DIR/$EXPERIMENT/$JOB\n"
						print jobName
						sub = open (pathToJobSub+jobName+".slurm","w")
						sub.write(s)
						sub.close()
