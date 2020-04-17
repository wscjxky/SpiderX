import paramiko
import time
log = open("log.txt",'a',encoding='utf8') 
class wang(object):
    def __init__(self, host, port, username, password, cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd

    def commad(self, newuser, newpass):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, port=self.port,
                    username=self.username, password=self.password)
        stdin, stdout, stderr = ssh.exec_command(
            self.cmd, get_pty=True, timeout=8)
        stdin.write(self.password+"\n")
        stdin.flush()
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        log_data=(time.asctime( time.localtime(time.time()) )+ result.decode())
        print(log_data)
        log.write(log_data.replace("\n",""))
        log.write("\n")
        ssh.close()


if __name__ == "__main__":
    with open("data.txt", 'r')as f:
        ls = f.readlines()
        for l in ls:
            try:
                arr = l.split("\t")
            except Exception as e:
                print(e)
                arr = l.split(" ")
            ip = arr[0]
            user = arr[1]
            passwd = arr[2]
            touser = arr[3]
            newpass = arr[4].strip('\n')
            print("正在连接: "+ip)
            log.write("正在连接: "+ip+"\n")
            cmd = 'echo "' + passwd + '" | sudo  -S '+' echo "' + \
                newpass + '" |sudo  passwd --stdin ' + touser
            cmd = ' echo "' + newpass + '" |sudo  passwd --stdin ' + touser
            try:
                wang(ip, 22, user, passwd, cmd).commad(touser, newpass)
            except Exception as e:
                print(e)
