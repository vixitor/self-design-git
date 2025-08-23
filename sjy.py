import argparse
from init import init

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    init_parser = subparser.add_parser("init")

    args = parser.parse_args()
    if args.command == "init":
        init()
