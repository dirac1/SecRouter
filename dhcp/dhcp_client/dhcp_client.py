#!/usr/bin/python
# APPLY BUTTON for DHCP tab in the category DHCP Client

import os
import subprocess
import fileinput
import sys

interface = sys.argv[1]
enable = sys.argv[2]
# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# ----------- execute command and print the stout or stderr  ---------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# -------------------------- comment function -----------------------------
def comment(interface,input_file,text,do=True,comment_glyph='#'):
    with fileinput.FileInput(input_file, inplace=True) as file:
        for line in file:
            if do:
                print(line.replace(text,comment_glyph + text), end="")
            else:
                print(line.replace(comment_glyph + text,text), end="")

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
