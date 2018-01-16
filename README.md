# pinTool

First, you need to instrument the binary of target application with DBGpin. DBGpin capture all function calls for each process/threads during the execution, compress them into byte codes and generate traces for every process/thread separately. Then you can use different versions of traceReader or ConceptLattice to decompress the traces and analyze it for different purposes.

## CONTENTS

- [Instruction](#instruction)
- [Related Tools](#related-tools)
	* [TAU](#tau)
	* [Score-p](#score-p)
	* [Valgrind](#valgrind)
	* [Vtune](#vtune)
	* [ITAC](#itac)
- [Benchmarks](#benchmarks)
	* [Tracing](#tracing)
		- [AMG](#amg2006)
		- [HPGMG](#hpgmg)
		- [NAS](#nas)
		- [pKifmm](#pkifmm)
	* [Debugging](#debugging)
		- [Integral](#integral)
		- [Eratosthenes](#eratosthenes)
		- [N-body](#n-body)
		- [ISP](#isp)
		- [TSP](#tsp)
		- [Matmul](#matmul)
	
	


## INSTRUCTION

### Instrumentation (generate traces from execution)

PIN instrumentaion tool from INTEL is already downloaded and built within "pin" folder.

Change your current directory to the repo you just cloned and run this:

`export PIN_ROOT=<path_to_here>/pin/`

`export PATH=$PIN_ROOT:$PATH`

Right now there is two versions of PIN instrumentator, One is instrumenting just the main image from the source program (DBGpin17mainimage)
and the other one is instrumAU for our purpose:enting all images including system library calls (DBGpin17allimages). 

`cd $PIN_ROOT/source/tools/DBG17main`

`make`

The make command create a new folder "obj-intel64" inside your current directory with mutators required for the instrumentation.
For simplicity of use, it is better to add this path to your $PATH or other environment variable.

`export MUTATOR_PATH=$PIN_ROOT/source/tools/DBG17main/obj-intel64`

To use the pin tool for instrumenting any executable, do:

`pin –t $MUTATOR_PATH/DBGpin17mainimage.so -- <running executable>` 
	
(e.g., `mpirun -np 8 pin –t $MUTATOR_PATH/DBGpin17mainimage.so -- ./helloWorld`)

This will generate the traces files. If you run a program on a single core with single process/thread, pin would generate a pair of .info and .0 files. 

`$ pin –t $MUTATOR_PATH/DBGpin17mainimage.so --./helloWorld`

`$ ls`

`Hdbg.17.kepler.6164.info  Hdbg.17.kepler.6164.0`

For a multiprocess version of helloWorld (MPI helloWolrd), the below command generates following files:

`$ pin –t $MUTATOR_PATH/DBGpin17mainimage.so -- mpirun -n 4 ./helloWorld_MPI`

`$ ls`

`Hdbg.17.kepler.6164.info  Hdbg.17.kepler.6164.0  Hdbg.17.kepler.6165.info  Hdbg.17.kepler.6165.0`
`Hdbg.17.kepler.6166.info  Hdbg.17.kepler.6166.0  Hdbg.17.kepler.6167.info  Hdbg.17.kepler.6167.0`

For a multiprocess/multithread version of helloWorld (MPI + OpenMP helloWorld), the below command generates following files:
```
$ OMP_NUM_THREADS = 4

$ mpirun -n 4 pin –t $MUTATOR_PATH/DBGpin17mainimage.so -- ./helloWorld_MPI_OpenMP

$ ls

Hdbg.17.kepler.6164.info  Hdbg.17.kepler.6164.0  Hdbg.17.kepler.6164.1  Hdbg.17.kepler.6164.2  Hdbg.17.kepler.6164.3
Hdbg.17.kepler.6165.info  Hdbg.17.kepler.6165.0  Hdbg.17.kepler.6165.1  Hdbg.17.kepler.6165.2  Hdbg.17.kepler.6165.3
Hdbg.17.kepler.6166.info  Hdbg.17.kepler.6166.0  Hdbg.17.kepler.6166.1  Hdbg.17.kepler.6166.2  Hdbg.17.kepler.6166.3
Hdbg.17.kepler.6167.info  Hdbg.17.kepler.6167.0  Hdbg.17.kepler.6167.1  Hdbg.17.kepler.6167.2  Hdbg.17.kepler.6167.3


The format of the name of these files are as follows: `Hbdg.<version>.<server_name>.<process_id>.<info/thread_id>
```


TraceReader (next section) will convert these files into human readable ASCII files.

### Trace Reader
```
cd traceReader

make
```
`./exec -h` for Usage options

Current version of TraceReader has two major mode:

1. Creates concept lattice out of all trace files

    * Usage for this mode:

    * `./exec -m 1 -p <path_to_traces_folder> -o <output_file_name> -d [mode_options]`

    * Mode options:

        1. Create concept lattice from function calls

        2. Create concept lattice from function edges

2. Creates a single text file from a trace file and info file

    * Usage for this mode:

    * `./exec -m 2 -i <info_file> -t <trace_file> -o <output_file_name(without extension)> -d [output_mode_options]`

    * Output mode options:

        1. Function Calls and their frequencies

        2. Function Call edges (caller-callee) and their frequencies

        3. Approximate call stack

        4. Full trace of function calls
  
## RELATED TOOLS

### TAU
- [TAU](https://www.cs.uoregon.edu/research/tau/home.php)
- Replace mpicc with tau_cc.sh
- Function-level, block (loop)-level, statement-level
-Supports user-defined events
	* TAU parallel profile data stored during execution
- Hardware counter values (multiple counters)
- Support for callgraph and callpath profiling
- All profile-level events
- Inter-process communication events
- Trace merging and format conversion
	* High details GUI report
##### Two main issues with TAU for our purpose:
- It needs recompilation with TAU scripts, makes it difficult to run it on complex benchmarks
- It collects all type of information and then we can filter out. High overhead, inappropriate for comparison


- sample report of TAU is available in *Sample* directory
Just emailed Sameer Shende and asks about these issues.

### Score-p
- [Score-p](http://www.vi-hps.org/projects/score-p/)
- Score-p looks good for our comparison with one major down point: It needs recompilation.
- sample report of Score-p is available in *Sample* directory
- * more investigation on how to change the flags to collect only function calls/stacks/traces

### Valgrind
- [valgrind-callgrind](http://valgrind.org/docs/manual/cl-manual.html)
- Needs -g flag
- Has the functionality of function call traces
- After program termination, a profile data file named callgrind.out.'pid' is generated, where pid is the process ID of the program being profiled. The data file contains information about the calls made in the program among the functions executed, together with Instruction Read (Ir) event counts.
- sample report of Valgrind is available in *Sample* directory



##### Data Collection Manipulation
- Callgrind in general is a call-graph generating and cache and branch prediction profiler. 
- The collected data by Callgrind can be presented by:
    - callgrind-annotate: prints a asorted list of functions, optionally with source annotation. 
    - KCachegrind: GUI
    - callgrind-control: interactive observe and control the status of a program current running under Callgrind’s control.
- Cachegrind collects flat profile data: event counts (data reads, cache misses, etc.) are attributed directly to the function they occurred in. This cost attribution mechanism is called self or exclusive attribution.
- Basic Usage:
`valgrind --tool=callgrind [callgrind options] your-program [program options]`

- Some options available on how to represent data (after collection) 
- Some options available on how to collect data:
    - the aggregation of event counters can be turned off until specific region of code (function) or can be turned on by user during the execution by callgrind-control.
    - Also you can limit the event collection to a specific function.
    - Callgrind command line options:
        - Dump creation options:
        - changing the name of output file
        - event counting should be performed at source line granularity (default) or at per-instruction granularity (allows assembly code annotation).
        - Compress strings to numbers (influences the output format of the profile data): specifies wether strings (file and function names) should be identified by numbers. This shrinks the file.
        - Compress positions (influences the output format of the profile data): It specifies whether numerical positions are always specified as absolute values or are allowed to be relative to previous numbers. This shrinks the file size.
        - Combine dumps: When enabled, when multiple profile data parts are to be generated these parts are appended to the same output file.
        - Dump options: after a specific count, after or before a specific function
        - Data collection options: switch on/off data instrumentation and collection at any point during the execution or by a specific function name. You can enable conditional jump, system call times and global bus event collection.
        - Cost entity separation: separate by threads, callers, recursive levels, skip PLT (ignore calls to/from PLT sections which is ON by default), skip direct recursions (ON by default)
        - Cache and branch simulation options which are all turned off by default

### Vtune
- Intel product
- Needs -g
- How much time spent on each function
- High GUI
- I could generate profiling info. It generates a bunch of weird files and the documentation is weak. Still looking for a way to interpret the generated data which would be a XML file. It could be a candidate.
- sample report of Vtune is available in *Sample* directory
- more investigation on how to change the flags to collect only function calls/stacks/traces

### ITAC
- more investigation on how to change the flags to collect only function calls/stacks/traces


## BENCHMARKS

### Tracing
Benchmarks that we used for tracing paper (PIN evaluation)
#### AMG2006
Here is the link to [runnig sets](https://asc.llnl.gov/sequoia/benchmarks/AMGTestProblemSet_v1.0.pdf) with the combination of input sizes and number of processes/nodes.

#### HPGMG 
Still looking for the best input numbers to run for at least 1 minute:

```
$ time ibrun -np 16 ./hpgmg-fv 4 8
[So many lines of output]
real  3m2.000s
user  0m1.649s
sys 0m1.345s
```
#### NAS
To be added ...

#### pKifmm
To be added ...

### Debugging

#### Integral
Injected bugs description:
area_mpi.c :
* GATHERR_S_COUNT: MPI_Gather() with wrong argument, wrong sendCount
* GATHER_R_COUNT: MPI_Gather() with wrong argument, wrong recvCount
* GATHER_ROOT: MPI_Gather() with wrong argument, wrong root
#### Eratosthenes
Injected bugs description:
c_eratosthenes_mpi.c:
* REDUCE_COUNT: MPI_Reduce() with wrong argument, wrong count
* REDUCE_ROOT: MPI_Reduce() with wrong argument, wrong root
#### N-Body
#### ISP
#### TSP
Injected bugs description
* CITY_BCAST_COUNT: MPI_Broadcast() that broadcasts the number of cities with wrong argument(count)
* CITY_BCAST_ROOT: MPI_Broadcast() that broadcasts the number of cities with wrong argument(root)
* POSX_BCAST_COUNT: MPI_Broadcast() that broadcasts the posx with wrong argument(count)
* POSX_BCAST_ROOT: MPI_Broadcast() that broadcasts the posx of cities with wrong argument(root)
* POSY_BCAST_COUNT: MPI_Broadcast() that broadcasts the posy of cities with wrong argument(count)
* POSY_BCAST_ROOT: MPI_Broadcast() that broadcasts the posy of cities with wrong argument(root)
* BYPASS_COMPUTE: This one is not a bug. It is a flag that bypass the computation loop.
* REDUCE_COUNT: MPI_Reduce() with wrong argument(count)
* REDUCE_ROOT: MPI_Reduce() with wrong argument(root)
#### Matmul



Benchmark | MPI | Fortran | C | C++ | Deterministic | Scalable | Complex Build System | Description |
----------|-----|---------|---|-----|---------------|----------|----------------------|-------------|
Sequoia AMG | * |   | * |   | y | y | n | Marquee performance code. Algebraic Mult-Grid linear system solver for unstructured mesh physics packages |
HPGMG | * |   | * |   | y | y | n | HPGMG-FV solves variable-coefficient elliptic problems (-b div beta grad u = f) on isotropic Cartesian grids using the finite volume method (FV) and Full Multigrid (FMG)|








