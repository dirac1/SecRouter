#!/usr/bin/python
# coding=utf-8

import os
import sys
import subprocess

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
def main():

    # Restart the DNS server to apply the changes     
    for path in execute(["systemctl","stop","bind9"]):
        print(path , end = '')
    for path in execute(["systemctl","disable","bind9"]):
        print(path , end = '')
        
main()
