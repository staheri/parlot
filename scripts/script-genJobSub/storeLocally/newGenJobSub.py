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
listOfServers = []


if len(sys.argv) != 5:
	print "USAGE:\n\t " +sys.argv[0]+" config-file pathToJobSub experiment_name tool"
	sys.exit(-1)

CONFIG_FILE = sys.argv[1]
pathToJobSub = sys.argv[2]
exp_name = sys.argv[3]
ttl =  sys.argv[4]

numberOfRuns=5

# A structure to hold the information reading from config files about benchmarks
class Benchmark:
	def __init__(self,flag,benchmark,compiler,app,topo,exec_file,module,env_var,task,node,time,psize):
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
		self.psize     = psize


# A structure to hold the information reading from config files about tools
class Tool:
	def __init__(self,tool,command,module,env_var,needed_files,path):
		self.tool = tool
		self.command = command
		self.module = module
		self.env_var = env_var
		self.needed_files = needed_files
		self.path = path
class Server:
	def __init__(self,name,options,ptl,pin,ls,workspace,cg,nas,cmd):
		self.name= name
		self.options=options
		self.ptl_root=ptl
		self.pin_root=pin
		self.local_storage=ls
		self.workspace=workspace
		self.cg_root=cg
		self.nas_root=nas
		self.tcmd=cmd
		
		
		
		
#Read Config file
def readConfig(conf,srv):
	config_file=open(conf)
	config=toml.loads(config_file.read())
	
	# Server config
	v = config["server"][srv]
	newServer = Server(srv,v["options"],v["ptool_root"],v["pin_root"],v["local_storage"],v["workspace"],v["callgrind_root"],v["nas_root"],v["command"])
	listOfServers.append(newServer)
	for k,v in config["instool"].items():
	       	newTool = Tool(k,v["command"],v["module"],v["env_var"],v["needed_files"],v["path"])
	       	listOfTools.append(newTool)

	for l,a in config["benchmarks"].items():
		for n,cd in config["compilers"].items():
			for i,e in config["nasapps"].items():
				for j,fg in config["topo"].items():
					for k,x in config["nasflags"].items():
						for kcl,cls in config["nasclasses"].items():
							ex = genExecPath(a["path"],k,n,fg["n_task"],e["name"],kcl)
							newBench=Benchmark(k,l,n,i,j,ex,cd["module"],cd["env_var"],fg["n_task"],fg["n_node"],"00:01:00",kcl)
							listOfBenchmarks.append(newBench)

# Generate execution path for NAS
def genExecPath(common,flags,comp,top,app,psize):
	s = common+"/"+flags+"/"
	s = s + app+"."+psize+"."+top
	return s

# Taking out the last section of the path (job)
def ext(s):
	return s.rsplit("/")[-1]	


# Insert the Stampede-related configuration to the final output
def s_server_config(server,jobName,nodes,time):
	s = ""
	s = s + "#!/bin/bash\n"
	for opt in server.options:
		s = s + "#SBATCH " + opt + "\n"
	s = s + "#SBATCH -N " + nodes + "\n"
	s = s + "#SBATCH -n "+ `int(nodes)*16` + "\n"
	s = s + "#SBATCH -t " + time + "\n"
	s = s + "#SBATCH -o " + jobName +  ".%j.output\n"
	s = s + "#SBATCH -e " + jobName +  ".%j.output\n"
	s = s + "#SBATCH --mail-user=staheri@cs.utah.edu\n"
	s = s + "#SBATCH --mail-type=ALL\n\n"
	
	
	s = s + "#ENV VAR SETUP\n"
	s = s + "export PIN_ROOT=" + server.pin_root + "\n"
	s = s + "export PTOOL_ROOT="+server.ptl_root+"\n"
	s = s + "export CG_ROOT="+server.cg_root+"\n"
	s = s + "export NAS_ROOT="+server.nas_root+"\n"
	s = s + "export LOCAL_STORAGE="+server.local_storage+"\n"
	s = s + "export WORKSPACE="+server.workspace+"\n"
	s = s + "export TCMD=\""+server.tcmd+"\"\n"
	return s

# Insert the common part of all scripts to the final output
def s_common(jobName):
	s = "EXPERIMENT="+exp_name+";\n"
	s = s + "JOB="+jobName+";\n"
	s = s + "TRACE_DIR=$WORKSPACE/$EXPERIMENT/traces;\n"
	s = s + "APPOUT_DIR=$WORKSPACE/$EXPERIMENT/app_out;\n"
	s = s + "EXEC_DIR=$WORKSPACE/$EXPERIMENT/exec_dir;\n"
	s = s + "FILE_DIR=$EXEC_DIR/files;\n"
	s = s + "# CREATING DIRS\n"
	s = s + "mkdir -p $APPOUT_DIR ; \n"
	s = s + "mkdir -p $FILE_DIR ; \n"
	s = s + "mkdir -p $TRACE_DIR ; \n"
	s = s + "mkdir -p $LOCAL_STORAGE/ ; \n\n"
	#s = s + "#Cleaning Local Storage\n"
	#s = s + "rm -rf $LOCAL_STORAGE/myTraces1/*; \n\n"
	return s

