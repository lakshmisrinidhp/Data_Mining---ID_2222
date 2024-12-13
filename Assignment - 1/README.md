# Data Mining Assignment: Finding Textually Similar Documents

## Description

This project demonstrates the process of identifying textually similar documents using advanced techniques:
- **Shingling**: Converts documents into sets of unique k-shingles.
- **Jaccard Similarity**: Calculates similarity based on shared shingles between documents.
- **MinHashing**: Generates compact representations (signatures) for efficient similarity computation.
- **Locality-Sensitive Hashing (LSH)**: Groups documents into candidate pairs likely to be similar.

The program is designed to handle text datasets and provide efficient approximate similarity detection.

---

## Requirements

To execute this project, ensure the following are installed:
- **Python**: Version 3.7 or above.
- **Python Libraries**: Listed in `requirements.txt`.

Install the dependencies with:
```bash
pip install -r requirements.txt
