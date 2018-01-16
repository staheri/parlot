#!/bin/bash
cd DBG17all ;
make clean ;
make ;
cd ../DBG17main ;
make clean ;
make ;

cd ../DDBG17all ;
make clean ;
make ;
cd ../DDBG17main ;
make clean ;
make ;

cd ../HDBG17all ;
make clean ;
make ;
cd ../HDBG17main ;
make clean ;
make ;

cd ../NDBG17all ;
make clean ;
make ;
cd ../NDBG17main ;
make clean ;
make ;

cd ../WDBG17all ;
make clean ;
make ;
cd ../WDBG17main ;
make clean ;
make ;
cd .. ;
