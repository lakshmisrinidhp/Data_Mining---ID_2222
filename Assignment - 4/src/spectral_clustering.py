import numpy as np
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

# Step 1: Load and Parse the Dataset
def load_edges(file_path, weighted=False):
    """
    Load edges from a dataset. Handles unweighted and weighted edge lists.
    :param file_path: Path to the dataset file
    :param weighted: If True, expects a third column for weights
    :return: List of edges, optionally with weights
    """
    edges = []
    weights = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            node1, node2 = int(values[0]), int(values[1])
            edges.append((node1, node2))
            if weighted and len(values) == 3:
                weights.append(float(values[2]))
    return (edges, weights) if weighted else edges


# Step 2: Create Adjacency Matrix
def create_adjacency_matrix(edges, n_nodes):
    """
    Create the adjacency matrix from the edge list.
    :param edges: List of edges (node1, node2)
    :param n_nodes: Total number of nodes in the graph
    :return: Adjacency matrix (numpy array)
    """
    A = np.zeros((n_nodes, n_nodes))
    for node1, node2 in edges:
        A[node1 - 1, node2 - 1] = 1
        A[node2 - 1, node1 - 1] = 1  # For undirected graphs
    return A


# Step 3: Create Degree Matrix
def create_degree_matrix(A):
    """
    Create the degree matrix from the adjacency matrix.
    :param A: Adjacency matrix
    :return: Degree matrix (numpy array)
    """
    degrees = np.sum(A, axis=1)
    return np.diag(degrees)


# Step 4: Create Laplacian Matrix
def create_laplacian_matrix(D, A):
    """
    Create the Laplacian matrix from the degree and adjacency matrices.
    :param D: Degree matrix
    :param A: Adjacency matrix
    :return: Laplacian matrix (numpy array)
    """
    return D - A


# Step 5: Normalize Cluster Labels
def normalize_labels(labels):
    """
    Normalize cluster labels to ensure consistent mapping of clusters to integers starting at 0.
    :param labels: Original cluster labels
    :return: Normalized cluster labels
    """
    unique_labels = np.unique(labels)
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    return [label_map[label] for label in labels]


# Step 6: Perform Spectral Clustering
def spectral_clustering(L, k):
    """
    Perform spectral clustering using the Laplacian matrix.
    :param L: Laplacian matrix
    :param k: Number of clusters
    :return: Normalized clustering labels
    """
    # Compute the eigenvalues and eigenvectors
    eigvals, eigvecs = eigh(L)
    # Use the first k eigenvectors (excluding the eigenvector for λ=0)
    eigvecs_k = eigvecs[:, 1:k+1]
    # Normalize rows (safeguard against division by zero)
    row_norms = np.linalg.norm(eigvecs_k, axis=1, keepdims=True)
    row_norms[row_norms == 0] = 1e-10  # Replace zeros with a small value
    eigvecs_k = eigvecs_k / row_norms
    # Apply k-means clustering on the eigenvector matrix
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = normalize_labels(kmeans.fit_predict(eigvecs_k))
    return normalize_labels(labels)  # Normalize labels


# Step 7: Visualize the Results
def visualize_graph(edges, labels, n_nodes, output_file):
    """
    Visualize the graph with clusters and save as an image.
    :param edges: List of edges
    :param labels: Normalized clustering labels
    :param n_nodes: Total number of nodes
    :param output_file: File path to save the graph
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    color_map = [labels[node - 1] for node in range(1, n_nodes + 1)]
    nx.draw(G, pos, node_color=color_map, with_labels=True, cmap=plt.cm.rainbow)
    plt.savefig(output_file)  # Save the graph as an image file
    plt.clf()  # Clear the figure to avoid overlapping plots


# Main Function
if __name__ == "__main__":
    # File paths for datasets
    file1_path = "../data/example1.dat"
    file2_path = "../data/example2.dat"

    # Load datasets
    edges1 = load_edges(file1_path)
    edges2 = load_edges(file2_path)

    # Determine the number of nodes
    n_nodes1 = max(max(e) for e in edges1)
    n_nodes2 = max(max(e) for e in edges2)

    # Create adjacency matrices
    A1 = create_adjacency_matrix(edges1, n_nodes1)
    A2 = create_adjacency_matrix(edges2, n_nodes2)

    # Create degree matrices
    D1 = create_degree_matrix(A1)
    D2 = create_degree_matrix(A2)

    # Create Laplacian matrices
    L1 = create_laplacian_matrix(D1, A1)
    L2 = create_laplacian_matrix(D2, A2)

    # Perform spectral clustering
    k1 = 4  # Number of clusters for example1
    k2 = 2  # Number of clusters for example2
    labels1 = spectral_clustering(L1, k1)
    labels2 = spectral_clustering(L2, k2)

    # Save visualizations as images
    print("Clustering Results for example1.dat:", labels1)
    visualize_graph(edges1, labels1, n_nodes1, "../output/output_graph_example1.png")

    print("Clustering Results for example2.dat:", labels2)
    visualize_graph(edges2, labels2, n_nodes2, "../output/output_graph_example2.png")
