# Champsim Trace Generation

## What is a Champsim Trace?
A Champsim trace is a record of a sequence of instructions executed by a program. Champsim does not directly execute the binary of a program; instead, it processes trace files of the binary. These traces are taken at decisive **simulation points** in the program's instruction stream to ensure they are representative of the program's workload.

## Requirements
To generate Champsim traces you will need the following tools and resources. The table below lists each tool, its purpose, and quick setup notes or links.

| Tool | Purpose | Notes / Setup |
|---|---|---|
| Valgrind | Generate BBV (Basic Block Vector) files | Required for BBV generation. See [valgrind-local/setup.md](valgrind-local/setup.md). Example: `valgrind --tool=exp-bbv --interval-size=<interval> --bb-out-file=BBVs/<file>.out <command>` |
| SimPoint | Identify representative simulation points (simpoints) | SimPoint performs K-means clustering on BBVs. See [Simpoint/setup.md](Simpoint/setup.md). Example: `./Simpoint/SimPoint.3.2/bin/simpoint -loadFVFile <fv> -maxK <K> -saveSimpoints <out.simpoints> -saveSimpointWeights <out.weights>` |
| Intel Pintool | Generate Champsim trace files (via Pintool) | The pintool drives trace generation. See [intel-pintool/procedure.md](intel-pintool/procedure.md). Ensure `PIN_ROOT` points to your pintool install. |
| Champsim tracer | Produce Champsim-compatible trace output | Build tracer: `cd $CHAMPSIM_ROOT/tracer/pin && make PIN_ROOT=$PIN_ROOT`. After building, set `CHAMPSIM_ROOT` in champsim root: `export CHAMPSIM_ROOT=$(pwd)` |
| Disk space | Storage for trace and intermediate files | Every instruction ≈ 64B raw. Example: 300 million instructions ≈ 17.88 GB raw (typically compressed to ≈245MB). Ensure ample disk space for BBVs and raw traces. |


## Generating a Champsim Trace for an Arbitrary Program

### 1. BBV File Generation
A **Basic Block Vector (BBV)** counts how many times each basic block is executed during specific intervals. This step is **slow** and must be done for single-threaded programs. Use the following command to generate BBV files:
```bash
valgrind --tool=exp-bbv --interval-size=<interval size> --bb-out-file=BBVs/<file_name>.out <command to run program>
```
- **Basic Block**: A sequence of instructions with a precise entry and exit point.
- **BBV**: A high-dimensional vector counting how many times each basic block was executed during a specific interval.
- **Interval Size**: Should be at least the sum of warmup and simulation instructions planned for Champsim.

### 2. Obtaining Good Simpoints
Good simpoints are representative of the program while containing a small fraction of instructions. Use the `SimPoint` tool to identify these points:
```bash
./Simpoint/SimPoint.3.2/bin/simpoint -loadFVFile ./BBVs/<file_name>.out -maxK <maxK value> -saveSimpoints ./Simpoint/Storage/Simpoints/<file_name>-<maxK value>K.simpoints -saveSimpointWeights ./Simpoint/Storage/SimpointWeights/<file_name>-<maxK value>K.weights
```
- **K-Means Clustering**: Used to group BBVs with similar program execution.
- **Representative Interval**: The interval most similar to others in the same cluster.
- **Weight**: Represents the fraction of program execution accounted for by the cluster.
- **Cluster Selection**: Choose clusters with higher weights (e.g., >0.1).

### Interpreting `.simpoints` and `.weights` files

- `.simpoints` file lines look like:
   ```text
   <representative_interval> <cluster_ID>
   ```
   - `representative_interval` is an integer index; multiply it by the BBV `interval size` to get the number of instructions to fast-forward.
   - `cluster_ID` matches the cluster labels in the corresponding `.weights` file.

- `.weights` file lines look like:
   ```text
   <weight> <cluster_ID>
   ```
   - `weight` is a floating-point fraction (sum of weights ≈ 1.0) that indicates how much of the program's execution that cluster represents.

- Example (toy):
   - `example.simpoints`:
      ```text
      100 0
      500 1
      900 2
      ```
   - `example.weights`:
      ```text
      0.45 0
      0.30 1
      0.25 2
      ```
   - Interpretation: cluster `0` corresponds to interval `100` and has weight `0.45`.

- Quick shell helpers:
   - List clusters with weight > 0.1:
      ```bash
      awk '$1>0.1 {print $0}' Simpoint/Storage/SimpointWeights/<file>-<K>K.weights
      ```
   - Show top-N clusters by weight:
      ```bash
      sort -nrk1 Simpoint/Storage/SimpointWeights/<file>-<K>K.weights | head -n 10
      ```
   - Map cluster IDs to representative intervals:
      ```bash
      awk '{interval[$2]=$1} END{for(id in interval) print id, interval[id]}' Simpoint/Storage/Simpoints/<file>-<K>K.simpoints
      ```

