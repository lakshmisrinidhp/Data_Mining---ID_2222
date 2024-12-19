# Ja-Be-Ja Graph Partitioning Algorithm

##  Brief Overview
This project implements the **Ja-Be-Ja algorithm**, a graph partitioning algorithm that minimizes edge cuts and balances partitions. The algorithm employs techniques like **simulated annealing**, **neighbor sampling**, and **randomized search** to optimize graph partitioning. An optional bonus implementation enhances the algorithm with advanced features like **probabilistic acceptance** and **exponential cooling**.

##  Tools and Technologies
- **Java**: Programming language for implementing the algorithm.
- **Maven**: Dependency management and build automation.
- **Gnuplot**: Command-line utility for graph visualization.
- **Bash**: Scripts for running the project and generating visualizations.

##  Features
1. **Original Implementation**:
   - Linear cooling function.
   - Strict partner selection based on benefit calculation.
   - Basic sampling strategies for node selection.
2. **Optional Bonus Implementation**:
   - Exponential cooling with periodic restarts.
   - Probabilistic acceptance of swaps to avoid local optima.
   - Improved sampling techniques for better performance.

##  How to Run the Project

### 1. **Setup Environment**
Ensure the following tools are installed:
- **Java Development Kit (JDK)** (version 8 or later)
- **Maven**
- **Gnuplot**

### 2. **Clone the Repository**
```bash
git clone <repository_url>
cd id2222-master
