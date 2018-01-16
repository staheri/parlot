#!/bin/bash
#SBATCH -A Nixing-Scale-Bugs  # account name
#SBATCH -J none_p4est_64_1024       # job name
#SBATCH -o none_p4est_64_1024.%j    # name of the output and error file
#SBATCH -N 64            # total number of nodes requested
#SBATCH -n 1024            # total number of tasks requested
#SBATCH -p normal       # queue name
#SBATCH -t 00:10:00     # expected maximum runtime (hh:mm:ss)
 
#export PATH=$PATH:/home1/02309/staheri/apps/pin-install/pin-3.0-76991-gcc-linux/
#export PATH=$PATH:/home1/02309/staheri/apps/hpgmg-itac/build/bin/
#export PATH=$PATH:/home1/02309/staheri/apps/hpgmg-original/build/bin
#export PATH=$PATH:/home1/02309/staheri/apps/p4est-itac/bin
export PATH=$PATH:/home1/02309/staheri/apps/p4est-install/bin
#export PATH=$PATH:$HOME/apps/valgrind/bin

#module load itac
#module load vtune

JOBB=none_p4est_64_1024

mkdir -p $SCRATCH/results/$JOBB

cd $SCRATCH/results/$JOBB

time ibrun p4est_mesh unit 9 > ../outputs/$JOBB.out



