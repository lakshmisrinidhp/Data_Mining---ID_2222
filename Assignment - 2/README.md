# A-Priori Algorithm Implementation

## Overview

This project implements the A-Priori algorithm to discover frequent itemsets in a dataset of sales transactions based on a minimum support threshold (`s`). Additionally, it generates association rules for the discovered frequent itemsets with a specified confidence threshold (`c`).

The project includes:
- Frequent itemset discovery using the A-Priori algorithm.
- Association rule generation (optional task for extra credit).

## Features

1. **Frequent Itemset Discovery**:
   - Identifies itemsets with support ≥ `s`.
   - Saves frequent itemsets to output files.
   - Runtime analysis for varying support thresholds.

2. **Association Rule Generation**:
   - Generates rules between frequent itemsets with confidence ≥ `c`.
   - Saves rules to output files.

## Files

### Source Code
- `apriori.py`: Core implementation of the A-Priori algorithm.
- `utils.py`: Utility functions for data loading, support calculation, and more.
- `rule_generator.py`: Logic for association rule generation.

### Output Files
- `frequent_itemsets<support_threshold>.txt`: Frequent itemsets for a given support threshold.
- `association_rules<support_threshold>.txt`: Generated association rules for a given support threshold.

Example:
- `frequent_itemsets.txt`: Frequent itemsets for `s = 0.01`.
- `association_rules.txt`: Association rules for `s = 0.01`.

## How to Run

### Prerequisites
- Python .x
- Required libraries: `pandas`, `numpy` (if applicable)

### Steps
1. Clone the repository or copy the files to your local environment.
2. Run the script with the dataset:
   ```bash
   python src/apriori.py
