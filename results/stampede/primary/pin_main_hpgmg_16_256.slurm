#!/bin/bash
#SBATCH -A Nixing-Scale-Bugs  # account name
#SBATCH -J pin_main_hpgmg_16_256       # job name
#SBATCH -o pin_main_hpgmg_16_256.%j    # name of the output and error file
#SBATCH -N 16            # total number of nodes requested
#SBATCH -n 256            # total number of tasks requested
#SBATCH -p normal       # queue name
#SBATCH -t 00:10:00     # expected maximum runtime (hh:mm:ss)
 
export PATH=$PATH:/home1/02309/staheri/apps/pin-install/pin-3.0-76991-gcc-linux/
#export PATH=$PATH:/home1/02309/staheri/apps/hpgmg-itac/build/bin/
export PATH=$PATH:/home1/02309/staheri/apps/hpgmg-original/build/bin
#export PATH=$PATH:/home1/02309/staheri/apps/p4est-itac/bin
#export PATH=$PATH:/home1/02309/staheri/apps/p4est-install/bin
#export PATH=$PATH:$HOME/apps/valgrind/bin

#module load itac
#module load vtune

mkdir -p $SCRATCH/results/pin_main_hpgmg_16_256

cd $SCRATCH/results/pin_main_hpgmg_16_256

time ibrun pin -t ../../DBGpin17mainimage.so -- hpgmg-fv 4 1 > ../outputs/pin_main_hpgmg_16_256.out


