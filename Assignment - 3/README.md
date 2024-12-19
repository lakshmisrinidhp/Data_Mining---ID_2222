# Streaming Graph Transitivity Estimation

## Project Overview
This project estimates the **transitivity** (clustering coefficient) of large graphs using a **streaming approach**. It employs **Reservoir Sampling** to sample edges from graph streams, enabling efficient analysis of graph properties such as wedges and triangles with minimal memory usage.

## Tools and Libraries Used
- **Python**: Programming language for implementation.
- **NetworkX**: Library for graph creation and analysis.
- **Random**: For probabilistic edge sampling.

## Main Components
1. **`main.py`**:
   - Coordinates the entire process.
   - Iteratively processes datasets with varying reservoir sizes to estimate transitivity.
2. **`utils.py`**:
   - Implements:
     - **Reservoir Sampling**: Randomly samples edges from the stream.
     - **Wedge and Triangle Counting**: Computes graph properties.
     - **Transitivity Estimation**: Calculates clustering coefficients.
3. **Datasets**:
   - Example graph datasets:
     - `facebook_combined.txt`
     - `email-Eu-core.txt`

## How to Run
1. **Install Dependencies**:
   - Ensure Python is installed.
   - Install required libraries:
     ```bash
     pip install networkx
     ```

2. **Prepare Directory Structure**:
   - Place your datasets in the `datasets/` folder.
   - Ensure the following structure:
     ```
     SGA/
     ├── code/
     │   ├── main.py
     │   ├── utils.py
     └── datasets/
         ├── facebook_combined.txt
         ├── email-Eu-core.txt
     ```

3. **Run the Program**:
   - Navigate to the `code` directory:
     ```bash
     cd code
     ```
   - Execute `main.py`:
     ```bash
     python main.py
     ```

4. **Output**:
   - The program will display:
     - Estimated transitivity for each dataset and reservoir size.
     - Comparison with the exact transitivity.
     - Absolute and relative errors.

