#!/bin/bash


for SS in pinMain pinAll npinMain npinAll hpinMain hpinAll
do
    for TT in 1 2 3 4 5 6 7 8 9 10 11 12
    do
	python newGenReport.py "/scratch/02309/staheri/main/$SS/$TT/*.8*" /scratch/02309/staheri/main/experiments/$SS$TT/traces  d.$SS.$TT;
    done
done



#python newGenReport.py "/scratch/02309/staheri/main/orig/1/*.8*" /scratch/02309/staheri/experiments/orig1/traces  d.orig.1;
#python newGenReport.py "/scratch/02309/staheri/main/orig/2/*.8*" /scratch/02309/staheri/experiments/orig2/traces  d.orig.2;
#python newGenReport.py "/scratch/02309/staheri/main/orig/3/*.8*" /scratch/02309/staheri/experiments/orig3/traces  d.orig.3;

#python genReport.py "/scratch/02309/staheri/jobSub/o1-orig-1/*.8*" /scratch/02309/staheri/experiments/o1-orig-1/traces  o1-orig-1
#python genReport.py "/scratch/02309/staheri/jobSub/o1-orig-2/*.8*" /scratch/02309/staheri/experiments/o1-orig-2/traces  o1-orig-2
#python genReport.py "/scratch/02309/staheri/jobSub/o1-orig-3/*.8*" /scratch/02309/staheri/experiments/o1-orig-3/traces  o1-orig-3
#python genReport.py "/scratch/02309/staheri/jobSub/o2-orig-1/*.8*" /scratch/02309/staheri/experiments/o2-orig-1/traces  o2-orig-1
#python genReport.py "/scratch/02309/staheri/jobSub/o2-orig-2/*.8*" /scratch/02309/staheri/experiments/o2-orig-2/traces  o2-orig-2
#python genReport.py "/scratch/02309/staheri/jobSub/o2-orig-3/*.8*" /scratch/02309/staheri/experiments/o2-orig-3/traces  o2-orig-3
#python genReport.py "/scratch/02309/staheri/jobSub/o3-orig-1/*.8*" /scratch/02309/staheri/experiments/o3-orig-1/traces  o3-orig-1
#python genReport.py "/scratch/02309/staheri/jobSub/o3-orig-2/*.8*" /scratch/02309/staheri/experiments/o3-orig-2/traces  o3-orig-2
#python genReport.py "/scratch/02309/staheri/jobSub/o3-orig-3/*.8*" /scratch/02309/staheri/experiments/o3-orig-3/traces  o3-orig-3
