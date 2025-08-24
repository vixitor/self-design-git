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

def build_tree(working_repo, current_repo, tracked_files):
    tree = []
    for name in os.listdir(current_repo):
        if name == ".sjy":
            continue
        path = os.path.join(current_repo, name)
        rel_path = os.path.relpath(path, working_repo)
        if os.path.isdir(path):
            result = build_tree(working_repo, path)
            if result:
                tree.append(('tree', result, rel_path))
        else:
            for file, hash in tracked_files:
                if rel_path == file:
                    tree.append(('blob', hash, rel_path))
                    break
    if tree:
        tree.sort(key=lambda x: x[2])
        data = ''.join([f"{item[0]} {item[1]} {item[2]}\n" for item in tree]).encode('utf-8')
        import hashlib
        tree_hash = hashlib.sha1(data).hexdigest()
        objects_path = os.path.join(working_repo, ".sjy", "objects")
        dir_path = os.path.join(objects_path, tree_hash[:2])
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = os.path.join(dir_path, tree_hash[2:])
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(data)
        return tree_hash
    else :
        return None
