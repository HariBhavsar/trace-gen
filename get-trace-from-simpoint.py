import os
import sys
from generate_bbv import algo_to_command
import subprocess

def parse_simpoint_weights(weights_data_string):
    """
    Parses a string containing SimPoint weights and cluster IDs.

    Args:
        weights_data_string (str): A multi-line string where each line
                                   contains the weight followed by the cluster ID,
                                   separated by whitespace.

    Returns:
        dict: A dictionary mapping cluster ID (int) to its weight (float).
    """
    simpoint_to_weight = {}
    
    # Split the input string into individual lines
    lines = weights_data_string.strip().split('\n')

    for line in lines:
        # Split each line by whitespace
        parts = line.split()
        
        if len(parts) == 2:
            try:
                # The weight is the first part (float)
                weight = float(parts[0])
                # The SimPoint/Cluster ID is the second part (int)
                cluster_id = int(parts[1])
                
                simpoint_to_weight[cluster_id] = weight
            except ValueError:
                # Handle cases where conversion to float or int fails
                print(f"Skipping malformed line: {line}")
                continue
    
    return simpoint_to_weight

def get_relevant_simpoints(algo, graph, cluster, threshold):
    BASE_DIR = "./Simpoint"
    SUB_DIR = "Storage"
    WEIGHTS_FOLDER = "SimpointWeights"
    SIMPOINTS_FOLDER = "Simpoints"
    
    filename_base = f"{algo}-{graph}-{cluster}"

    weight_file = os.path.join(BASE_DIR, SUB_DIR, WEIGHTS_FOLDER, f"{filename_base}.weights")
    simpoint_file = os.path.join(BASE_DIR, SUB_DIR, SIMPOINTS_FOLDER, f"{filename_base}.simpoints")

    with open(weight_file, 'r') as wf:
        weights_data = wf.read()
    
    simpoint_to_weight = parse_simpoint_weights(weights_data)

    with open(simpoint_file, 'r') as sf:
        simpoints_data = sf.read()
    
    simpoint_to_ins = parse_simpoint_weights(simpoints_data)
    relevant_simpoints = []
    for cluster, weight in simpoint_to_weight.items():
        if cluster in simpoint_to_ins:
            if float(weight) > threshold:
                bb_start = simpoint_to_ins[cluster]
                relevant_simpoints.append(int(bb_start) * 300000000)
        else:
            print(f"Cluster {cluster} not found in simpoint file.")
            sys.exit(1)
    return relevant_simpoints


# export OMP_NUM_THREADS=1 && $PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o pr-twitter-1.trace -s 80400000000 -t 300000000 -- ./gapbs/pr -f ./gapbs/benchmark/graphs/twitter.sg -i1000 -t1e-4 -n2 && xz pr-twitter-1.trace && export OMP_NUM_THREADS=96

def generate_trace_command(algo, graph, simpoint_ins) -> str:
    return f"export OMP_NUM_THREADS=1 && $PIN_ROOT/pin -t $CHAMPSIM_ROOT/tracer/pin/obj-intel64/champsim_tracer.so -o {algo}-{graph}-{int(simpoint_ins/100000000)}.trace -s {simpoint_ins} -t 300000000 -- {algo_to_command(algo, graph)} && xz {algo}-{graph}-{int(simpoint_ins/100000000)}.trace"

if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print("Invalid args, usage: python3 get-instruction-stats-from-weights.py <algo> <graph>")
        sys.exit(1)
        
    # 1. Use .strip() on arguments to remove spaces/newlines
    algo = sys.argv[1].strip()
    graph = sys.argv[2].strip()

    # Check from cluster = 120K then 60K then 30K then give error if not found
    cluster_list = ["120K", "60K", "30K"]
    found_cluster = False

    relevant_simpoints = []

    for cluster in cluster_list:
        threshold = 0.045
        simpoints = get_relevant_simpoints(algo, graph, cluster, threshold)
        while len(simpoints) > 3:
            threshold *= 2
            simpoints = get_relevant_simpoints(algo, graph, cluster, threshold)
        if len(simpoints) > 0 and len(simpoints) <= 3:
            print(f"Using cluster: {cluster} and threshold: {threshold} for algo: {algo}, graph: {graph}")
            print("Relevant Simpoints (in instructions):")
            found_cluster = True
            for sp in simpoints:
                relevant_simpoints.append(sp)
            break
    if not found_cluster:
        print(f"No relevant simpoints found for algo: {algo}, graph: {graph} in any cluster size.")
        sys.exit(1)
    print("Simpoints are:", relevant_simpoints)
    
    processes = []
    for simpoint in relevant_simpoints:
        command = generate_trace_command(algo, graph, simpoint)
        env = os.environ.copy()
        pin_root = os.environ.get("PIN_ROOT")
        champsim_root = os.environ.get("CHAMPSIM_ROOT")

        # 2. Check if they actually exist before proceeding
        if not pin_root or not champsim_root:
            raise EnvironmentError("Environment variables PIN_ROOT or CHAMPSIM_ROOT are not set. "
                                "Please run 'export PIN_ROOT=/path/to/pin' in your terminal first.")
        env["PIN_ROOT"] = pin_root
        env["CHAMPSIM_ROOT"] = champsim_root
        env["OMP_NUM_THREADS"] = "1"
        print("Executing command:", command)
        p = subprocess.Popen(command, shell=True, env=env)    
        processes.append(p)
    
    for p in processes:
        p.wait()