import os.path

if os.path.exists("init_test"):
    os.system("rm -rf init_test")
os.mkdir("init_test")
os.chdir("init_test")
os.system(".././sjy init")
print("-> init again to test the warning message")
os.system(".././sjy init")

