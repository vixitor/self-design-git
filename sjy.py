import argparse
import os.path


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    init_parser = subparser.add_parser("init")
    add_parser = subparser.add_parser("add")
    add_parser.add_argument("file", nargs=1)
    args = parser.parse_args()
    match args.command:
        case "init":
            from init import init
            init()
        case "add":
            from add import add
            file = os.path.abspath(args.file[0])
            add(file)
        case _:
            print("\033[31m Unknown command \033[0m")