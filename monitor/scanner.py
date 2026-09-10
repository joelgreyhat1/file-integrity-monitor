import hashlib
import os

def hash_file(filepath):
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            # read in chunks so large files don't eat all your RAM :)
            while chunk := f.read(8192):
                md5.update(chunk)
                sha256.update(chunk)
        return {
            "md5": md5.hexdigest(),
            "sha256": sha256.hexdigest(),
        }
    except (PermissionError, OSError):
        return None


def scan_directory(directory):
    snapshot = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            hashes = hash_file(filepath)
            if hashes:
                # store relative path so the baseline is portable
                relative = os.path.relpath(filepath, directory)
                snapshot[relative] = hashes
    return snapshot