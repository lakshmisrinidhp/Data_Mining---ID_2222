from shingling import Shingling
from minhashing import MinHashing
from compare_sets import CompareSets
from compare_signatures import CompareSignatures
from lsh import LSH
import os

def main():
    # Initialize components with adjusted parameters
    shingler = Shingling(k=10)
    minhasher = MinHashing(num_hashes=100)
    lsh = LSH(num_bands=5, rows_per_band=20)  # Adjusted LSH parameters for potential increased matches

    data_path = 'data/'
    signatures = {}
    shingles = {}
    doc_names = []

    # Step 1: Generate shingles for each document
    print("Generating shingles for each document...")
    for filename in os.listdir(data_path):
        filepath = os.path.join(data_path, filename)
        doc_shingles = shingler.process_document(filepath)
        shingles[filename] = doc_shingles
        doc_names.append(filename)
        print(f"{filename} - Number of shingles: {len(doc_shingles)}")

    # Step 2: Calculate Jaccard Similarity between each document pair
    print("\nJaccard Similarity between documents:")
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            doc1, doc2 = doc_names[i], doc_names[j]
            similarity = CompareSets.jaccard_similarity(shingles[doc1], shingles[doc2])
            print(f"Jaccard Similarity between {doc1} and {doc2}: {similarity:.4f}")

    # Step 3: Generate MinHash signatures for each document
    print("\nGenerating MinHash signatures for each document...")
    for doc_id, doc_shingles in shingles.items():
        signature = minhasher.minhash_signature(doc_shingles)
        signatures[doc_id] = signature
        lsh.lsh_banding(signature, doc_id)
        print(f"{doc_id} - MinHash signature generated.")

    # Step 4: Calculate Signature-Based Similarity between document pairs
    print("\nSignature Similarity between documents:")
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            doc1, doc2 = doc_names[i], doc_names[j]
            similarity = CompareSignatures.signature_similarity(signatures[doc1], signatures[doc2])
            print(f"Signature Similarity between {doc1} and {doc2}: {similarity:.4f}")

    # Step 5: Find Candidate Pairs using LSH
    candidate_pairs = lsh.get_candidate_pairs()
    print("\nCandidate Pairs from LSH:")
    if candidate_pairs:
        for pair in candidate_pairs:
            print(pair)
    else:
        print("No candidate pairs found by LSH.")

    # Step 6: Calculate Similarity for Candidate Pairs
    if candidate_pairs:
        print("\nEstimated Similarities for Candidate Pairs:")
        for (doc1, doc2) in candidate_pairs:
            similarity = CompareSignatures.signature_similarity(signatures[doc1], signatures[doc2])
            print(f"Similarity between {doc1} and {doc2}: {similarity:.4f}")
    else:
        print("No candidate pairs to calculate similarity for.")

if __name__ == "__main__":
    main()
