# Spectral Clustering Project

This project implements the **Spectral Clustering Algorithm** as described in the paper ["On Spectral Clustering: Analysis and an Algorithm"](https://papers.nips.cc/paper/2001/file/801272eea220b21e2a7f42dbb021e63c-Paper.pdf) by Ng, Jordan, and Weiss. The algorithm clusters nodes in a graph by leveraging eigenvectors of the Laplacian matrix to partition datasets effectively.

## Features
- Implementation of spectral clustering for two datasets:
  - **`example1.dat`**: A real-world dataset on medical innovation.
  - **`example2.dat`**: A synthetic dataset.
- Visualization of clustered graphs for each dataset.
- Tools to compute adjacency, degree, and Laplacian matrices.

---

## Tools and Libraries Used
- **Python 3.x**
- **Libraries:**
  - `numpy`: For matrix operations.
  - `scipy`: For eigenvalue decomposition.
  - `matplotlib`: For graph visualization.
  - `networkx`: For handling graph structures.
  - `scikit-learn`: For K-Means clustering.

---

## How to Run the Project

### Prerequisites
1. Install Python 3.x.
2. Install the required libraries using `pip`:
   ```bash
   pip install numpy scipy matplotlib networkx scikit-learn
