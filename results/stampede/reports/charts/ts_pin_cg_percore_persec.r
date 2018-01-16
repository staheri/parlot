apps<-c("bt","cg","ep","ft","is","lu","mg","sp")
colors<-c("red","blue","orange","yellow","green","black","pink","purple")

cores_cg<-c("cg.16","cg.64","cg.256","cg.1024")

cores_pa<-c("pa.16","pa.64","pa.256","pa.1024")

cores_pm<-c("pm.16","pm.64","pm.256","pm.1024")

ts_callgrind_avg_1_1_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/ts_callgrind_avg_1_1.csv",header=F,sep=",")
n_ts_callgrind_avg_1_1_0 <- structure(list(A=ts_callgrind_avg_1_1_0[,1],B=ts_callgrind_avg_1_1_0[,2],C=ts_callgrind_avg_1_1_0[,3],D=ts_callgrind_avg_1_1_0[,4]) , .Names=cores_cg, class="data.frame",row.names=apps)

ts_pinAll_avg_1_1_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/ts_pinAll_avg_1_1.csv",header=F,sep=",")
n_ts_pinAll_avg_1_1_0 <- structure(list(A=ts_pinAll_avg_1_1_0[,1],B=ts_pinAll_avg_1_1_0[,2],C=ts_pinAll_avg_1_1_0[,3],D=ts_pinAll_avg_1_1_0[,4]) , .Names=cores_pa, class="data.frame",row.names=apps)

ts_pinMain_avg_1_1_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/ts_pinMain_avg_1_1.csv",header=F,sep=",")
n_ts_pinMain_avg_1_1_0 <- structure(list(A=ts_pinMain_avg_1_1_0[,1],B=ts_pinMain_avg_1_1_0[,2],C=ts_pinMain_avg_1_1_0[,3],D=ts_pinMain_avg_1_1_0[,4]) , .Names=cores_pm, class="data.frame",row.names=apps)


mix<-cbind(n_ts_callgrind_avg_1_1_0,n_ts_pinAll_avg_1_1_0,n_ts_pinMain_avg_1_1_0)

pdf(file="ts_pin_cg_percore_persec.pdf",height=6,width=25)
getOption("scipen")
opt <- options("scipen" = 5)
getOption("scipen")
barplot(as.matrix(mix),main="Trace Size(MB) per core, pre second ,Callgrind vs. ParLOT",ylab="trace size per core per second" , xlab=c(cores_cg,cores_pa,cores_pm),beside=TRUE,col=colors)
legend("topleft", apps, cex=1.3, bty="n", fill=colors)
dev.off()

