import argparse
import glob
import sys,subprocess



def fex(f):
    print "fex : " + f
    ff=f.split(".")
    #print "***********************************"
    #print f
    #print ff[3]+","+ff[4]
    print ff[1].partition("/")[2]+","+ff[2]
    return ff[1].partition("/")[2]+","+ff[2]


def readfiles():
    ret = {}
    for f in sorted(glob.glob("./*.csv")):
        print "file : " + f
        fname=fex(f)
        fin = open(f,"r")
        for line in fin.readlines():
            print "\tline : " + line
            det = line.split(",")
            ret[fname+","+det[0].rstrip()+","+det[1].rstrip()+","+det[2].rstrip()+","+det[3].rstrip()+","+det[4].rstrip()+","+det[5].rstrip()+","+det[6].rstrip()+","+det[7].rstrip()] = det[8].rstrip()+","+det[9].rstrip()+","+det[10].rstrip()+","+det[11].rstrip()
            print "key:\n\t"+fname+","+det[0]+","+det[1]+","+det[2]+","+det[3]+","+det[4]+","+det[5]+","+det[6]+","+det[7]
            print "value:\n\t"+det[8]+","+det[9]+","+det[10]+","+det[11]
    return ret

def concatlist(ll):
    s = ""
#    l = ll.split(",")
    #print ll
    l = ll
    for i in range(0,len(l)-1):
        s = s + l[i] + ","
    #print s + l[len(l)-1]
    return s + l[len(l)-1]


def findrun(data,fname,tool,app,node,procs,frep,rep):
    if tool == "dpinMain":
        tool1 = "devParLotMain"
    elif tool == "dpinAll":
        tool1 = "devParLotAll"
    else:
        tool1=tool
    key = fname+",o1,"+tool1+",mpicc,nas,"+app+","+node+","+procs+","+frep
    print "\n*\t"+key+ "***\n"
    s = concatlist((key.split(",")[2:])[:-1])  + "," + rep + "," + data[key]
    print s
    return s



# returns a dictionary key : Tool.app.node Val: index
def readindex(data,f):
    apps= ["bt","cg","ep","ft","is","lu","mg","sp"]
    nodes = ["1","4","16","64"]
    rep = ["1","2","3"]
    fin = open(f,"r")
    ln=fin.readlines()
    dic = {}
    print "LEN"
    print len(ln)
    for ii in range (0,len(ln)/10):
        i = ii*10
        #print "i , ii"
        #print i
        #print ii
        #print ln[i-1].split(",")[0]
        #print ln[i+1].split(",")[0]
        tool = ln[i].split(",")[0]
        #print "\t\tTOOOOOOOOOOL:"
        print "\t\t"+tool
        for x in range(1,9):
            for y in range(0,4):
                for z in range(0,3):
                    if  y == 3:
                        continue
                    index = ln[i+x].split(",")[(y*3)+z].rstrip()
                    fname=tool+","+index
                    frep="1"
                    #print "\t\t\t*******  Inside Read Indexes  **********"
                    key = tool+","+apps[x-1]+","+nodes[y]+","+rep[z]
                    #print "\t\tKEY:\n\t\t\t"+key
                    val = findrun(data,fname,tool,apps[x-1],nodes[y],`int(nodes[y])*16`,frep,rep[z])
                    #print "\t\tVALUE:\n\t\t\t"+val
                    dic[key]=val
    return dic
        
data=readfiles()
indexes = readindex(data,"indexes.txt")
#indexes = readindex(data,"ind2.txt")
s = ""
nodes = ["1","4","16"]
#nodes=["1"]
for tool in ["orig","npinMain","npinAll","dpinMain","dpinAll","pinAll","pinMain","callgrind"]:
#for tool in ["orig","pinMain","pinAll","dpinMain"]:
    for node in nodes:
        for app in ["bt","cg","ep","ft","is","lu","mg","sp"]:
            for rep in ["1","2","3"]:
                #idx = indexes[tool+","+app+","+node+","+rep]
               # s = s + findrun(data,tool,rep,tool,app,node,`int(node)*16`,rep)
                #print "IDX"
                #print tool+","+app+","+node+","+rep
                s = s +  indexes[tool+","+app+","+node+","+rep]+"\n"

#            key = "orig,"+rep+",o1,orig,mpicc,nas,"+app+","+node+","+`int(node)*16`
#            s = s + concatlist(key.split(",")[2:]) + ","+rep+"," + data[key]

        #key = "orig,1,o1,orig,mpicc,nas,"+app+","+node+","+`int(node)*16`
        #s = s + concatlist(key.split(",")) + ",1," + concatlist(data[key])
        #key = "orig,2,o1,orig,mpicc,nas,"+app+","+node+","+`int(node)*16`
        #s = s + concatlist(key.split(",")) + ",2," + concatlist(data[key])
        #key = "orig,3,o1,orig,mpicc,nas,"+app+","+node+","+`int(node)*16`
        #s = s + concatlist(key.split(",")) + ",3," + concatlist(data[key])
fout = open("all-exc-wpin.csv","w")
fout.write(s)
fout.close()
            

