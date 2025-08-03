import os.path

from helper import find_git_repo, read_index, TrackedFile, build_tree


def main(message):
    print("Committing changes with message:", message)
    git_repo = find_git_repo(".")
    git_dir = os.path.join(git_repo, ".git")
    index_path = os.path.join(git_dir, "index")
    cached_files = read_index(index_path)
    if not cached_files:
        raise Exception("No files to commit. Use 'git add <file>' to stage files for commit.")
    print(f"Cached files: {cached_files}")
    build_tree(git_repo, cached_files, git_repo)