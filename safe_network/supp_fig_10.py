"""
safe_network/supp_fig_10
~~~~~~~~~~~~~~~~~~~~~~~~
"""

import gc
import json
import os
import pickle
import psutil
import time
import tracemalloc

import networkx as nx
import statistics

from safepy import safe


def measure_performance(func, *args, **kwargs):
    """Measure the execution time, CPU time, and memory usage of a function.

    Args:
        func (callable): The function to measure.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        tuple: (result of the function, performance metrics dict)
    """
    # Start measuring performance
    start_time = time.time()
    process = psutil.Process()
    cpu_times_before = process.cpu_times()
    memory_before = process.memory_info().rss / (1024**2)  # Convert to MB
    # Start tracing memory
    tracemalloc.start()

    # Execute the function
    result = func(*args, **kwargs)
    # Stop tracing memory
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # End measuring performance
    end_time = time.time()
    cpu_times_after = process.cpu_times()
    memory_after = process.memory_info().rss / (1024**2)  # Convert to MB
    # Calculate performance metrics
    metrics = {
        "execution_time": end_time - start_time,
        "cpu_user_time": cpu_times_after.user - cpu_times_before.user,
        "cpu_system_time": cpu_times_after.system - cpu_times_before.system,
        "memory_usage": memory_after - memory_before,
        "peak_memory_usage": peak / (1024**2),  # Convert to MB
    }

    return result, metrics


def benchmark_safe_workflow(file_path, stat_test, num_permutations=1000, max_workers=6, num_runs=5):
    """Benchmark the SAFE workflow as a single block combining all operations.

    Args:
        file_path (str): Path to the network file (.gpickle).
        stat_test (str): The statistical test to apply. Defaults to "permutation".
        num_permutations (int): Number of permutations for the neighborhood computation. Defaults to 1000.
        max_workers (int): Number of workers for parallel computation. Defaults to 6.
        num_runs (int): Number of runs for averaging. Defaults to 5.

    Returns:
        dict: Benchmark metrics with averages and standard deviations.
    """
    # Make necessary adjustments to the network for compatibility with SAFE
    g_adj = shift_node_ids_left(read_gpickle(file_path))
    g_adj_file_path = f'./data/gpickle/benchmark/{file_path.split("/")[-1].replace(".gpickle", "_node_id_adj.gpickle")}'
    write_gpickle(g_adj, g_adj_file_path)

    # Initialize the SAFE object
    sf = safe.SAFE()
    combined_metrics = []

    # Run the workflow multiple times and collect performance metrics
    for _ in range(num_runs):

        def execute_workflow():
            """Execute the SAFE workflow."""
            sf.load_network(
                network_file=g_adj_file_path,
                node_key_attribute="label",
            )
            sf.background = "network"
            sf.load_attributes(
                attribute_file="./data/tar.gz/annotations/20250125_1000_mock_go_bp_annotations.tar.gz"
            )
            sf.define_neighborhoods(
                node_distance_metric="shortpath_weighted_layout", neighborhood_radius=0.20
            )
            if stat_test == "permutation":
                sf.enrichment_type = "permutation"
            else:
                sf.enrichment_type = "hypergeometric"

            sf.enrichment_threshold = 0.9999999
            sf.compute_pvalues(processes=max_workers, num_permutations=num_permutations)
            return sf

        _, workflow_metrics = measure_performance(execute_workflow)
        combined_metrics.append(workflow_metrics)

    def calculate_stats(metrics_list):
        """Calculate the average and standard deviation of performance metrics.

        Args:
            metrics_list (list): List of performance metrics dictionaries.
        """
        return {
            "avg_execution_time": statistics.mean([m["execution_time"] for m in metrics_list]),
            "stdev_execution_time": (
                statistics.stdev([m["execution_time"] for m in metrics_list]) if num_runs > 1 else 0
            ),
            "avg_cpu_user_time": statistics.mean([m["cpu_user_time"] for m in metrics_list]),
            "stdev_cpu_user_time": (
                statistics.stdev([m["cpu_user_time"] for m in metrics_list]) if num_runs > 1 else 0
            ),
            "avg_cpu_system_time": statistics.mean([m["cpu_system_time"] for m in metrics_list]),
            "stdev_cpu_system_time": (
                statistics.stdev([m["cpu_system_time"] for m in metrics_list])
                if num_runs > 1
                else 0
            ),
            "avg_memory_usage": statistics.mean([m["memory_usage"] for m in metrics_list]),
            "stdev_memory_usage": (
                statistics.stdev([m["memory_usage"] for m in metrics_list]) if num_runs > 1 else 0
            ),
            "avg_peak_memory_usage": statistics.mean(
                [m["peak_memory_usage"] for m in metrics_list]
            ),
            "stdev_peak_memory_usage": (
                statistics.stdev([m["peak_memory_usage"] for m in metrics_list])
                if num_runs > 1
                else 0
            ),
        }

    return calculate_stats(combined_metrics)


