#!/bin/bash
#SBATCH -A soc-kp
#SBATCH -p soc-kp
#SBATCH --mem=6400
#SBATCH -N 4
#SBATCH -n 64
#SBATCH -t 00:15:00
#SBATCH -o callgrind.4.%j.output
#SBATCH -e callgrind.4.%j.output
#SBATCH --mail-user=staheri@cs.utah.edu
#SBATCH --mail-type=ALL

#ENV VAR SETUP
export PIN_ROOT=/uufs/chpc.utah.edu/common/home/u0993036/pintool/newpin/
export PTOOL_ROOT=/uufs/chpc.utah.edu/common/home/u0993036/pintool/newpin/source/tools
export CG_ROOT=/uufs/chpc.utah.edu/common/home/u0993036/valgrind/bin
export NAS_ROOT=/uufs/chpc.utah.edu/common/home/u0993036/nas/NPB3.3-MPI/bin
export LOCAL_STORAGE=/scratch/local/
export WORKSPACE=$SCRATCH/workspace/
export TCMD="mpirun -np $SLURM_NTASKS "
EXPERIMENT=callgrind;
JOB=callgrind.4;
TRACE_DIR=$WORKSPACE/$EXPERIMENT/traces;
APPOUT_DIR=$WORKSPACE/$EXPERIMENT/app_out;
EXEC_DIR=$WORKSPACE/$EXPERIMENT/exec_dir;
FILE_DIR=$EXEC_DIR/files;
# CREATING DIRS
mkdir -p $APPOUT_DIR ; 
mkdir -p $FILE_DIR ; 
mkdir -p $TRACE_DIR ; 

echo LOADING APPROPRIATE MODULES ; 
# LOADING APPROPRIATE MODULES

echo LOADING APPROPRIATE ENV_VARS ; 
# SETTING APPROPRIATE ENVIRONMENT VARIABLES
# SETTING PATH FOR TOOLS
export PATH=$PATH:$CG_ROOT ; 


echo COPYING ; 

#COPYING EXECUTABLES AND INPUT FILES

cp $NAS_ROOT/o1/cg.C.64 $FILE_DIR ; 


#COPY NEEDED FILES FOR TOOL


####################### Runs Begin ###########################



#********************* RUN 1 *********************#


# CREATE A DIRECTORY FOR TRACES OF EACH RUN

mkdir -p $TRACE_DIR/$JOB.1 ; 

# CREATE A TEMP DIRECTORY FOR running jobs and generating traces

TEMP_DIR=$EXEC_DIR/$JOB.1 ; 

mkdir -p $TEMP_DIR;

#File Permission
chmod -R 755 $TEMP_DIR ; 

cd $TEMP_DIR ; 

echo job:$JOB.1 ; 

echo "time $TCMD valgrind --tool=callgrind $FILE_DIR/cg.C.64 1> $APPOUT_DIR/$JOB.1.txt 2> $APPOUT_DIR/$JOB.1.err.txt" ; 
time $TCMD valgrind --tool=callgrind --callgrind-out-file=/scratch/local/callgrind.%q{SLURM_NODEID}.%p $FILE_DIR/cg.C.64 1> $APPOUT_DIR/$JOB.1.txt 2> $APPOUT_DIR/$JOB.1.err.txt ; 

echo END OF JOBBBBBBBBB ; 
mv $LOCAL_STORAGE/callgrind.* $TRACE_DIR/$JOB.1/ ;


echo END OF MOVING TRACES ; 

cd $EXEC_DIR ; 

rm -rf $TEMP_DIR ; 

