# Procedure
1. Setup gap
    - Follow the instructions in `gapbs/changes.md`
2. Setup valgrind
    - Follow procedure in `valgrind-local/setup.md`
3. BBV output file generation
    - General template is `valgrind --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/<file_name>.out <command to run on valgrind>`
    - Exact command ran: `valgrind --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/pr-twitter.out ./gapbs/pr -f ./gapbs/benchmark/graphs/twitter.sg -i1000 -t1e-4 -n16`
    - Ran with nohup, not sure of execution time, but larger than 30 minutes