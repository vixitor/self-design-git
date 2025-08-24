import os
def init():
    if os.path.exists(".sjy"):
        print("\033[33m Repository already exists \033[0m")
    else :
        os.mkdir(".sjy")
        os.mkdir(".sjy/objects")
        os.system("touch .sjy/index")
        os.system("touch .sjy/HEAD")
        print("\033[32m Repository initialized \033[0m")