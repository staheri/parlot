#!/bin/bash

for i in 16 64 256 1024
do
    for j in D
    do
        make bt NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make cg NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make ep NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make ft NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make is NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPICC=mpicc
        make lu NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make mg NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
        make sp NPROCS=$i CLASS=$j BINDIR=$PWD/bin/o1 MPIF77=mpif77
    done
done
