import itertools

def generate_rules(frequent_itemsets, transactions, min_confidence):
    """
    Generate association rules from frequent itemsets.
    """
    total_transactions = len(transactions)
    rules = []

    for itemset in frequent_itemsets:
        if len(itemset) < 2:  # Skip itemsets that can't form rules
            continue
        for subset in map(set, itertools.chain.from_iterable(itertools.combinations(itemset, r) for r in range(1, len(itemset)))):
            confidence = count_support(itemset, transactions) / count_support(subset, transactions)
            if confidence >= min_confidence:
                rules.append((subset, itemset - subset, confidence))

    return rules

def count_support(itemset, transactions):
    """
    Count the support of an itemset in the transactions.
    """
    return sum(1 for transaction in transactions if itemset.issubset(transaction))
