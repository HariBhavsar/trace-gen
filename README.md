# Procedure
1. Setup gap
    - Follow the instructions in `gapbs/changes.md`
2. Setup valgrind
    - Follow procedure in `valgrind-local/setup.md`
3. BBV output file generation
    - General template is `valgrind --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/<file_name>.out <command to run on valgrind>`
    - Exact command ran: `export OMP_NUM_THREADS=1 && valgrind --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/pr-twitter/pr-twitter.out ./gapbs/pr -f ./gapbs/benchmark/graphs/twitter.sg -i1000 -t1e-4 -n2 && export OMP_NUM_THREADS=96`
        - Note, changed from n16 to n2, might be worth it to do n4 or n8 tbh
    - Ran with nohup, not sure of execution time, but larger than 30 minutes
        - Completed overnight
4. SimPoint
    - Follow procedure in `Simpoint/setup.md`
    - Run the `gen-simpoint-from-bbv.sh` script (< 1 min)
    - Observations
        - With 120 maxK, got decent ish output
5. Tracer
    - Follow instructions in `intel-pintool/procedure.md`
    - General command is `$PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o [TRACE_FILE_NAME] -s [FAST_FORWARD_INSTRUCTIONS] [INTERVAL_SIZE] -- [PROGRAM_FILE] [BENCHMARK_FILE] && xz [TRACE_FILE_NAME] &`
        - Exact command: `export OMP_NUM_THREADS=1 && $PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o pr-twitter-1.trace -s 80400000000 -t 300000000 -- ./gapbs/pr -f ./gapbs/benchmark/graphs/twitter.sg -i1000 -t1e-4 -n2 && xz pr-twitter-1.trace && export OMP_NUM_THREADS=96`
# Errors
1. Currently, ran `pr` in multithreaded mode. This is wrong, since we want only one `.out` file to be generated. Therefore, will push everything to git, then prune out everything and re-run.