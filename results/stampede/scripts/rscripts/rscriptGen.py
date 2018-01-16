import sys,subprocess
import glob
import os
import math


def rscript(inpath,metric,tool,mode,ipc,ips,outpath,log):
    blk=["wpinMain","wpinAll"]
    ifl = inpath+"/"+metric+"_"+tool+"_"+mode+"_"+`ipc`+"_"+`ips`+".csv"
    ofl = outpath+"/"+metric+"_"+tool+"_"+mode+"_"+`ipc`+"_"+`ips`+"_"+`log`
    main = ""
    if metric == "sd":
        main = main + "Slowdown - "
        ylab="slowdown"
    elif metric == "ts":
        main = main + "Trace size(MB) - "
        ylab="size(MB)"
    main = main + tool + " - "
    if ipc:
        main = main + "per core - "
    if ips:
        main = main + "per second - "
    main = main + "("+mode+")"
    tar=ofl.rpartition("/")[2]
    s = ""
    s = s + "print(\""+tar+"\")\n"
    s = s + "apps<-c(\"bt\",\"cg\",\"ep\",\"ft\",\"is\",\"lu\",\"mg\",\"sp\")\n"
    s = s + "cores<-c(\"16\",\"64\",\"256\",\"1024\")\n"
    s = s + "colors<-c(\"red\",\"blue\",\"orange\",\"yellow\",\"green\",\"black\",\"pink\",\"purple\")\n"
    s = s + tar+"<-read.table(\""+ifl+"\",header=F,sep=\",\")\n"
    s = s + "n_"+tar+" <- structure(list(A="+tar+"[,1],B="+tar+"[,2],C="+tar+"[,3],D="+tar+"[,4]) , .Names=cores, class=\"data.frame\",row.names=apps)\n"
    s = s + "png(file=\""+ofl+".png\")\n"
    s = s + "getOption(\"scipen\")\n"
    s = s + "opt <- options(\"scipen\" = 5)\n"
    s = s + "getOption(\"scipen\")\n"
    if log and tool not in blk:
        s = s + "barplot(as.matrix(n_"+tar+"),main=\""+main+"\",ylab=\""+ylab+"\" , xlab=\"cores\",beside=TRUE,col=colors,log=\"y\")\n"
    else:
        s = s + "barplot(as.matrix(n_"+tar+"),main=\""+main+"\",ylab=\""+ylab+"\" , xlab=\"cores\",beside=TRUE,col=colors)\n"
    s = s + "legend(\"topleft\", apps, cex=1.3, bty=\"n\", fill=colors)\n"
    s = s + "options(opt)\n"
    s = s + "dev.off()\n"
    return s

def rscript2(inpath,metric,tool,mode,ipc,ips,outpath,log):
    blk=["wpinMain","wpinAll"]
    ifl = inpath+"/"+metric+"_"+tool+"_"+mode+"_"+`ipc`+"_"+`ips`+".csv"
    ofl = outpath+"/"+metric+"_"+tool+"_"+mode+"_"+`ipc`+"_"+`ips`+"_"+`log`
    tar=ofl.rpartition("/")[2]
    s = ""
    s = s + tar+"<-read.table(\""+ifl+"\",header=F,sep=\",\")\n"
    s = s + "n_"+tar+" <- structure(list(A="+tar+"[,1],B="+tar+"[,2],C="+tar+"[,3],D="+tar+"[,4]) , .Names=cores, class=\"data.frame\",row.names=apps)\n\n\n"
    return s
        
            
if len(sys.argv) != 3:
    print "USAGE:\n\t " +sys.argv[0]+" input-path output-path"
    sys.exit(-1)

inpath=sys.argv[1]
outpath=sys.argv[2]

s = ""

tools=["pinMain","pinAll","dpinMain","dpinAll","npinMain","npinAll","hpinMain","hpinAll","wpinMain","wpinAll","callgrind","tau_exec"]
modes=["avg","med","min","max"]

metric="sd"
for tool in tools:
    for mode in modes:
        for log in [0,1]:
            s = s + rscript(inpath,metric,tool,mode,0,0,outpath,log)


metric="ts"
tools=["pinMain","pinAll","callgrind","tau_exec"]
for tool in tools:
    for mode in modes:
        for log in [0,1]:
            for ipc in [0,1]:
                for ips in [0,1]:
                    s = s + rscript(inpath,metric,tool,mode,ipc,ips,outpath,log)
#print s


ss = ""
ss = ss + rscript2(inpath,"sd","pinMain","avg",0,0,outpath,0) 
ss = ss + rscript2(inpath,"sd","pinAll","avg",0,0,outpath,0)
ss = ss + rscript2(inpath,"sd","callgrind","avg",0,0,outpath,0)  

#ss = ss + rscript(inpath,"sd","pinMain","med",0,0,outpath,0) 
#ss = ss + rscript(inpath,"sd","pinAll","med",0,0,outpath,0)
#ss = ss + rscript(inpath,"sd","callgrind","med",0,0,outpath,0)  

#ss = ss + rscript(inpath,"sd","pinMain","avg",0,0,outpath,1) 
#ss = ss + rscript(inpath,"sd","pinAll","avg",0,0,outpath,1)
#ss = ss + rscript(inpath,"sd","callgrind","avg",0,0,outpath,1)  

#ss = ss + rscript(inpath,"sd","pinMain","med",0,0,outpath,1) 
#ss = ss + rscript(inpath,"sd","pinAll","med",0,0,outpath,1)
#ss = ss + rscript(inpath,"sd","callgrind","med",0,0,outpath,1)


ss = ss + rscript2(inpath,"sd","tau_exec","avg",0,0,outpath,0)  
#ss = ss + rscript(inpath,"sd","tau_exec","med",0,0,outpath,0)  
#ss = ss + rscript(inpath,"sd","tau_exec","avg",0,0,outpath,1)  
#ss = ss + rscript(inpath,"sd","tau_exec","med",0,0,outpath,1)

 
ss = ss + rscript2(inpath,"sd","wpinMain","avg",0,0,outpath,0) 
ss = ss + rscript2(inpath,"sd","wpinAll","avg",0,0,outpath,0)

ss = ss + rscript2(inpath,"sd","npinMain","avg",0,0,outpath,0) 
ss = ss + rscript2(inpath,"sd","npinAll","avg",0,0,outpath,0)

ss = ss + rscript2(inpath,"sd","dpinMain","avg",0,0,outpath,0) 
ss = ss + rscript2(inpath,"sd","dpinAll","avg",0,0,outpath,0)

ss = ss + rscript2(inpath,"sd","hpinMain","avg",0,0,outpath,0) 
ss = ss + rscript2(inpath,"sd","hpinAll","avg",0,0,outpath,0)





ss = ss + rscript2(inpath,"ts","pinMain","avg",1,1,outpath,0) 
ss = ss + rscript2(inpath,"ts","pinAll","avg",1,1,outpath,0)
ss = ss + rscript2(inpath,"ts","callgrind","avg",1,1,outpath,0)  

ss = ss + rscript2(inpath,"ts","pinMain","avg",1,0,outpath,0) 
ss = ss + rscript2(inpath,"ts","pinAll","avg",1,0,outpath,0)
ss = ss + rscript2(inpath,"ts","callgrind","avg",1,0,outpath,0)  

print ss
