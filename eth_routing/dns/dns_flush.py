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
    os.remove('/home/secrouter/eth_route/dns/parsed_cache.csv') # removing old cache list
    # flush dns cache and reload the dns server     
    for path in execute(["rndc","flush"]):
        print(path , end = '')
    for path in execute(["rndc","reload"]):
        print(path , end = '')

main()

