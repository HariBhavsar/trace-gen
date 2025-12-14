# Idea
- Need to generate traces of running `pr` on different graphs
- First try it with `twitter` graph
- Eventually, once we have a working version, try with other graphs
# Procedure
1. Ran `make` (~1 min)
2. Modified `bench.mk` by changing `GRAPHS = twitter web road kron urand` to `GRAPHS = twitter` (~0 min)
3. Ran `make bench-graphs` (~ 25/30 min)
# Twitter Characteristics and Output
- Graph has 61578415 nodes and 1468364884 directed edges for degree: 23
- Command to run pr: `./pr -f benchmark/graphs/twitter.sg -i1000 -t1e-4 -n16`
- Output:
```
bhavsar@ASPLOS:~/ISCA/trace-gen/gapbs> ./pr -f benchmark/graphs/twitter.sg -i1000 -t1e-4 -n16
Read Time:           7.29231
Graph has 61578415 nodes and 1468364884 directed edges for degree: 23
Trial Time:          49.19495
Trial Time:          35.44760
Trial Time:          20.28391
Trial Time:          20.37638
Trial Time:          19.86748
Trial Time:          20.36203
Trial Time:          20.13932
Trial Time:          19.95285
Trial Time:          19.98985
Trial Time:          19.91437
Trial Time:          20.17830
Trial Time:          20.09688
Trial Time:          20.13617
Trial Time:          20.10205
Trial Time:          20.09910
Trial Time:          20.10534
Average Time:        22.89041
```