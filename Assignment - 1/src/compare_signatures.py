class CompareSignatures:
    @staticmethod
    def signature_similarity(sig1, sig2):
        """Estimate similarity between two MinHash signatures."""
        matches = sum(1 for i in range(len(sig1)) if sig1[i] == sig2[i])
        return matches / len(sig1) if len(sig1) > 0 else 0.0
