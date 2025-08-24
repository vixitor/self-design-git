import os

if os.path.exists("commit_test"):
    os.system("rm -rf commit_test")
os.mkdir("commit_test")
os.chdir("commit_test")
os.system(".././sjy init")
with open("file1.txt", "w") as f:
    f.write("Hello World")
os.system(".././sjy add file1.txt")
os.system('.././sjy commit -m "Initial commit"')
with open("file1.txt", "a") as f:
    f.write("\nThis is a test file.")
os.system(".././sjy add file1.txt")
os.system('.././sjy commit -m "Update file1.txt"')