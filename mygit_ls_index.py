from helper import find_git_repo, read_index
import os

def main():
    root = find_git_repo(".")
    git_dir = os.path.join(root, ".git")
    if not git_dir:
        raise Exception("Not a git repository (or any of the parent directories): .git")
    index_path = os.path.join(git_dir, "index")
    if not os.path.exists(index_path):
        raise Exception(f"Index file '{index_path}' does not exist in the repository")
    print(f"git ls-index files: {index_path}")
    files = read_index(index_path)
    for file in files:
        print(f"{file.file_hash} {file.file_path}")