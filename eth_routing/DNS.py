#!/usr/bin/python
# coding=utf-8

import os
import sys
import fileinput
import subprocess
import math

# variables 
server1 = sys.argv[1]
server2 = sys.argv[2]
server3 = sys.argv[3]
max_cache_size = sys.argv[4]

# ----------- execute command and print the stout or stderr  -------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# ---------------------------------- main --------------------------------
def main(server1,server2,server3,max_cache_size):

    max_cache_size = int(max_cache_size)*math.pow(10,6)

    data = [ 'acl allowed {', \
             'localhost;', \
             'localnets;};', \
             'options {', \
             'directory "/var/cache/bind";', \
             'recursion yes;', \
             'allow-query {allowed;};', \
             'forwarders {'+server1+';'+server2+';'+server3+';};', \
             'max-cache-size '+max_cache_size+';', \
             'forward only;', \
             'dnssec-enable yes;', \
             'dnssec-validation yes;', \
             'auth-nxdomain no;};' ]

    file_dir = '/etc/bind/named.conf.options'
    named = open( file_dir , 'w+' )
    named.writelines('\n'.join(data))
    named.close()

    # Restart the DNS server to apply the changes     
    for path in execute(["systemctl","restart","bind9"]):
        print(path , end = '')
    for path in execute(["named-checkconf"]):
        print(path , end = '')