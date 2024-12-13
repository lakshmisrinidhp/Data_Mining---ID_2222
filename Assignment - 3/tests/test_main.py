import unittest
from utils import reservoir_sampling, count_wedges_and_closed_wedges, estimate_transitivity

class TestUtils(unittest.TestCase):
    def test_reservoir_sampling(self):
        """
        Test that the reservoir sampling function selects a fixed number of edges from the stream.
        """
        stream = [(1, 2), (2, 3), (3, 4), (4, 5)]
        k = 2
        reservoir = reservoir_sampling(stream, k)
        self.assertEqual(len(reservoir), k)
        for edge in reservoir:
            self.assertIn(edge, stream)

    def test_count_wedges_and_closed_wedges(self):
        """
        Test the wedge and closed wedge counting function.
        """
        reservoir = [(1, 2), (2, 3), (1, 3), (3, 4)]
        wedge_count, closed_wedge_count = count_wedges_and_closed_wedges(reservoir)
        
        # Expected wedges: (1-2-3), (2-3-4), (1-3-4)
        self.assertEqual(wedge_count, 3)
        # Expected closed wedges: (1-2-3)
        self.assertEqual(closed_wedge_count, 1)

    def test_estimate_transitivity(self):
        """
        Test the transitivity estimation function.
        """
        wedge_count = 6
        closed_wedge_count = 2
        transitivity = estimate_transitivity(wedge_count, closed_wedge_count)
        self.assertAlmostEqual(transitivity, 1.0)  # Expected transitivity: 1.0

        wedge_count = 0
        closed_wedge_count = 0
        transitivity = estimate_transitivity(wedge_count, closed_wedge_count)
        self.assertEqual(transitivity, 0.0)  # Edge case: No wedges, transitivity should be 0

if __name__ == "__main__":
    unittest.main()
