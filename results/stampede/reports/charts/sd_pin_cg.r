apps<-c("bt","cg","ep","ft","is","lu","mg","sp")
colors<-c("red","blue","orange","yellow","green","black","pink","purple")

cores_pm<-c("pm.16","pm.64","pm.256","pm.1024")

cores_pa<-c("pa.16","pa.64","pa.256","pa.1024")

cores_cg<-c("cg.16","cg.64","cg.256","cg.1024")

sd_pinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_pinMain_avg_0_0.csv",header=F,sep=",")
n_sd_pinMain_avg_0_0_0 <- structure(list(A=sd_pinMain_avg_0_0_0[,1],B=sd_pinMain_avg_0_0_0[,2],C=sd_pinMain_avg_0_0_0[,3],D=sd_pinMain_avg_0_0_0[,4]) , .Names=cores_pm, class="data.frame",row.names=apps)

sd_pinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_pinAll_avg_0_0.csv",header=F,sep=",")
n_sd_pinAll_avg_0_0_0 <- structure(list(A=sd_pinAll_avg_0_0_0[,1],B=sd_pinAll_avg_0_0_0[,2],C=sd_pinAll_avg_0_0_0[,3],D=sd_pinAll_avg_0_0_0[,4]) , .Names=cores_pa, class="data.frame",row.names=apps)

sd_callgrind_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_callgrind_avg_0_0.csv",header=F,sep=",")
n_sd_callgrind_avg_0_0_0 <- structure(list(A=sd_callgrind_avg_0_0_0[,1],B=sd_callgrind_avg_0_0_0[,2],C=sd_callgrind_avg_0_0_0[,3],D=sd_callgrind_avg_0_0_0[,4]) , .Names=cores_cg, class="data.frame",row.names=apps)


mix<-cbind(n_sd_callgrind_avg_0_0_0,n_sd_pinAll_avg_0_0_0,n_sd_pinMain_avg_0_0_0)

pdf(file="sd_pin_cg.pdf",height=6,width=15)
getOption("scipen")
opt <- options("scipen" = 5)
getOption("scipen")
barplot(as.matrix(mix),main="Callgrind vs. ParLOT",ylab="slowdown" , xlab=c(cores_cg,cores_pa,cores_pm),beside=TRUE,col=colors)
legend("topleft", apps, cex=1.3, bty="n", fill=colors)
dev.off()
