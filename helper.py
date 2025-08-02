import configparser
import os
import hashlib

def find_git_repo(path):
    current_path = os.path.abspath(path)
    while current_path != os.path.dirname(current_path):
        git_dir = os.path.join(current_path, ".git")
        if os.path.isdir(git_dir):
            return current_path
        current_path = os.path.dirname(current_path)
    raise Exception("Not a git repository (or any of the parent directories): .git")

def git_blob_sha1(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    size = len(data)
    header = f"blob {size}\0".encode("utf-8")
    full = header + data
    return hashlib.sha1(full).hexdigest()

def create_blob(file_hash, git_dir):
    objects_dir = os.path.join(git_dir,"objects")
    file_path = os.path.join(objects_dir, file_hash[:2], file_hash[2:])
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(file_hash.encode('utf-8'))

def write_index(file_path, file_hash, git_dir):
    index_path = os.path.join(git_dir, "index")
    with open(index_path, 'ab') as index_file:
        index_file.write(file_hash.encode("utf-8"))
        index_file.write(file_path.encode('utf-8') + b'\0')

def read_index(index_path):
    files = []
    with open(index_path, 'rb') as index_file:
        while True:
            file_hash = index_file.read(40)
            if not file_hash:
                break
            file_hash = file_hash.decode('utf-8')
            tmp = index_file.read(1)
            file_path = ''
            while tmp and tmp != b'\0':
                file_path += tmp.decode('utf-8')
                tmp = index_file.read(1)
            files.append(TrackedFile(file_path, file_hash))
    return files


class TrackedFile:
    file_path = None
    file_hash = None
    git_dir = None
    def __init__(self, file_path, file_hash=None, git_dir=None):
        self.file_path = file_path
        self.git_dir = git_dir or self.get_git_dir()
        if file_hash is None:
            self.file_hash = git_blob_sha1(file_path)
        else:
            self.file_hash = file_hash

    def write(self):
        create_blob(self.file_hash, self.git_dir)
        write_index(self.file_path, self.file_hash, self.git_dir)

    def get_git_dir(self):
        return self.git_dir or os.path.join(find_git_repo(self.file_path),".git")

    def recalculate_hash(self):
        self.file_hash = git_blob_sha1(self.file_path)

    def __repr__(self):
        return f"TrackedFile(file_path={self.file_path}, file_hash={self.file_hash}, git_dir={self.git_dir})"

class GitRepository:

    repo_path = None
    git_dir = None

    def __init__(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.repo_path = os.path.abspath(path)
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




