from scripts.helper import find_working_repo, update_index
import os
def checkout(commit_id):
    working_repo = find_working_repo()
    HEAD_path = os.path.join(working_repo, ".sjy", "HEAD")
    with open(HEAD_path, 'w', encoding="utf-8") as HEAD_file:
        HEAD_file.write(commit_id)
    print(f"\033[32m Switched to commit {commit_id} \033[0m")
    commit_path = os.path.join(working_repo, ".sjy", "objects", commit_id[:2], commit_id[2:])
    with open(commit_path, 'rb') as commit_file:
        data = commit_file.read().decode('utf-8').split('\n')
        tree_hash = data[1]
    data = update_index(working_repo, tree_hash)
    data.sort(key=lambda x: x[0])
    index_path = os.path.join(working_repo, ".sjy", "index")
    with open(index_path, 'w', newline='', encoding="utf-8") as index_file:
        import csv
        writer = csv.writer(index_file)
        writer.writerows(data)
    print(f"\033[32m Index updated to commit {commit_id} \033[0m")
    for root, dirs, files in os.walk(working_repo):
        if '.sjy' in dirs:
            dirs.remove('.sjy')
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, working_repo)
            for tracked_file, hash in data:
                if rel_path == tracked_file:
                    obj_path = os.path.join(working_repo, ".sjy", "objects", hash[:2], hash[2:])
                    with open(obj_path, 'rb') as f_src:
                        with open(file_path, 'wb') as f_dst:
                            f_dst.write(f_src.read())
                    print(f"{rel_path} restored")
                    break
            else:
                os.remove(file_path)
    for file, hash in data:
        file_path = os.path.join(working_repo, file)
        if not os.path.exists(file_path):
            obj_path = os.path.join(working_repo, ".sjy", "objects", hash[:2], hash[2:])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(obj_path, 'rb') as f_src:
                with open(file_path, 'wb') as f_dst:
                    f_dst.write(f_src.read())
            print(f"{file} restored")