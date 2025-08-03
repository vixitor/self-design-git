
from helper import TrackedFile, find_git_repo, read_index
import os
from pathlib import Path
def main(args):
    if not args.files and not args.all:
        raise Exception("No files specified to add. Use 'git add --all' to add all files.")
    root = find_git_repo(".")
    git_dir = os.path.join(root, ".git")
    if not git_dir:
        raise Exception("Not a git repository (or any of the parent directories): .git")
    file_to_add = []
    root_path = Path(os.path.abspath(root)).resolve()
    git_path = Path(os.path.abspath(git_dir)).resolve()
    if args.all:
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                file_path = Path(os.path.abspath(os.path.join(dirpath, filename))).resolve()
                if file_path.is_relative_to(git_path):
                    continue
                file_to_add.append(os.path.relpath(file_path, root_path))
    else:
        files = args.files
        for file in files:
            file_path = Path(os.path.abspath(os.path.join(".", file))).resolve()
            if not os.path.exists(file_path):
                raise Exception(f"Pathspec '{file}' did not match any files")
            if not file_path.is_relative_to(root_path):
                raise Exception(f"Pathspec '{file}' is outside of the repository root '{root}'")
            if file_path.is_relative_to(git_path):
                continue
            file_to_add.append(os.path.relpath(file_path, root))
    objects_dir = os.path.join(git_dir, "objects")
    if not os.path.exists(objects_dir):
        raise Exception(f"Objects directory '{objects_dir}' does not exist in the repository")
    file_to_add.sort()
    cached_file = [] if not os.path.exists(os.path.join(git_dir, "index")) else read_index(os.path.join(git_dir, "index"))
    for file in file_to_add:
        flag = False
        for cached in cached_file:
            if cached.file_path == file:
                cached.recalculate_hash()
                flag = True
        if not flag:
            cached_file.append(TrackedFile(file_path=file, git_dir=git_dir))
    with open(os.path.join(git_dir, "index"), 'wb') as _:
        pass
    for file in cached_file:
        file.write()
