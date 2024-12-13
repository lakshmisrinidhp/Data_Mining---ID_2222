class CompareSets:
    @staticmethod
    def jaccard_similarity(set1, set2):
        """Compute Jaccard Similarity between two sets."""
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0.0
