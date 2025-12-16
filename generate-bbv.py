import sys
import os

def algo_to_command(algo, graph) -> str:
    if algo == "pr":
        return f"./gapbs/pr -f gapbs/benchmark/graphs/{graph}.sg -i1000 -t1e-4 -n2"
    elif algo == "sssp":
        if graph != "road":
            return f"./gapbs/sssp -f gapbs/benchmark/graphs/{graph}.sg -n64 -d2"
        else:
            return f"./gapbs/sssp -f gapbs/benchmark/graphs/{graph}.sg -n64 --d5000"
    elif algo == "tc":
        return f"./gapbs/tc -f gapbs/benchmark/graphs/{graph}.sg -n3"
    elif algo == "bc":
        return f"./gapbs/bc -f gapbs/benchmark/graphs/{graph}.sg -i4 -n16"
    elif algo == "cc":
        return f"./gapbs/cc -f gapbs/benchmark/graphs/{graph}.sg -n16"
    else:
        raise ValueError(f"Unknown algorithm: {algo}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-bbv.py <algo> <graph>")
        sys.exit(1)
    algo = sys.argv[1]
    graph = sys.argv[2]

    base_command = algo_to_command(algo, graph)

    # Need to run the base command through valgrind
    # export OMP_NUM_THREADS=1 && ./valgrind-local/valgrind-3.20.0/vg-in-place --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/{algo}-{graph}.out {base_command}
    final_command = f"export OMP_NUM_THREADS=1 && ./valgrind-local/valgrind-3.20.0/vg-in-place --tool=exp-bbv --interval-size=300000000 --bb-out-file=BBVs/{algo}-{graph}.out {base_command}"
    print("Executing the following command:")
    print(final_command)
    os.system(final_command)