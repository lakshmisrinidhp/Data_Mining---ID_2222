import random

class MinHashing:
    def __init__(self, num_hashes=100):
        self.num_hashes = num_hashes
        self.hash_functions = self._generate_hash_functions()
    
    def _generate_hash_functions(self):
        """Generate random hash functions for MinHashing."""
        max_shingle_id = 2**32 - 1
        random.seed(42)  # Ensures reproducibility
        hash_funcs = []
        for _ in range(self.num_hashes):
            a = random.randint(1, max_shingle_id)
            b = random.randint(0, max_shingle_id)
            hash_funcs.append((a, b))
        return hash_funcs

    def minhash_signature(self, shingle_set, max_shingle=2**32 - 1):
        """Generate a MinHash signature for the given shingle set."""
        signature = []
        for a, b in self.hash_functions:
            min_hash = min((a * int(shingle, 16) + b) % max_shingle for shingle in shingle_set)
            signature.append(min_hash)
        return signature