def write_json(data, file_path):
    """Write data to a JSON file.

    Args:
        data (dict): Data to write to the JSON file.
        file_path (str): Path to the JSON file.
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_gpickle(filepath):
    """Read a GPickle file.

    Args:
        filepath (str): Path to the GPickle file.
    """
    with open(filepath, "rb") as f:
        G = pickle.load(f)
    return G


def write_gpickle(graph, filepath):
    """Write network to a GPickle file.

    Args:
        graph (nx.Graph): NetworkX graph to write.
        filepath (str): Path to the output GPickle file.
    """
    with open(filepath, "wb") as file:
        pickle.dump(graph, file)


def shift_node_ids_left(graph):
    """Shift the node IDs of a NetworkX graph to start at 0 and assign the original IDs to a 'label' attribute.

    Parameters:
        graph (nx.Graph): The input NetworkX graph.

    Returns:
        nx.Graph: The updated NetworkX graph with shifted node IDs and 'label' attributes.
    """
    # Ensure the graph is a copy to avoid modifying the original
    graph = graph.copy()
    # Create a mapping of new node IDs (starting from 0) to the original node IDs
    original_ids = sorted(graph.nodes())
    mapping = {old: new for new, old in enumerate(original_ids)}
    # Create a new graph with shifted node IDs
    shifted_graph = nx.Graph() if graph.is_directed() is False else nx.DiGraph()
    # Relabel nodes and copy edges/attributes
    for old_id, new_id in mapping.items():
        # Add node with the new ID and the original ID as a 'label'
        shifted_graph.add_node(new_id, **graph.nodes[old_id], label=old_id)

    # Add edges with the updated node IDs
    for old_u, old_v, data in graph.edges(data=True):
        new_u, new_v = mapping[old_u], mapping[old_v]
        shifted_graph.add_edge(new_u, new_v, **data)

    return shifted_graph


def loop_and_benchmark_gpickle_files(
    gpickle_directory,
    json_output_directory,
    stat_test="permutation",
    num_permutations=1000,
    max_workers=6,
    num_runs=5,
):
    """Loop through all `.gpickle` files in a directory, benchmark them, and save the results to JSON files.

    Args:
        gpickle_directory (str): Directory containing the `.gpickle` files.
        json_output_directory (str): Directory to save the JSON benchmark results.
        stat_test (str): The statistical test to apply. Defaults to "permutation".
        num_permutations (int): Number of permutations for the neighborhood computation. Defaults to 1000.
        max_workers (int): Number of workers for parallel computation. Defaults to 6.
        num_runs (int): Number of runs for averaging. Defaults to 5.
    """
    # Create the output directory if it does not exist
    os.makedirs(json_output_directory, exist_ok=True)
    sorted_files = sorted(
        [
            (file_name, int(file_name.split("_")[4]))  # Extract node count from filename
            for file_name in os.listdir(gpickle_directory)
            if file_name.endswith(".gpickle")
        ],
        key=lambda x: x[1],
    )

    # Loop through the files and benchmark them
    for file_name, _ in sorted_files:
        file_path = os.path.join(gpickle_directory, file_name)
        base_name = os.path.splitext(file_name)[0]
        json_path = os.path.join(json_output_directory, f"{base_name}_benchmark.json")

        # Process the file
        print(f"Processing {file_name}...")
        try:
            metrics = benchmark_safe_workflow(
                file_path=file_path,
                stat_test=stat_test,
                num_permutations=num_permutations,
                max_workers=max_workers,
                num_runs=num_runs,
            )
            # Save the results to a JSON file
            write_json(metrics, json_path)
            print(f"Saved results to {json_path}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

        # Clean up
        del metrics
        gc.collect()


if __name__ == "__main__":
    # Source and store files in risk_network/data directory
    gpickle_directory = "../risk_network/data/gpickle/benchmark"
    json_output_directory = "../risk_network/data/json/benchmark/safe"
    # Benchmark the SAFE workflow
    loop_and_benchmark_gpickle_files(
        gpickle_directory=gpickle_directory,
        json_output_directory=json_output_directory,
        stat_test="hypergeom",
        num_permutations=1000,
        max_workers=3,
        num_runs=5,
    )
