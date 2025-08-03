import configparser
import os
import hashlib

def build_tree(path, files, git_repo):
    tree = Tree(path)
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path):
            for file in files:
                print(entry_path, os.path.join(git_repo, file.file_path))
                if os.path.join(git_repo, file.file_path) == entry_path:
                    print(path, file.file_path)
                    tree.add((file.file_path, file.file_hash))
        else:
            if entry == ".git":
                continue
            sub_file = []
            for file in files:
                if file.file_path.startswith(entry + os.sep):
                    sub_file.append(file)
            sub_tree = build_tree(entry_path, sub_file, git_repo)
            if not sub_tree.empty():
                tree.add((sub_tree.path, sub_tree.hash))
    if not tree.empty():
        tree.cal_hash()
        tree.write()
    return tree

def find_git_repo(path):
    current_path = os.path.abspath(path)
    while current_path != os.path.dirname(current_path):
        git_dir = os.path.join(current_path, ".git")
        if os.path.isdir(git_dir):
            return current_path
        current_path = os.path.dirname(current_path)
    raise Exception("Not a git repository (or any of the parent directories): .git")

def git_sha1(filepath):
    """
    use abs file path
    """
    print(f"in git_sha1: file path {filepath}")
    with open(filepath, 'rb') as f:
        data = f.read()
    return hashlib.sha1(data).hexdigest()


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
    def __init__(self, file_path, file_hash=None, git_dir=None):
        self.file_path = file_path
        self.git_dir = git_dir or os.path.join(find_git_repo(self.file_path),".git")
        self.abs_path = os.path.join(os.path.dirname(self.git_dir), file_path)
        if file_hash is None:
            self.file_hash = git_sha1(self.abs_path)
        else:
            self.file_hash = file_hash

    def write(self):
        create_blob(self.file_hash, self.git_dir)
        write_index(self.file_path, self.file_hash, self.git_dir)

    def recalculate_hash(self):
        self.file_hash = git_sha1(self.abs_path)

    def __repr__(self):
        return f"TrackedFile(file_path={self.file_path}, file_hash={self.file_hash}, git_dir={self.git_dir})"

class Tree:
    def __init__(self, path, git_dir=None):
        self.hash = None
        self.entry = []
        if not git_dir:
            self.git_dir = os.path.join(find_git_repo(path), ".git")
        self.path = path

    def add(self, file):
        self.entry.append(file)

    def empty(self):
        return len(self.entry) == 0

    def cal_hash(self):
        data = b""
        for e in self.entry:
            data += e[0].encode('utf-8') + b'\0' + bytes.fromhex(e[1])
        self.hash = hashlib.sha1(data).hexdigest()
        return self.hash

    def write(self):
        if not self.hash:
            self.cal_hash()
        object_path = os.path.join(self.git_dir, "objects", self.hash[:2], self.hash[2:])
        os.makedirs(os.path.dirname(object_path), exist_ok=True)
        with open(object_path, 'wb') as f:
            for entry in self.entry:
                f.write(entry[0].encode('utf-8') + b'\0' + bytes.fromhex(entry[1]))

    def __repr__(self):
        return f"Tree(path={self.path}, hash={self.hash}, git_dir={self.git_dir}, entry={self.entry})"
class GitRepository:
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




