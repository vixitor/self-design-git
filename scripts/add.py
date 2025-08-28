import os.path
import csv
from scripts.helper import find_working_repo, cal_hash


def add(file):
    working_repo = find_working_repo()
    if not os.path.exists(file):
        index_path = os.path.join(working_repo, ".sjy", "index")
        with open(index_path, 'r',encoding="utf-8") as index_file:
            reader = csv.reader(index_file)
            data = list(reader)
        for i, row in enumerate(data):
            if row[0] == os.path.relpath(file, working_repo):
                del data[i]
                print("\033[32m File removed from index \033[0m")
                break
        with open(index_path, 'w', newline='',encoding="utf-8") as index_file:
            writer = csv.writer(index_file)
            writer.writerows(data)
        return

    rel_path = os.path.relpath(file, working_repo)
    hash = cal_hash(file)
    obj_path = os.path.join(working_repo, ".sjy", "objects")
    dir_path = os.path.join(obj_path, hash[:2])
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = os.path.join(dir_path, hash[2:])
    if os.path.exists(file_path):
        print("\033[33m File already added \033[0m")
    else :
        with open(file, 'rb') as f_src:
            with open(file_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
    index_path = os.path.join(working_repo, ".sjy", "index")
    with open(index_path, 'r',encoding="utf-8") as index_file:
        reader = csv.reader(index_file)
        data = list(reader)
        for row in data:
            if row[0] == rel_path:
                if row[1] == hash:
                    print("\033[33m File already added and not modified\033[0m")
                else:
                    row[1] = hash
                    print("\033[32m File updated in index \033[0m")
                break
        else:
            data.append([rel_path, hash])
            print("\033[32m File added to index \033[0m")
            data.sort(key=lambda x: x[0])
    with open(index_path, 'w', newline='',encoding="utf-8") as index_file:
        writer = csv.writer(index_file)
        writer.writerows(data)