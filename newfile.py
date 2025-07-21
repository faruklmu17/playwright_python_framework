import hashlib

#from something unrelated
def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    digest = sha256.hexdigest()
    print(f"[✓] SHA-256 hash: {digest}")
    return digest