# Generates and inserts the body of job (modules,executables,repitations,...)
def s_body(tl,bm):
	s = "\necho LOADING APPROPRIATE MODULES ; \n"
	s = s + "# LOADING APPROPRIATE MODULES\n"
	for item in bm.module :
		s = s + "module load "+item+" ; \n"
	for item in tl.module :
		s = s + "module load "+item+" ; \n\n"
	s = s + "\necho LOADING APPROPRIATE ENV_VARS ; \n"
	s = s + "# SETTING APPROPRIATE ENVIRONMENT VARIABLES\n"
	for item in bm.env_var :
		s = s + "export "+item+" ; \n"
	for item in tl.env_var :
		s = s + "export "+item+" ; \n"
	s = s + "# SETTING PATH FOR TOOLS\n"
	for item in tl.path :
		s = s + "export PATH=$PATH:" + item + " ; \n\n"
	s = s + "\necho COPYING ; \n"
	s = s + "\n#COPYING EXECUTABLES AND INPUT FILES\n\n"
	s = s + "cp " + bm.exec_file + " $FILE_DIR ; \n\n"
        # Copy needed files for tool
        s = s + "\n#COPY NEEDED FILES FOR TOOL\n"
        for nf in tl.needed_files:
                s = s + "cp " + nf + " $FILE_DIR\n"
	s=s+"\n\n####################### Runs Begin ###########################\n\n"
	for i in range (1,numberOfRuns+1):
		s = s+"\n\n#********************* RUN "+`i`+" *********************#\n\n"
		
		s = s + "\n# CREATE A DIRECTORY FOR TRACES OF EACH RUN\n"
		s = s + "\nmkdir -p $TRACE_DIR/$JOB."+`i`+" ; \n"
		s = s + "\n# CREATE A TEMP DIRECTORY FOR running jobs and generating traces\n"
                s = s + "\nTEMP_DIR=$EXEC_DIR/$JOB."+`i`+" ; \n"
                s = s + "\nmkdir -p $TEMP_DIR;\n"
		s = s + "\n#File Permission\n"
                s = s + "chmod -R 755 $TEMP_DIR ; \n"
		s = s +"\ncd $TEMP_DIR ; \n"
		s = s + "\necho job:$JOB."+`i`+" ; \n"
		s = s + "\necho \"" + tl.command + " $FILE_DIR/"+ext(bm.exec_file)+" 1> $APPOUT_DIR/$JOB."+`i`+".txt 2> $APPOUT_DIR/$JOB."+`i`+".err.txt\" ; \n"
		s = s + tl.command + " $FILE_DIR/"+ext(bm.exec_file)+" 1> $APPOUT_DIR/$JOB."+`i`+".txt 2> $APPOUT_DIR/$JOB."+`i`+".err.txt ; \n"
		s = s + "\necho END OF JOBBBBBBBBB ; \n"
		if (tl.tool == "pinMain" or tl.tool == "pinAll" or tl.tool=="callgrind"):
			s = s + "mv $LOCAL_STORAGE/Hd* $TRACE_DIR/$JOB."+`i`+"/ ;\n\n"
                if "wpin" in tl.tool:
                        s = s + "rm $TEMP_DIR/* "
		s = s + "\necho END OF MOVING TRACES ; \n"
		s = s +"\ncd $EXEC_DIR ; \n"
		s = s +"\nrm -rf $TEMP_DIR ; \n"
		i = i + 1
	s=s+"\n\n####################### Runs End ###########################\n\n"
	return s
	
	
# Generate the final SLURM script
def genScript(key,time):
	ks=key.split(".")
	srv = ks[0]
	tol = ks[1]
	flag = ks[2]
	comp = ks[3]
	bmk = ks[4]
	app = ks[5]
	psize = ks[6]
	nod = ks[7]
	
	jobName = key
	
	if len(listOfServers) != 1:
		print "error servers list"
		system.exit(-1)
		
	s = s_server_config(listOfServers[0],jobName,nod,time)
	s = s + s_common(jobName)
	for tl in [x for x in listOfTools if x.tool == tol]:
		for bm in listOfBenchmarks:
			if bm.benchmark == bmk and bm.node == nod and bm.compiler == comp and bm.app == app and bm.flag == flag and bm.psize == psize:
				s = s + s_body(tl,bm)
	sub = open (pathToJobSub+"/"+jobName+".slurm","w")
	sub.write(s)
	sub.close()




# Reads the configuration file and store the values in the Data Structure
if __name__ == '__main__':
	process = subprocess.Popen(["mkdir -p "+pathToJobSub], stdout=subprocess.PIPE,shell=True)
	si, err = process.communicate()
	print si
	server = "chpc"
	bench = "nas"
	compiler = "mpicc"
	problem_sizes=["C"]
	flags=["o1"]
	#nodes = ["1","4","16"]
	nodes = ["1","4"]
	nasApps=["cg"]
	#nasApps=["bt","cg","ep","ft","is","lu","mg","sp"]
	readConfig(CONFIG_FILE,server)
	for psize in problem_sizes:
		for node in nodes:
			for app in nasApps:
				for flag in flags:
					key=server + "." + ttl + "." + flag + "." + compiler + "." + bench + "." + app + "." + psize + "." + node
                                        print key
					if "wpin" in ttl or ttl == "callgrind":
						genScript(key,"06:00:00")
					else:
						genScript(key,"00:15:00")
