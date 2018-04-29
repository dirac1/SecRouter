#!/usr/bin/python
# coding=utf-8

import os
import sys
import subprocess

# functions
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main():

    # Restart the DNS server to apply the changes     
    for path in execute(["systemctl","stop","bind9"]):
        print(path , end = '')
    for path in execute(["systemctl","disable","bind9"]):
        print(path , end = '')

main()
