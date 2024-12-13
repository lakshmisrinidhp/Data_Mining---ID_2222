import unittest
from src.apriori import apriori
from src.utils import load_dataset

class TestApriori(unittest.TestCase):
    def test_frequent_itemsets(self):
        transactions = [{1, 2}, {1, 2, 3}, {1, 3}, {2, 3}]
        min_support = 0.5
        frequent_itemsets = apriori(transactions, min_support)
        expected = [{1}, {2}, {3}, {1, 2}, {2, 3}]
        self.assertEqual(set(map(frozenset, frequent_itemsets)), set(map(frozenset, expected)))

    def test_dataset_loading(self):
        filepath = "../data/sample_data.dat"  # Replace with a small sample file
        transactions = load_dataset(filepath)
        self.assertIsInstance(transactions, list)
        self.assertGreater(len(transactions), 0)

if __name__ == "__main__":
    unittest.main()
