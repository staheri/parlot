apps<-c("bt","cg","ep","ft","is","lu","mg","sp")
colors<-c("red","blue","orange","yellow","green","black","pink","purple")

cores_npa<-c("npa.16","npa.64","npa.256","npa.1024")

cores_wpa<-c("wpa.16","wpa.64","wpa.256","wpa.1024")

cores_hpa<-c("hpa.16","hpa.64","hpa.256","hpa.1024")

cores_dpa<-c("dpa.16","dpa.64","dpa.256","dpa.1024")

cores_pa<-c("pa.16","pa.64","pa.256","pa.1024")


sd_npinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_npinAll_avg_0_0.csv",header=F,sep=",")
n_sd_npinAll_avg_0_0_0 <- structure(list(A=sd_npinAll_avg_0_0_0[,1],B=sd_npinAll_avg_0_0_0[,2],C=sd_npinAll_avg_0_0_0[,3],D=sd_npinAll_avg_0_0_0[,4]) , .Names=cores_npa, class="data.frame",row.names=apps)

sd_wpinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_wpinAll_avg_0_0.csv",header=F,sep=",")
n_sd_wpinAll_avg_0_0_0 <- structure(list(A=sd_wpinAll_avg_0_0_0[,1],B=sd_wpinAll_avg_0_0_0[,2],C=sd_wpinAll_avg_0_0_0[,3],D=sd_wpinAll_avg_0_0_0[,4]) , .Names=cores_wpa, class="data.frame",row.names=apps)


sd_hpinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_hpinAll_avg_0_0.csv",header=F,sep=",")
n_sd_hpinAll_avg_0_0_0 <- structure(list(A=sd_hpinAll_avg_0_0_0[,1],B=sd_hpinAll_avg_0_0_0[,2],C=sd_hpinAll_avg_0_0_0[,3],D=sd_hpinAll_avg_0_0_0[,4]) , .Names=cores_hpa, class="data.frame",row.names=apps)


sd_dpinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_dpinAll_avg_0_0.csv",header=F,sep=",")
n_sd_dpinAll_avg_0_0_0 <- structure(list(A=sd_dpinAll_avg_0_0_0[,1],B=sd_dpinAll_avg_0_0_0[,2],C=sd_dpinAll_avg_0_0_0[,3],D=sd_dpinAll_avg_0_0_0[,4]) , .Names=cores_dpa, class="data.frame",row.names=apps)


sd_pinAll_avg_0_0_0<-read.table("/home1/02309/staheri/apps/pintool/experiments/testingStampede/reports/blocks/orig1/sd_pinAll_avg_0_0.csv",header=F,sep=",")
n_sd_pinAll_avg_0_0_0 <- structure(list(A=sd_pinAll_avg_0_0_0[,1],B=sd_pinAll_avg_0_0_0[,2],C=sd_pinAll_avg_0_0_0[,3],D=sd_pinAll_avg_0_0_0[,4]) , .Names=cores_pa, class="data.frame",row.names=apps)


mix<-cbind(n_sd_npinAll_avg_0_0_0,n_sd_wpinAll_avg_0_0_0,n_sd_hpinAll_avg_0_0_0,n_sd_dpinAll_avg_0_0_0,n_sd_pinAll_avg_0_0_0)

pdf(file="sd_pa_det.pdf",height=6,width=25)
getOption("scipen")
opt <- options("scipen" = 5)
getOption("scipen")
barplot(as.matrix(mix),main="Detail of ParLOT(all)",ylab="slowdown" , xlab=c(cores_npa,cores_wpa,cores_hpa,cores_dpa,cores_pa),beside=TRUE,col=colors)
legend("topleft", apps, cex=1.3, bty="n", fill=colors)
dev.off()


