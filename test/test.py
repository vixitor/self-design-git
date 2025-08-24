import subprocess
import os
"""
这个测试是测试工具能不能像git一样工作，只测试功能不测试实现。
"""
### 准备工作，如果有名字是final_test的文件夹就删除
if os.path.exists("final_test"):
    result = subprocess.run(["rm", "-rf", "final_test"])
    if result.returncode != 0:
        print("\033[31m remove final_test failed \033[0m")
        print(result.stderr)
        exit(1)
os.mkdir("final_test")
os.chdir("final_test")

print("input the name or address of the tool:")
tool = input().strip()
print(f"test {tool}...")
result = subprocess.run([tool, "init"])
if result.returncode != 0:
    print("\033[31m init failed \033[0m")
    print(result.stderr)
    exit(1)
print("\033[32m init success \033[0m")

info = ["my name is william", "i am a student", "i love programming"]
with open("name.txt", "w", encoding="utf-8") as f:
    f.write(info[0])
result = subprocess.run([tool, "add", "name.txt"])
if result.returncode != 0:
    print("\033[31m add failed \033[0m")
    print(result.stderr)
    exit(1)
print("\033[32m add success \033[0m")


result = subprocess.run([tool, "commit", "-m", "first commit"])
if result.returncode != 0:
    print("\033[31m commit failed \033[0m")
    print(result.stderr)
    exit(1)
with open("name.txt", "r", encoding="utf-8") as f:
    content = f.read().strip()
    if content != info[0]:
        print("\033[31m commit failed \033[0m")
        print(f"\033[31m content:{content} \033[0m", )
        exit(1)
print("\033[32m commit success \033[0m")
