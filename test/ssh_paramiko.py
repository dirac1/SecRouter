#!/usr/bin/python
import paramiko
import sys
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('10.10.42.29',port=22,username='pi',password='raspberry')
sftp = ssh.open_sftp()

#interfaces = sftp.listdir(path="/sys/class/net")
#print('\n'.join(interfaces))

#thisfile = sftp.put('/home/dirac/dhcp.txt','/home/dirac/dhcp.txt')
#print(thisfile)

stdin, stdout, stderr = ssh.exec_command('ip a')
#print(stdout.read())
this = stdout.read()
print('\n'.join(this))

#dhcp = sftp.listdir(path="/home/dirac")
#print('\n'.join(dhcp))

#archivo = sftp.open('/home/dirac/dhcp.txt','a')
#archivo.write("This is a regular procedure")
#archivo.close

#archivo = sftp.open('/home/dirac/dhcp.txt','r+')
#print(archivo.read())
#print(archivo.read())
