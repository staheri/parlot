#!/bin/bash

#print "USAGE:\n\t " +sys.argv[0]+" config-file pathToJobSub tool experiment_name #ofRuns psize node flag runName"

for i in pinMain pinAll 
do
    for j in B
    do
	for k in 1 4
	do 
	    python newGenJobSub.py nascon2.toml $PROJECT/workspace $i $i 3 $j $k o1 run-x1
	done
    done
done




#python newGenJobSub.py nascon2.toml $PROJECT/workspace pinMain pinMain 3 C 1 o1 run-00
