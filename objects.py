import os
import configparser
from helper import find_git_repo, git_blob_sha1
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

def git_track_file():

    def __init__(self, path, git_repo = None):
        self.path = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.sha1 = git_blob_sha1(path)
        self.git_repo = git_repo or find_git_repo(os.path.dirname(path))
        if not self.git_repo:
            raise Exception(f"Not a git repository (or any of the parent directories): {os.path.dirname(path)}")
        self.objects_dir = os.path.join(self.git_repo, ".git", "objects")
        self.object_file = os.path.join(self.objects_dir, self.sha1[:2], self.sha1[2:])
        os.makedirs(os.path.dirname(self.object_file), exist_ok=True)
        with open(self.object_file, 'wb') as f:
            f.write(self.sha1.encode('utf-8'))
        print(f"Add file {path}: SHA1: {self.sha1} in objects")


