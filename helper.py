import os

def find_git_dir(path):
    """
    Find the .git directory in the given path or its parent directories.
    Returns the path to the .git directory if found, otherwise None.
    """
    current_path = os.path.abspath(path)
    while current_path != os.path.dirname(current_path):  # Stop when reaching root
        git_dir = os.path.join(current_path, ".git")
        if os.path.isdir(git_dir):
            return git_dir
        current_path = os.path.dirname(current_path)
    return None
