import os
import hashlib

def find_git_repo(path):
    """
    Find the .git directory in the given path or its parent directories.
    Returns the path to the .git directory if found, otherwise None.
    """
    current_path = os.path.abspath(path)
    while current_path != os.path.dirname(current_path):  # Stop when reaching root
        git_dir = os.path.join(current_path, ".git")
        if os.path.isdir(git_dir):
            return current_path
        current_path = os.path.dirname(current_path)
    return None

def git_blob_sha1(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    size = len(data)
    header = f"blob {size}\0".encode("utf-8")
    full = header + data
    return hashlib.sha1(full).hexdigest()
