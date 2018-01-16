apps<-c("bt","cg","ep","ft","is","lu","mg","sp")
colors<-c("red","blue","orange","yellow","green","black","pink","purple")
cores_npm<-c("npm.16","npm.64","npm.256","npm.1024")
cores_wpm<-c("wpm.16","wpm.64","wpm.256","wpm.1024")
cores_hpm<-c("hpm.16","hpm.64","hpm.256","hpm.1024")
cores_dpm<-c("dpm.16","dpm.64","dpm.256","dpm.1024")
cores_pm<-c("pm.16","pm.64","pm.256","pm.1024")

sd_npinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_npinMain_avg_0_0.csv",header=F,sep=",")
n_sd_npinMain_avg_0_0_0 <- structure(list(A=sd_npinMain_avg_0_0_0[,1],B=sd_npinMain_avg_0_0_0[,2],C=sd_npinMain_avg_0_0_0[,3],D=sd_npinMain_avg_0_0_0[,4]) , .Names=cores_npm, class="data.frame",row.names=apps)


sd_wpinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_wpinMain_avg_0_0.csv",header=F,sep=",")
n_sd_wpinMain_avg_0_0_0 <- structure(list(A=sd_wpinMain_avg_0_0_0[,1],B=sd_wpinMain_avg_0_0_0[,2],C=sd_wpinMain_avg_0_0_0[,3],D=sd_wpinMain_avg_0_0_0[,4]) , .Names=cores_wpm, class="data.frame",row.names=apps)

sd_hpinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_hpinMain_avg_0_0.csv",header=F,sep=",")
n_sd_hpinMain_avg_0_0_0 <- structure(list(A=sd_hpinMain_avg_0_0_0[,1],B=sd_hpinMain_avg_0_0_0[,2],C=sd_hpinMain_avg_0_0_0[,3],D=sd_hpinMain_avg_0_0_0[,4]) , .Names=cores_hpm, class="data.frame",row.names=apps)

sd_dpinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_dpinMain_avg_0_0.csv",header=F,sep=",")
n_sd_dpinMain_avg_0_0_0 <- structure(list(A=sd_dpinMain_avg_0_0_0[,1],B=sd_dpinMain_avg_0_0_0[,2],C=sd_dpinMain_avg_0_0_0[,3],D=sd_dpinMain_avg_0_0_0[,4]) , .Names=cores_dpm, class="data.frame",row.names=apps)

sd_pinMain_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_pinMain_avg_0_0.csv",header=F,sep=",")
n_sd_pinMain_avg_0_0_0 <- structure(list(A=sd_pinMain_avg_0_0_0[,1],B=sd_pinMain_avg_0_0_0[,2],C=sd_pinMain_avg_0_0_0[,3],D=sd_pinMain_avg_0_0_0[,4]) , .Names=cores_pm, class="data.frame",row.names=apps)


mix<-cbind(n_sd_npinMain_avg_0_0_0,n_sd_wpinMain_avg_0_0_0,n_sd_hpinMain_avg_0_0_0,n_sd_dpinMain_avg_0_0_0,n_sd_pinMain_avg_0_0_0)

pdf(file="sd_pm_det.pdf",height=6,width=25)
getOption("scipen")
opt <- options("scipen" = 5)
getOption("scipen")
barplot(as.matrix(mix),main="Detail of ParLOT(main)",ylab="slowdown" , xlab=c(cores_npm,cores_wpm,cores_hpm,cores_dpm,cores_pm),beside=TRUE,col=colors)
legend("topleft", apps, cex=1.3, bty="n", fill=colors)
dev.off()

