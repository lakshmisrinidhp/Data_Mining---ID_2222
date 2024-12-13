from collections import Counter

def load_dataset(filepath):
    """
    Load the dataset from a file into a list of transactions.
    """
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transaction = set(map(int, line.strip().split()))
            transactions.append(transaction)
    return transactions

def get_item_counts(transactions):
    """
    Count the frequency of each item across all transactions.
    """
    item_counts = Counter()
    for transaction in transactions:
        item_counts.update(transaction)
    return item_counts
