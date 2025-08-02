import argparse
import os.path
import sys

import mygit_init as init
import mygit_add as add
import mygit_ls_index as ls_index
from helper import find_git_repo, read_index
from pathlib import Path
from helper import TrackedFile

argparser = argparse.ArgumentParser(description="The stupidest content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

init_parser = argsubparsers.add_parser("init", help="Initialize a new repository")
init_parser.add_argument("path", nargs="?", default=".", help="Path to initialize the repository in (default: current directory)")

add_parser = argsubparsers.add_parser("add", help="Add file contents to the index")
add_parser.add_argument("files", nargs="*", help="Files to add to the index")
add_parser.add_argument("--all", "-A", action="store_true", help="Add all files in the current directory and subdirectories")

ls_parser = argsubparsers.add_parser("ls-index", help="List files in the index")

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = argparser.parse_args(argv)
    print(f"args : {args}")
    if args.command == "init":
        init.main(args.path)
    elif args.command == "ls-index":
        ls_index.main()
    elif args.command == "add":
        add.main(args)