### If you don't find 2–3 clusters with weight > 0.1 at `maxK=120`

Follow this ordered strategy (used by `get-trace-from-simpoint.py`):

1. Lower `maxK`: try `60`, then `30` — merging clusters often increases individual cluster weights.
2. Reduce the selection threshold (e.g., from `0.1` to `0.05` or the repo default `0.045`) to allow more candidates.
3. If thresholding still fails, pick the top 2–3 clusters by weight:
    ```bash
    sort -nrk1 Simpoint/Storage/SimpointWeights/<file>-120K.weights | head -n 3
    ```
4. Use cumulative coverage: select the smallest set of clusters whose summed weights exceed a coverage target (e.g., 20–50%).
5. Prefer clusters that are stable across `maxK` values (appear at multiple K values or have similar representative intervals).
6. Optionally merge nearby representative intervals if they are redundant.
7. As a last resort, increase BBV `interval size` to produce fewer, more stable BBVs (this changes fidelity; use cautiously).

After selecting clusters, compute `FAST_FORWARD_INSTRUCTIONS`:
```
FAST_FORWARD_INSTRUCTIONS = representative_interval * interval_size
```


**About `maxK` (choices and tradeoffs):**
- `maxK` sets the maximum number of clusters for SimPoint's K-means clustering. Typical values used in this repository and in practice are `30`, `60`, and `120`.
- Tradeoffs:
   - `30` — coarse clustering: fewer representative intervals, faster SimPoint runs, useful for quick exploration or limited compute/disk.
   - `60` — medium granularity: a reasonable compromise between runtime and representativeness.
   - `120` — fine-grained clustering: usually yields higher-quality simpoints and more candidate intervals, but increases SimPoint runtime and the number of potential traces to generate.
- Practical guidance: if clusters have very small weights at high `maxK`, reduce `maxK` (to merge similar intervals into fewer, higher-weight clusters). If you need more coverage and have resources, use `120`.

### 3. Generating the Trace File
This step is **slow** and must be done for single-threaded programs. Select 2-3 clusters with weights >0.1 (or adjust thresholds). For each cluster:
1. Calculate `FAST_FORWARD_INSTRUCTIONS`:
   ```
   FAST_FORWARD_INSTRUCTIONS = representative interval * interval size
   ```
2. Ensure `$PIN_ROOT` and `$CHAMPSIM_ROOT` are set:
   ```bash
   echo $PIN_ROOT
   echo $CHAMPSIM_ROOT
   ```
3. Generate the trace:
   ```bash
   $PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o [TRACE_FILE_NAME] -s [FAST_FORWARD_INSTRUCTIONS] [INTERVAL_SIZE] -- [PROGRAM] && xz [TRACE_FILE_NAME]
   ```

## Generating Trace Files for GAP Benchmark Suite

### Setup
1. **GAP**
   - Install and set up the GAP benchmark suite.
   - Follow the instructions in [`gapbs/changes.md`](gapbs/changes.md).

2. **Tracing Tools**
   - Follow the setup instructions in the [Requirements](#requirements) section.

3. **Python (Optional)**
   - Python scripts automate trace generation.

### Simpoint and Weight File Generation
Use the `generate_bbv.py` script to generate simpoints and weights:
```bash
python3 generate_bbv.py <algo> <graph>
```
- Generates simpoints and weights for `maxK` values of 30, 60, and 120.
- Interval size: 300 million.
- Set GAP to single-threaded mode:
  ```bash
  export OMP_NUM_THREADS=1
  ```
- **Details**:
  - The script first runs the target algorithm on the graph through Valgrind to generate BBVs.
  - Then, it generates simpoints and weights for the specified `maxK` values.

**Why `30`, `60`, `120`?**
- The `generate_bbv.py` script runs SimPoint for these three `maxK` values to provide a sweep from coarse to fine clustering. Running multiple `maxK` values helps:
   - reveal representative intervals that might only appear at certain granularities,
   - allow comparison of cluster weights across granularities,
   - help choose stable, high-weight intervals for trace generation without blindly trusting a single clustering resolution.

### Trace Generation
Use the `get-trace-from-simpoint.py` script to generate trace files:
```bash
python3 get-trace-from-simpoint.py <algo> <graph>
```
- **Trace File Naming**: `<algo>-<graph>-<skipped-ins>.trace.xz`.
- **Process**:
  1. Generates dictionaries mapping cluster IDs to weights and representative intervals.
  2. Adjusts thresholds and `maxK` values to find 1-3 clusters.
  3. Calculates `FAST_FORWARD_INSTRUCTIONS`.
  4. Generates trace files using the calculated instructions.

### Additional Notes
- **Cluster Selection**:
  - Aim for clusters with weights >0.1 at `maxK=120`.
  - If weights are too low, decrease `maxK` or adjust the threshold.
  - If too many clusters are found, increase the threshold or decrease `maxK`.
- **Thresholds**:
  - Default: 0.045.
  - Adjust dynamically based on the number of clusters found.