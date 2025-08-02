import os
from helper import git_blob_sha1
def main(git_dir, files):
    for file in files:
        sha1 = git_blob_sha1(file)

        objects_dir = os.path.join(git_dir, "objects")

        object_file = os.path.join(objects_dir, sha1[:2], sha1[2:])
        os.makedirs(os.path.dirname(object_file), exist_ok=True)
        print(f"object_file: {object_file}")
        with open(object_file, 'wb') as f:
            f.write(sha1.encode('utf-8'))

        print(f"Added {file} to the index with SHA-1 {sha1}")