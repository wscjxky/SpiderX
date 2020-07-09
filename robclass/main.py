import os
import subprocess
import time
with open('rob_data.txt', 'r', encoding='utf8')as f:
    ls = f.readlines()
    for line in ls:
        if line != '' and "#" not in line:
            print(line)
            subprocess.Popen('python 12-16.py '+ line,shell=True)
            time.sleep(20)