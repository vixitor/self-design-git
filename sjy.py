import argparse
import os.path


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    init_parser = subparser.add_parser("init")
    add_parser = subparser.add_parser("add")
    add_parser.add_argument("file", nargs=1)
    commit_parser = subparser.add_parser("commit")
    commit_parser.add_argument("-m", "--message", nargs=1)
    log_parser = subparser.add_parser("log")
    status_parser = subparser.add_parser("status")
    checkout_parser = subparser.add_parser("checkout")
    checkout_parser.add_argument("commit_hash", nargs=1)
    args = parser.parse_args()
    match args.command:
        case "init":
            from scripts.init import init
            init()
        case "add":
            from scripts.add import add
            file = os.path.abspath(args.file[0])
            add(file)
        case "commit":
            from scripts.commit import commit
            commit(args.message[0])
        case "log":
            from scripts.log import log
            log()
        case "status":
            from scripts.status import status
            status()
        case "checkout":
            from scripts.checkout import checkout
            checkout(args.commit_hash[0])
        case _:
            print("\033[31m Unknown command \033[0m")