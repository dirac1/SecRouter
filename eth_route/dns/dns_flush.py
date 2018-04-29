#!/usr/bin/python
# coding=utf-8

import os
import sys
import subprocess

# functions
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main():
    os.remove('/home/secrouter/eth_route/dns/parsed_cache.csv') # removing old cache list
    # flush dns cache and reload the dns server     
    for path in execute(["rndc","flush"]):
        print(path , end = '')
    for path in execute(["rndc","reload"]):
        print(path , end = '')

main()

