import hashlib

class Shingling:
    def __init__(self, k=10):
        self.k = k  # Length of each shingle (number of characters)

    def create_shingles(self, document):
        """Create shingles from a document and hash them."""
        shingles = set()
        for i in range(len(document) - self.k + 1):
            # Extract the k-length shingle
            shingle = document[i:i + self.k]
            # Hash the shingle and add to the set
            hashed_shingle = hashlib.md5(shingle.encode('utf-8')).hexdigest()
            shingles.add(hashed_shingle)
        return shingles

    def process_document(self, filepath):
        """Read a document from a file, create shingles, and return hashed shingles."""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            document = file.read().replace('\n', ' ')  # Combine lines into a single text block
        return self.create_shingles(document)
