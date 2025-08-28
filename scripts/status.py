from scripts.helper import find_working_repo, cal_hash
import os
def status():
    working_repo = find_working_repo()
    index_path = os.path.join(working_repo, ".sjy", "index")
    with open(index_path, 'r', encoding="utf-8") as index_file:
        import csv
        reader = csv.reader(index_file)
        index_data = list(reader)
    modified_files = []
    tracked_files = []
    untracked_files = []
    for file, hash in index_data:
        abs_path = os.path.join(working_repo, file)
        if os.path.exists(abs_path):
            current_hash = cal_hash(abs_path)
            if current_hash != hash:
                modified_files.append(file)
            else:
                tracked_files.append(file)
        else:
            modified_files.append(file + " (deleted)")
    for root, dirs, files in os.walk(working_repo):
        if '.sjy' in dirs:
            dirs.remove('.sjy')
        for name in files:
            abs_path = os.path.join(root, name)
            rel_path = os.path.relpath(abs_path, working_repo)
            for file, hash in index_data:
                if rel_path == file:
                    break
            else:
                untracked_files.append(rel_path)
    print("\033[33m Modified files: \033[0m")
    for f in modified_files:
        print(f"  \033[31m {f} \033[0m")
    print("\033[32m Tracked files: \033[0m")
    for f in tracked_files:
        print(f"  \033[32m {f} \033[0m")
    print("\033[34m Untracked files: \033[0m")
    for f in untracked_files:
        print(f"  \033[34m {f} \033[0m")