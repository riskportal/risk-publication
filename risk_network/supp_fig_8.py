"""
risk_network/supp_fig_8
~~~~~~~~~~~~~~~~~~~~~~~
"""

import gc
import json
import os
import psutil
import time
import tracemalloc

import statistics

from risk import RISK


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


def benchmark_risk_workflow(
    file_path,
    annotations_content,
    stat_test="permutation",
    num_permutations=1000,
    max_workers=6,
    num_runs=5,
):
    """Benchmark the RISK workflow as a single block combining all operations.

    Args:
        file_path (str): Path to the network file (.gpickle).
        annotations_content (dict): Annotations content for the network.
        stat_test (str): The statistical test to perform. Defaults to "permutation".
        num_permutations (int): Number of permutations for the neighborhood computation. Defaults to 1000.
        max_workers (int): Number of workers for parallel computation. Defaults to 6.
        num_runs (int): Number of runs for averaging. Defaults to 5.

    Returns:
        dict: Benchmark metrics with averages and standard deviations.
    """
    # Initialize the RISK object
    risk = RISK(verbose=False)
    combined_metrics = []

    # Define the statistical test functions
    stat_test_funcs = {
        "binom": risk.load_neighborhoods_binom,
        "chi2": risk.load_neighborhoods_chi2,
        "hypergeom": risk.load_neighborhoods_hypergeom,
        "poisson": risk.load_neighborhoods_poisson,
        "zscore": risk.load_neighborhoods_zscore,
    }
    for _ in range(num_runs):

        def execute_workflow():
            """Execute the RISK workflow."""
            network = risk.load_network_gpickle(
                file_path,
                compute_sphere=False,
                surface_depth=0.0,
                min_edges_per_node=0,
            )
            annotation = risk.load_annotation_dict(
                network=network,
                content=annotations_content,
            )
            if stat_test == "permutation":
                return risk.load_neighborhoods_permutation(
                    network=network,
                    annotation=annotation,
                    distance_metric="louvain",
                    louvain_resolution=2,
                    fraction_shortest_edges=0.20,
                    score_metric="sum",
                    null_distribution="network",
                    num_permutations=num_permutations,
                    random_seed=887,
                    max_workers=max_workers,
                )

            stat_test_func = stat_test_funcs[stat_test]
            return stat_test_func(
                network=network,
                annotation=annotation,
                distance_metric="louvain",
                louvain_resolution=2,
                fraction_shortest_edges=0.20,
                null_distribution="network",
                random_seed=887,
            )

        # Measure the performance of the workflow
        _, workflow_metrics = measure_performance(execute_workflow)
        combined_metrics.append(workflow_metrics)

    def calculate_stats(metrics_list):
        """Calculate the average and standard deviation of the benchmark metrics.

        Args:
            metrics_list (list): List of benchmark metrics.

        Returns:
            dict: Dictionary with average and standard deviation of each metric.
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


def loop_and_benchmark_gpickle_files(
    gpickle_directory,
    json_output_directory,
    annotations_content,
    stat_test="permutation",
    num_permutations=1000,
    max_workers=6,
    num_runs=5,
):
    """Loop through all `.gpickle` files in a directory, benchmark them, and save the results to JSON files.

    Args:
        gpickle_directory (str): Directory containing the `.gpickle` files.
        json_output_directory (str): Directory to save the JSON benchmark results.
        annotations_content (dict): Annotations content for benchmarking.
        stat_test (str): The statistical test to perform. Defaults to "permutation".
        num_permutations (int): Number of permutations for the neighborhood computation. Defaults to 1000.
        max_workers (int): Number of workers for parallel computation. Defaults to 6.
        num_runs (int): Number of runs for averaging. Defaults to 5.
    """
    # Create the output directory if it does not exist
    os.makedirs(json_output_directory, exist_ok=True)
    # Sort the files by node count
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
            metrics = benchmark_risk_workflow(
                file_path=file_path,
                annotations_content=annotations_content,
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
    # Source benchmark files from risk_network/data directory
    gpickle_directory = "./data/gpickle/benchmark"
    json_output_directory = "./data/json/benchmark/risk"
    mock_go_bp = json.load(open("./data/json/benchmark/20250125_1000_mock_go_bp_annotations.json"))
    # Benchmark the RISK workflow
    loop_and_benchmark_gpickle_files(
        gpickle_directory=gpickle_directory,
        json_output_directory=json_output_directory,
        annotations_content=mock_go_bp,
        stat_test="hypergeom",
        num_permutations=1000,
        max_workers=3,
        num_runs=5,
    )
