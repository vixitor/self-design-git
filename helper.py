import os
def find_working_repo():
    """如果找不到直接报错"""
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, '.sjy')):
        return os.path.abspath(current_dir)
    parent_dir = os.path.dirname(current_dir)
    if parent_dir == current_dir:
        print("\033[31m Not a sjy repository (or any of the parent directories) \033[0m")
        raise Exception("Not a sjy repository (or any of the parent directories)")
    return find_working_repo(parent_dir)

def cal_hash(file):
    import hashlib
    with open(file, 'rb') as f:
        content = f.read()
        sha1 = hashlib.sha1(content).hexdigest()
    return sha1