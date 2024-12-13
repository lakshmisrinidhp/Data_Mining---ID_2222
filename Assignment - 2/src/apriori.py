import itertools
from multiprocessing import Pool
from utils import load_dataset, get_item_counts
from rule_generator import generate_rules

def apriori(transactions, min_support):
    """
    A-Priori algorithm for frequent itemset mining with multiprocessing support.
    """
    # Step 1: Count single items
    item_counts = get_item_counts(transactions)
    total_transactions = len(transactions)
    frequent_itemsets = [{item} for item, count in item_counts.items() if count / total_transactions >= min_support]

    results = []  # Store all frequent itemsets
    k = 1
    while frequent_itemsets:
        results.extend(frequent_itemsets)
        # Generate candidates of size k+1
        candidates = generate_candidates(frequent_itemsets, k + 1)
        # Count support for candidates using multiprocessing
        candidate_counts = count_candidates_parallel(candidates, transactions)
        # Filter frequent itemsets
        frequent_itemsets = [
            itemset for itemset, count in candidate_counts.items()
            if count / total_transactions >= min_support
        ]
        k += 1

    return results

def generate_candidates(itemsets, k):
    """
    Generate candidate k-itemsets from (k-1)-itemsets.
    """
    return [
        frozenset(a.union(b)) for a in itemsets for b in itemsets
        if len(a.union(b)) == k
    ]

def count_candidates_parallel(candidates, transactions):
    """
    Count the support of each candidate itemset in the transactions using multiprocessing.
    """
    pool = Pool()  # Use all available CPU cores
    chunks = divide_into_chunks(candidates, len(pool._pool))
    results = pool.starmap(count_candidates_chunk, [(chunk, transactions) for chunk in chunks])
    pool.close()
    pool.join()

    # Combine results from all chunks
    combined_counts = {}
    for result in results:
        for candidate, count in result.items():
            combined_counts[candidate] = combined_counts.get(candidate, 0) + count

    return combined_counts

def count_candidates_chunk(candidates_chunk, transactions):
    """
    Count support for a chunk of candidates.
    """
    counts = {candidate: 0 for candidate in candidates_chunk}
    for transaction in transactions:
        for candidate in candidates_chunk:
            if candidate.issubset(transaction):
                counts[candidate] += 1
    return counts

def divide_into_chunks(data, n):
    """
    Divide data into n roughly equal chunks.
    """
    chunk_size = len(data) // n + (len(data) % n > 0)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

if __name__ == "__main__":
    filepath = "./data/T10I4D100K.dat"
    transactions = load_dataset(filepath)
    min_support = 0.01   
    frequent_itemsets = apriori(transactions, min_support)

    # Validate and print support counts
    total_transactions = len(transactions)
    print("\nFrequent Itemsets with Support:")
    for itemset in frequent_itemsets:
        support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / total_transactions
        print(f"Itemset: {itemset}, Support: {support:.2f}")

    # Save sorted frequent itemsets to a file
    output_file = "./output/frequent_itemsets0_01.txt"
    sorted_itemsets = sorted(frequent_itemsets, key=lambda x: (len(x), x))
    with open(output_file, "w") as file:
        for itemset in sorted_itemsets:
            file.write(f"{itemset}\n")
    print(f"\nFrequent itemsets saved to {output_file}")

    # Generate and save association rules
    min_confidence = 0.6
    rules = generate_rules(frequent_itemsets, transactions, min_confidence)
    rules_file = "./output/association_rules0_01.txt"
    with open(rules_file, "w") as file:
        for antecedent, consequent, confidence in rules:
            file.write(f"Rule: {antecedent} -> {consequent}, Confidence: {confidence:.2f}\n")
    print(f"\nAssociation rules saved to {rules_file}")

    # Simplify output (filter 2-itemsets)
    filtered_itemsets = [itemset for itemset in frequent_itemsets if len(itemset) == 2]
    print(f"\nFiltered 2-Itemsets: {filtered_itemsets}")
    filtered_file = "./output/2_itemsets0_01.txt"
    with open(filtered_file, "w") as file:
        for itemset in filtered_itemsets:
            file.write(f"{itemset}\n")
    print(f"2-itemsets saved to {filtered_file}")
