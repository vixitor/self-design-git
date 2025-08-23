import os
def find_working_repo():
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, '.sjy')):
        return current_dir
    parent_dir = os.path.dirname(current_dir)
    if parent_dir == current_dir:
        return None
    return find_working_repo(parent_dir)