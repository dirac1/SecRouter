#!/usr/bin/python
# APPLY BUTTON for DHCP tab in the category DHCP Client

import os
import subprocess
import fileinput
import sys

interface = sys.argv[1]
enable = sys.argv[2]

# functions
from misc_rs import cow # check or  write
from misc_rs import execute # execute a command 

# ------------------------------ main -------------------------------------
def main(interface,enable):
    if enable=='False':
        for path in execute(["ip",'l','set',interface,'down']):
            print(path, end="")
        for path in execute(["ip",'l','set',interface,'up']):
            print(path, end="")
    else:
        # request ip from the specified interface
        for path in execute(["dhclient",'-4','-v', interface]):
            print(path, end="")

main(interface,enable)
