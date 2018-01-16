#!/bin/bash
#SBATCH -A owner-guest
#SBATCH -p kingspeak-guest
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 00:10:00
#SBATCH -o o1.pinMain.nas.mg.mpicc.1.%j.output 
#SBATCH -e o1.pinMain.nas.mg.mpicc.1.%j.output 
#SBATCH --mail-user=staheri@cs.utah.edu
#SBATCH --mail-type=ALL
EXPERIMENT=test
JOB=o1.pinMain.nas.mg.mpicc.1
COMMON_DIR=$SCRATCH/experiments
TRACE_DIR=$COMMON_DIR/$EXPERIMENT/traces
APPOUT_DIR=$COMMON_DIR/$EXPERIMENT/app_out
EXEC_DIR=$COMMON_DIR/$EXPERIMENT/$JOB/execu
WORK_DIR=$COMMON_DIR/$EXPERIMENT/$JOB
# CREATING OUTPUT DIR
mkdir -p $APPOUT_DIR
# LOADING APPROPRIATE MODULES
# SETTING APPROPRIATE ENVIRONMENT VARIABLES
# SETTING PATH FOR TOOLS
export PATH=$PATH:$HOME/pintool/newpin


####################### RUNS ###########################



#********************* RUN 1 *********************#


#COPYING EXECUTABLES AND INPUT FILES

mkdir -p $COMMON_DIR/$EXPERIMENT/$JOB/execu
cp $HOME/nas/NPB3.3-MPI/bin/o1/orig-16/mg.C.16 $EXEC_DIR


#COPY NEEDED FILES FOR TOOL
cp $HOME/pintool/newpin/source/tools/DBG17main/obj-intel64/DBGpin17mainimage.so $WORK_DIR

# CREATE A DIRECTORY FOR TRACES OF EACH RUN

mkdir -p $TRACE_DIR/$JOB.mg.1

#File Permission

chmod -R 755 $WORK_DIR

cd $WORK_DIR

echo job:$JOB.mg.1
time mpirun -np $SLURM_NTASKS pin -t DBGpin17mainimage.so -- execu/mg.C.16 1> $APPOUT_DIR/$JOB.mg.1.txt 2> $APPOUT_DIR/$JOB.mg.1.err.txt

# CLEAN UP WORK DIR
rm -rf $COMMON_DIR/$EXPERIMENT/$JOB/execu
rm DBGpin17mainimage.so
mv $WORK_DIR/* $TRACE_DIR/$JOB.mg.1/

