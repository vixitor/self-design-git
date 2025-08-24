import os

if os.path.exists("add_test"):
    os.system("rm -rf add_test")
os.mkdir("add_test")
os.chdir("add_test")
os.system(".././sjy init")
os.system("echo 'hello world' > hello.txt")
os.system(".././sjy add hello.txt")
print("-> add again to test the warning message")
os.system(".././sjy add hello.txt")
os.system("echo 'hello world hello world' > hello2.txt")
os.system(".././sjy add hello2.txt")
print("-> add a not exist file to test the error message")
os.system(".././sjy add not_exist.txt")
