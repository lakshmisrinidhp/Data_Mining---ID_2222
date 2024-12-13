from utils import reservoir_sampling, count_wedges_and_closed_wedges, estimate_transitivity
import networkx as nx

def process_dataset(graph_file, reservoir_size, iterations=5):
    
    print(f"\nProcessing dataset: {graph_file}")
    
    # Load the graph dataset
    G = nx.read_edgelist(graph_file, nodetype=int, create_using=nx.Graph())
    edge_stream = list(G.edges())
    print(f"Loaded graph with {len(G.nodes())} nodes and {len(edge_stream)} edges.")

    # Store estimated transitivity values across iterations
    estimated_transitivity_values = []

    for i in range(iterations):
        print(f"\nIteration {i + 1}/{iterations}")
        
        # Perform reservoir sampling
        reservoir = reservoir_sampling(edge_stream, reservoir_size)
        print(f"Sampled {len(reservoir)} edges into the reservoir.")

        # Count wedges and closed wedges
        wedge_count, closed_wedge_count = count_wedges_and_closed_wedges(reservoir)
        print(f"Total wedges: {wedge_count}")
        print(f"Closed wedges (triangles): {closed_wedge_count}")

        # Estimate transitivity
        estimated_transitivity = estimate_transitivity(wedge_count, closed_wedge_count)
        estimated_transitivity_values.append(estimated_transitivity)
        print(f"Estimated Transitivity (Iteration {i + 1}): {estimated_transitivity}")

    # Compute the average estimated transitivity across iterations
    average_estimated_transitivity = sum(estimated_transitivity_values) / iterations
    print(f"\nAverage Estimated Transitivity: {average_estimated_transitivity}")

    # Compare with exact transitivity
    exact_transitivity = nx.transitivity(G)
    print(f"Exact Transitivity: {exact_transitivity}")
    print(f"Absolute Error: {abs(average_estimated_transitivity - exact_transitivity)}")
    print(f"Relative Error: {abs(average_estimated_transitivity - exact_transitivity) / exact_transitivity * 100:.2f}%")

def main():
    # List of datasets to process
    datasets = [
    "C:/Users/HP/desktop/SGA/datasets/facebook_combined.txt",
    "C:/Users/HP/desktop/SGA/datasets/email-Eu-core.txt"
]
    reservoir_sizes = [5000, 10000, 15000, 20000]  # Increase reservoir size for better accuracy
    iterations = 5         # Number of iterations to average results

    # Process each dataset
    for graph_file in datasets:
        for reservoir_size in reservoir_sizes:
            print(f"\nProcessing {graph_file} with reservoir size: {reservoir_size}")
            process_dataset(graph_file, reservoir_size, iterations)

if __name__ == "__main__":
    main()
