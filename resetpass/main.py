from fabric.api import *


with open("data.txt", 'r')as f:
    ls = f.readlines()
    for l in ls:
        arr = l.split(" ")
        ip = arr[0]
        user = arr[1]
        passwd = arr[2]
        touser = arr[3]
        newpass = arr[5].strip('\n')
        print("正在连接: "+ip)
        env.passwords[user+"@"+ip+":22"]=passwd
        env.hosts.append(ip)

def mytask():
    from fabric.state import env
    print(env.passwords)
    print(env.hosts)
    com='echo "' + passwd + '" | sudo -S '+' echo "' + newpass+ '" |sudo  passwd --stdin ' + touser 
    sudo(com) 
    run('ls')
if __name__ == "__main__":
    results = execute(mytask)