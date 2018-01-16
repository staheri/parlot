import sys,subprocess
import glob
import random 

def genPath(tool,app,node,frep):
    s = "/scratch/kingspeak/serial/u0993036/experiments/" + tool
    s = s + frep + "/traces/o1."
    s = s + tool + ".nas."
    s = s + app + ".mpicc."
    s = s + node + "."
    s = s + app + ".1/"
    return s

def readindexTracePATH(f):
    common_path=""
    apps= ["bt","cg","ep","ft","is","lu","mg","sp"]
    nodes = ["1","4","16","64"]
    rep = ["1","2","3"]
    fin = open(f,"r")
    ln=fin.readlines()
    dic = {}
    #print "LEN"
    #print len(ln)
    for ii in range (0,len(ln)/10):
        i = ii*10
        tool = ln[i].split(",")[0]
        #print "\t\tTOOOOOOOOOOL:"
        #print "\t\t"+tool
        for x in range(1,9):
            for y in range(0,4):
                for z in range(0,3):
                    index = ln[i+x].split(",")[(y*3)+z].rstrip()                    
                    key = "o1,"+tool+",nas,"+apps[x-1]+",mpicc,"+nodes[y]+","+apps[x-1]+","+rep[z]
                    if "d" in index:
                        val = "/scratch/02309/staheri/main/experiments/dups/traces/o1.pinAll.nas.lu.mpicc.64.lu."+index[1:]+"/"
                    else: 
                        val = genPath(tool,apps[x-1],nodes[y],index)
                    #print "\t\tKey:\n\t\t\t"+key
                    #print "\t\tVALUE:\n\t\t\t"+val
                    dic[key]=val
    return dic



def decompress(key,path):
    fout1 = open("avg-comp-ratio-pin.csv","a+")
    print key
    # generate mode 3 trace from each file in this folder:
    #command = "mkdir -p /scratch/02309/staheri/decompressed/"+key+"/ "
    #process = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
    #print "\tCommand to execute:\n"+command
    # find the list of files 
    sample=0
    lof = sorted (glob.glob(path+"/*.info"))
    if key.split(",")[5] == "1":
        sample = 1
    if key.split(",")[5] == "4":
        sample = 4
    if key.split(",")[5] == "16":
        sample = 16
    if key.split(",")[5] == "64":
        sample = 32
    randLof = random.sample(lof,sample)
    lc=[]
    lu=[]
    lr=[]
    for f in randLof:
        #print f
        trace_common = f.rpartition(".")[0]
        for ft in sorted(glob.glob(trace_common+".*")):
            if ft.split(".")[-1] == "0":
                print ft
                ret={}
                keys=key.split(",")
                #c1= (keys[1] == "pinAll" and keys[3] == "cg" and  keys[5] == "64")
                #print c1
                
                #c2= (keys[1] == "pinAll" and keys[3] == "is" and  keys[5] == "64")            
                #c3= (keys[1] == "pinAll" and keys[3] == "sp" and  keys[5] == "64")
                #c4 = (keys[1] == "pinMain" and keys[3] == "ft" and  keys[5] == "64"
                #print c2
                c1 = c2 = c3 = 0
                if c1 or c2 or c3:
                    #print "KIRR"
                    ret["com"]=0.0
                    ret["unc"]=0.0
                    ret["ratio"]=0.0
                else:
                    #print "KOS"
                    exe="./tr20"
                    trace = " "+ft+" "
                    command = exe+trace
                    process = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
                    s, err = process.communicate()
                    for l in s.split("\n"):
                        if l != "":
                        #print l
                            if "com" not in l and "unc:" not in l and "ratio:" not in l:
                            #print l[:3]
                            #print "com"
                                print "error"
                                print key
                                print l
                                break
                            else:
                            #print key
                                print l
                            #print l.split(":")[0]
                                ret[l.split(":")[0]]= float(l.split(":")[-1])
                fout2 = open("det-comp-ratio-pin.csv","a+")
                com = ret["com"]
                unc = ret["unc"]
                ratio = ret["ratio"]
                fout2.write(key+","+f.rpartition("/")[2]+","+`com`+","+`unc`+","+`ratio`+"\n")
                lr.append(ratio)
                lc.append(com)
                lu.append(unc)
                fout2.close()
                    
         
    sumc=0
    sumu=0
    sumr=0

    for i in lc:
        sumc = sumc + i
    for i in lu:
        sumu = sumu + i
    for i in lr:
        sumr = sumr + i
    
    fout1.write(key+","+`sumc/len(lc)`+","+`sumu/len(lu)`+","+`sumr/len(lr)`+"\n")
    fout1.close()
    




data=readindexTracePATH("indexes.txt")


s = ""
#flag=1

tools=["pinMain"]
apps= ["lu","mg","sp"]
#apps= ["ft"]
#nodes = ["64"]
#reps = ["2"]

tools=["pinAll"]
apps= ["sp"]
nodes = ["64"]
reps = ["1","2","3"]

for tool in tools:
    for app in apps:
        for node in nodes:
            for rep in reps:
                key = "o1,"+tool+",nas,"+app+",mpicc,"+node+","+app+","+rep
                decompress(key,data[key])
#for key,val in sorted(data.items()):
   # if flag:
 #   decompress(key,val)
    #    flag=0
