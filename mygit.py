import argparse
import os.path
import sys
import mygit_init as init
import mygit_add as add
argparser = argparse.ArgumentParser(description="The stupidest content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
init_parser = argsubparsers.add_parser("init", help="Initialize a new repository")
init_parser.add_argument("path", nargs="?", default=".", help="Path to initialize the repository in (default: current directory)")
add_parser = argsubparsers.add_parser("add", help="Add file contents to the index")
add_parser.add_argument("files", nargs="*", help="Files to add to the index")
add_parser.add_argument("--all", "-A", action="store_true", help="Add all files in the current directory and subdirectories")

def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv[:1])
    if args.command == "init":
        path = args.path
        init.main(path)
    if args.command == "add":
        if not args.files and not args.all:
            print("No files specified to add. Use 'git add --all' to add all files.")
            return
        if args.all:
            root_dir = os.getcwd()
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    add.main(file_path)
        else:
            for file in args.files:
                if os.path.exists(file):
                    add.main(file)
                else:
                    print(f"File '{file}' does not exist.")
