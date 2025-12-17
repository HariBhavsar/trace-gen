# Champsim Trace Generation
## What is a champsim trace?
- It is a record of a sequence of instructions executed by a program
- Champsim does not directly execute the binary of a program, instead it executes trace files of the binary
- Traces are not arbitarily taken from random points inside the program's execution
    - Because arbitary points may not be representative of the program's workload
- Therefore, traces are taken at decisive **simulation points** inside the program's instruction stream
- These simulation points more or less represent the program
## Requirements
1. Valgrind
    - You will need to setup the `valgrind` tool to generate champsim traces
    - Follow the instructions in `valgrind-local/setup.md`
2. SimPoint
    - The `SimPoint` tool helps in identifying good representative simulation points
    - Follow the instructions in `Simpoint/setup.md`
3. Intel Pintool
    - The intel pintool is responsible for generating the traces
    - Follow the instructions in `intel-pintool/procedure.md`
4. Champsim
    - Champsim's tracer is required to generate champsim traces
    - Once you have your Champsim directory installed, go to the `tracer/pin` folder
    - Then run `make PIN_ROOT=$PIN_ROOT`
    - Go back to the base champsim directory and do `export CHAMPSIM_ROOT=$(pwd)`
## Generating a champsim trace for an arbitary program
For an arbitary program, generating a (good) champsim trace consists of the following steps:
1. BBV file generation:
    - A Basic Block is a sequence of instructions with a precise entry point and exit point, that is, the first and last instruction in the sequence are explicitly defined
    - A Basic Block Vector (BBV) is a high dimensional vector that counts how many times each basic block was executed during a specific interval
    - BBVs more representative of the program state will have higher **weight**, that is, they will be executed more number of times
    - BBV file generation is a **slow** step, since it requires execution of the program
    - BBV file generation **must** be done for a single-threaded program, if your program is multi-threaded, modify it so that it becomes single-threaded 
    - We use the `valgrind` tool to generate BBV files, the exact command is `valgrind --tool=exp-bbv --interval-size=<interval size> --bb-out-file=BBVs/<file_name>.out <command to run program>`
    - The interval size should be *at least* as large as the sum of the number of warmup and simulation instructions you plan to execute on champsim
2. Obtaining good simpoints:
    - Good simpoints are representative of the program while containing a small fraction of the instructions
    - *K-Means clustering* is used to *cluster* BBVs which have similar program execution
    - Therefore, simpoints are a function of `maxK` which is defined as the maximum number of clusters
        - Higher values of `maxK` imply the clustering is done at a finer granularity and higher quality
        - Lower values imply lesser quality and that different BBVs may be clustered together
    - Each cluster is given a representative interval and a weight
        - The representative interval is chosen as the one which is most similar to other intervals in the same cluster
        - The weight represents fraction of program execution that this particular cluster can account for
    - Thus, clusters with higher weight are more important
    - Obtaining good simpoints from `BBV` files is a **fast** step
    - We use the `SimPoint` tool for identifying good simulation points
    - The exact command to run is `./Simpoint/SimPoint.3.2/bin/simpoint -loadFVFile ./BBVs/<file_name>.out -maxK <maxK value> -saveSimpoints ./Simpoint/Storage/Simpoints/<file_name>-<maxK value>K.simpoints -saveSimpointWeights ./Simpoint/Storage/SimpointWeights/<file_name>-<maxK value>K.weights`
        - The `.simpoints` files consist of lines that look like `<representative interval> <SPACE> <cluster ID>`
        - The `.weights` files consist of lines that look like `<weight> <SPACE> <cluster ID>`
        - The clusters having higher weights are more important and the representative interval denotes the start of the interval that represents that particular cluster
3. Generating the trace file:
    - Generating the trace files is a **slow** step
    - Generating the trace files must be done on a single-threaded program, if your program is multi-threaded, modify it so that it becomes single-threaded
    - Theoretically, we should be generating a trace file for every cluster
    - Practically, that will be too many simulations to run on champsim
    - Therefore, we opt to select clusters having larger weights
    - The general goal is to select around 2-3 traces per program
    - Ideally, you will select 2-3 clusters with weights higher than 0.1, obtained at a `maxK` value of around 120
        - If all your clusters have weights < 0.1, you can either decrease the `maxK` value or decrease the threshold to something like 0.5
        - For the sake of this project, I have ensured that only clusters having weight of at least 0.045 are selected
        - If you have too many clusters with weights beyond 0.1, you should increase the weight threshold or decrease the `maxK` value
        - Decreasing the `maxK` value causes decrease in quality since less clustering occurs but it also means that fewer clusters are formed and with higher weights
    - Once you have selected a cluster, obtain the `representative interval` corresponding to that cluster
    - Then find the number of instructions to skip (`FAST_FORWARD_INSTRUCTIONS`) as `FAST_FORWARD_INSTRUCTIONS = representative interval * interval size`
    - Finally, check once that the `$PIN_ROOT` and `$CHAMPSIM_ROOT` environment variables are set, you can do this by running `echo $PIN_ROOT` and `echo $CHAMPSIM_ROOT` inside your terminal and checking that the output directory is valid
    - Run the following command to generate the trace:
        `$PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o [TRACE_FILE_NAME] -s [FAST_FORWARD_INSTRUCTIONS] [INTERVAL_SIZE] -- [PROGRAM] && xz [TRACE_FILE_NAME]`
## Generating trace files for GAP benchmark suite
### Setup
1. GAP
    - First we need to install and setup the gap benchmark suite
    - Follow the instructions in `gapbs/changes.md/Procedure`
2. Tracing tools
    - These tools will help us generate the traces and BBV files
    - Follow the instructions in this `README.md/Requirements`
3. Python (Optional)
    - This directory contains several scripts which automate the tedious trace generation process
    - These scripts are written in python, so python is an optional dependency
### Simpoint and Weight file generation
- We have given you a python script `generate_bbv.py`, which can be run by `python3 generate_bbv.py <algo> <graph>`, it will generate the simpoint and weight files
- We generate simpoints and weights for `maxK` values of 30, 60 and 120
- We use an interval size of 300 million
- GAP is multi-threaded by default and uses the `OpenMP` library to do multi-threading, we can make it single-threaded by setting the `OMP_NUM_THREADS` environment variable to 1
- The `generate_bbv.py` file first runs the target algorithm on the graph through valgrind and generates the corresponding BBVs
- Then, it generates the simpoints and weights for the three different `maxK` values
### Trace generation
- We have given you a python script `get-trace-from-simpoint.py`, which can be run by `python3 get-trace-from-simpoint.py <algo> <graph>`, it will generate trace files
- The nomenclature of the generated trace files will be `<algo>-<graph>-<skipped-ins>.trace.xz` where `skipped-ins` is the number of instructions skipped, divided by 100 million, to generate the trace
- It first generates a dictionary from cluster ID to weight and one from cluster ID to representative interval
- Then, it starts by assuming a weight threshold of 0.045 and `maxK` value of 120
- If it finds between 1 and 3 clusters generated with the given maxK and threshold values, it stops
- If there are too many clusters, the threshold is doubled
- If there are too few clusters, the `maxK` value is decreased, first to 60 and then to 30 and threshold is reset
- If no clusters are ever found, an error is thrown
- Once we have the clusters, we obtain the representative intervals, which also gives us the `FAST_FORWARD_INSTRUCTIONS` by multiplying the representative intervals by 300 million
- Finally, once we have the `FAST_FORWARD_INSTRUCTIONS`, we begin generating the trace files using the aforementioned command