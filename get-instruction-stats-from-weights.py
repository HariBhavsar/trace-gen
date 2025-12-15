import os
import sys

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

if __name__ == '__main__':

    if (len(sys.argv) != 4):
        print("Invalid args, usage: python3 get-instruction-stats-from-weights.py <algo> <graph> <cluster>")
        sys.exit(1)
        
    # 1. Use .strip() on arguments to remove spaces/newlines
    algo = sys.argv[1].strip()
    graph = sys.argv[2].strip()
    cluster = sys.argv[3].strip()

    # 2. Define path components cleanly
    # Note: We are using "Simpoint/Storage" and relying on the OS to find it relative to the CWD
    BASE_DIR = "./Simpoint"
    SUB_DIR = "Storage"
    WEIGHTS_FOLDER = "SimpointWeights"
    SIMPOINTS_FOLDER = "Simpoints"
    
    filename_base = f"{algo}-{graph}-{cluster}"

    # 3. Use os.path.join to build the paths without manual slashes
    weight_file = os.path.join(BASE_DIR, SUB_DIR, WEIGHTS_FOLDER, f"{filename_base}.weights")
    simpoint_file = os.path.join(BASE_DIR, SUB_DIR, SIMPOINTS_FOLDER, f"{filename_base}.simpoints")

    # Add a final, ultimate strip on the constructed string just in case
    weight_file = weight_file.strip()
    simpoint_file = simpoint_file.strip()

    # Final check just before opening
    if not os.path.exists(weight_file):
        print(f"\nFATAL ERROR: os.path.exists check failed for: {weight_file}")
        sys.exit(1)
        
    try:
        with open(weight_file,"r") as f:
            weight_list = f.read()
        with open(simpoint_file, "r") as f:
            simpoint_list = f.read()
            
        cluster_to_weights = parse_simpoint_weights(weight_list)
        cluster_to_ins = parse_simpoint_weights(simpoint_list)
        simpoints = []
        for cluster, weights in cluster_to_weights.items():
            if cluster not in cluster_to_ins:
                print(f"Cluster: {cluster} not found in cluster-to-instructions list")
                sys.exit(1)
            if float(weights) > 0.045:
                simpoints.append(cluster_to_ins[cluster] * 300000000)
        print(simpoints)
        # ... (rest of the script logic) ...

    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: File not found. The path is almost certainly wrong.")
        print(f"Error details: {e}")
        print(f"Final calculated path: {weight_file}")
        sys.exit(1)

