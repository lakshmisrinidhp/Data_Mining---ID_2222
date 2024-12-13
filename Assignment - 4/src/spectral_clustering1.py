import numpy as np
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

# Step 1: Load and Parse the Dataset
def load_edges(file_path, weighted=False):
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
    A = np.zeros((n_nodes, n_nodes))
    for node1, node2 in edges:
        A[node1 - 1, node2 - 1] = 1
        A[node2 - 1, node1 - 1] = 1  # For undirected graphs
    return A


# Step 3: Create Degree Matrix
def create_degree_matrix(A):
    degrees = np.sum(A, axis=1)
    return np.diag(degrees)


# Step 4: Create Laplacian Matrix
def create_laplacian_matrix(D, A):
    return D - A


# Step 5: Perform Spectral Clustering
def spectral_clustering(L, k):
    eigvals, eigvecs = eigh(L)
    eigvecs_k = eigvecs[:, 1:k+1]  # Use the first k eigenvectors (excluding λ=0)
    row_norms = np.linalg.norm(eigvecs_k, axis=1, keepdims=True)
    row_norms[row_norms == 0] = 1e-10  # Avoid division by zero
    eigvecs_k = eigvecs_k / row_norms
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(eigvecs_k)
    return labels


# Step 6: Visualization Functions
def visualize_graph(edges, labels, n_nodes, output_file):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    color_map = [labels[node - 1] for node in range(1, n_nodes + 1)]
    nx.draw(G, pos, node_color=color_map, with_labels=True, cmap=plt.cm.rainbow)
    plt.savefig(output_file)
    plt.clf()  # Clear the figure


def plot_eigenvalues(eigenvalues, output_file):
    plt.figure()
    plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.title('Eigenvalue Gap')
    plt.savefig(output_file)
    plt.clf()


def plot_fiedler_vector(fiedler_vector, output_file):
    plt.figure()
    plt.scatter(range(len(fiedler_vector)), fiedler_vector, c='b', s=10)
    plt.xlabel('Node Index')
    plt.ylabel('Fiedler Vector Value')
    plt.title('Fiedler Vector')
    plt.savefig(output_file)
    plt.clf()


def plot_sparsity_pattern(matrix, output_file):
    plt.figure()
    plt.spy(matrix, markersize=1)
    plt.title('Sparsity Pattern')
    plt.savefig(output_file)
    plt.clf()


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
    k1 = 3  # Number of clusters for example1
    k2 = 4  # Number of clusters for example2
    labels1 = spectral_clustering(L1, k1)
    labels2 = spectral_clustering(L2, k2)

    # Save clustered graphs
    print("Clustering Results for example1.dat:", labels1)
    visualize_graph(edges1, labels1, n_nodes1, "output_graph_example1.png")

    print("Clustering Results for example2.dat:", labels2)
    visualize_graph(edges2, labels2, n_nodes2, "output_graph_example2.png")

    # Save eigenvalue gap plots
    eigenvalues1 = np.sort(eigh(L1, eigvals_only=True))
    plot_eigenvalues(eigenvalues1, "eigenvalues_example1.png")

    eigenvalues2 = np.sort(eigh(L2, eigvals_only=True))
    plot_eigenvalues(eigenvalues2, "eigenvalues_example2.png")

    # Save Fiedler vector plots
    fiedler_vector1 = eigh(L1, eigvals_only=False)[1][:, 1]
    plot_fiedler_vector(fiedler_vector1, "fiedler_vector_example1.png")

    fiedler_vector2 = eigh(L2, eigvals_only=False)[1][:, 1]
    plot_fiedler_vector(fiedler_vector2, "fiedler_vector_example2.png")

    # Save sparsity pattern plots
    plot_sparsity_pattern(L1, "sparsity_example1.png")
    plot_sparsity_pattern(L2, "sparsity_example2.png")
