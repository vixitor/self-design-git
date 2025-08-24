from scripts.helper import find_working_repo
import os
def log():
    working_repo = find_working_repo()
    HEAD_path = os.path.join(working_repo, ".sjy", "HEAD")
    with open(HEAD_path, 'r', encoding="utf-8") as HEAD_file:
        commit_hash = HEAD_file.read().strip()
        while commit_hash:
            commit_path = os.path.join(working_repo, ".sjy", "objects", commit_hash[:2], commit_hash[2:])
            with open(commit_path, 'rb') as commit_file:
                data = commit_file.read().decode('utf-8').split('\n')
                parent_hash = data[0]
                message = data[2]
                print(f"\033[32m [{commit_hash}] {message} \033[0m")
                commit_hash = parent_hash