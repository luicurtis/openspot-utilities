import paramiko
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--IP', required=True)
args = parser.parse_args()
#Connect my PC to my RPi via SSH
relative_path = os.path.relpath(os.curdir)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(args.IP, port = 22, username = "pi", password="hr634431")
print ("Connected to the Pi")
ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command('python /home/pi/Desktop/Technician/test.py')
time.sleep(15)
print("Sample Image Has Been Captured")
#Move file from RPi to my PC
ftp_client = ssh_client.open_sftp()
print("Transferring Image to Local Machine")
ftp_client.get("/home/pi/Desktop/Technician/checksport.jpg",os.path.join(relative_path, "Preview.jpg"))
ftp_client.close()