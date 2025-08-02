import argparse
import os.path
import sys
import mygit_init as init
import mygit_add as add
from helper import find_git_repo
from pathlib import Path
argparser = argparse.ArgumentParser(description="The stupidest content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
init_parser = argsubparsers.add_parser("init", help="Initialize a new repository")
init_parser.add_argument("path", nargs="?", default=".", help="Path to initialize the repository in (default: current directory)")
add_parser = argsubparsers.add_parser("add", help="Add file contents to the index")
add_parser.add_argument("files", nargs="*", help="Files to add to the index")
add_parser.add_argument("--all", "-A", action="store_true", help="Add all files in the current directory and subdirectories")

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = argparser.parse_args(argv)
    print(f"args : {args}")
    if args.command == "init":
        path = args.path
        init.main(path)

    elif args.command == "add":
        if not args.files and not args.all:
            raise Exception("No files specified to add. Use 'git add --all' to add all files.")
        root = find_git_repo(".")
        git_dir = os.path.join(root, ".git")
        if not git_dir:
            raise Exception("Not a git repository (or any of the parent directories): .git")
        file_toadd = []
        root_path = Path(os.path.abspath(root)).resolve()
        git_path = Path(os.path.abspath(git_dir)).resolve()
        if args.all:
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    file_path = Path(os.path.abspath(os.path.join(dirpath, filename))).resolve()
                    if file_path.is_relative_to(git_path):
                        continue
                    file_toadd.append(os.path.relpath(file_path, root_path))
        else:
            files = args.files
            for file in files:
                file_path = Path(os.path.abspath(os.path.join(".", file))).resolve()
                print(file_path)
                if not os.path.exists(file_path):
                    raise Exception(f"Pathspec '{file}' did not match any files")
                if not file_path.is_relative_to(root_path):
                    raise Exception(f"Pathspec '{file}' is outside of the repository root '{root}'")
                if file_path.is_relative_to(git_path):
                    continue
                file_toadd.append(os.path.relpath(file_path, root))
        objects_dir = os.path.join(git_dir, "objects")
        if not os.path.exists(objects_dir):
            raise Exception(f"Objects directory '{objects_dir}' does not exist in the repository")
        print(f"git add files: {files}")
        add.main(git_dir, file_toadd)