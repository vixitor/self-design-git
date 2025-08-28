import subprocess
import os
"""
这个测试是测试工具能不能像git一样工作，只测试功能不测试实现。
"""
### 准备工作，如果有名字是final_tst的文件夹就删除，所有测试在testfile下面完成
if os.path.exists("testfile"):
    os.system("rm -rf testfile")
os.mkdir("testfile")
os.chdir("testfile")
tool = "../.././sjy"
### 初始化仓库
subprocess.run([tool, "init"])
assert os.path.exists(".sjy")
### 创建一个文件并添加到仓库
os.system("echo 'Hello World' > file1.txt")
subprocess.run([tool, "add", "file1.txt"])
index_path = os.path.join(".sjy", "index")
assert os.path.exists(index_path)
os.system(f"{tool} commit -m 'Initial commit'")
os.system("echo 'This is a test file.' >> file1.txt")
subprocess.run([tool, "add", "file1.txt"])
os.system(f"{tool} commit -m 'Update file1.txt'")
print("-> test log")
os.system(f"{tool} log")
print("-> test status")
os.system("echo 'Another line.' >> file1.txt")
subprocess.run([tool, "status"])
os.system("rm file1.txt")
os.system("echo 'New file content.' > file2.txt")
os.system("echo 'Some other content.' > file3.txt")
os.system(f"{tool} add file2.txt")
subprocess.run([tool, "status"])
os.system(f"{tool} commit -m 'Add file2.txt'")
os.system(f"{tool} add file1.txt")
subprocess.run([tool, "status"])