import configparser
import os.path


class GitRepository:

    def __init__(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        if os.path.exists(os.path.join(path, ".git")):
            print(f"Reinitialized existing Git repository in {os.path.join(path, '.git')}")
            """
            TODO
            """
        else:
            os.mkdir(os.path.join(path, ".git"))
            print(f"Initialized empty Git repository in {os.path.join(path, '.git')}")
            config = configparser.ConfigParser()
            config["core"] = {
                "repositoryformatversion": "0",
                "filemode": "true",
                "bare": "false",
                "logallrefupdates": "true",
            }
            with open(os.path.join(path, ".git", "config"), "w") as configfile:
                config.write(configfile)
            with open(os.path.join(path, ".git", "description"), "w") as descfile:
                descfile.write("Unnamed repository; edit this file 'description' to name the repository.\n")
            with open(os.path.join(path, ".git", "HEAD"), "w") as headfile:
                headfile.write("ref: refs/heads/main\n")
            os.mkdir(os.path.join(path, ".git", "refs"))
            os.mkdir(os.path.join(path, ".git", "refs", "heads"))
            os.mkdir(os.path.join(path, ".git", "refs", "tags"))
            os.mkdir(os.path.join(path, ".git", "objects"))
            os.mkdir(os.path.join(path, ".git", "objects", "info"))
            os.mkdir(os.path.join(path, ".git", "objects", "pack"))

def main(path=None):
    repo = GitRepository(path)