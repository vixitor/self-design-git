import os

from scripts.helper import find_working_repo, build_tree
def commit(message):
    working_repo = find_working_repo()
    commit_data = []
    with open(os.path.join(working_repo, ".sjy", "index"), 'r', encoding="utf-8") as index_file:
        import csv
        reader = csv.reader(index_file)
        index_data = list(reader)
    tree_hash = build_tree(working_repo, working_repo, index_data)
    if tree_hash is None:
        print("\033[31m No changes added to commit \033[0m")
        return
    HEAD_path = os.path.join(working_repo, ".sjy", "HEAD")
    with open(HEAD_path, 'r', encoding="utf-8") as HEAD_file:
        last_commit = HEAD_file.read().strip()
    commit_data.append(last_commit)
    commit_data.append(tree_hash)
    commit_data.append(message)
    import hashlib
    data = '\n'.join(commit_data).encode('utf-8')
    commit_hash = hashlib.sha1(data).hexdigest()
    objects_path = os.path.join(working_repo, ".sjy", "objects")
    dir_path = os.path.join(objects_path, commit_hash[:2])
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = os.path.join(dir_path, commit_hash[2:])
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(data)
    with open(HEAD_path, 'w', encoding="utf-8") as HEAD_file:
        HEAD_file.write(commit_hash)
    print(f"\033[32m [{commit_hash}] {message} \033[0m")