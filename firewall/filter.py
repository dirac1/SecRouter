#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import fileinput
import subprocess

# variables 

# --------------------------  check and replace  -----------------------------
# function to check if the file contain the value, if it is there the function will delete it
def cor(file_int,data,replace):
    with fileinput.FileInput(file_int,inplace=True) as file:
        for line in file:
            print(line.replace(data,replace),end=' ')

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will replace it  
def cow(file_int,data):
     with open(file_int,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data+'\n')

# ----------- execute command and print the stout or stderr  -------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
# What you have to do?
# The main ability of this script is to add rules to iptables with a defined kind of targets and matches
# To do this you need to know how to add the rules
# each match and target has a way to add it
# ---------------------------------- main --------------------------------
def main():
    # Rule Handler
    if Handler == '1': # Append mode = '1' 
        chain = '-A ' + chain
    if Handler == '2': # Insert mode = '2' 
        chain = '-I ' + chain
    if Handler == '3': # Add to rule_line mode = '3' 
        chain = '-I ' + rule_line + ' ' + chain
    # Add to Chain ( INPUT, OUTPUT, FORWARD, User_Defined )
    # Source IP
    '-s ' + src_ip if src_ip_not == '0' else '-s ! ' + src_ip
    # Destination IP
    '-d '+dst_ip if dst_ip_not == '0' else '-d ! '+ dst_ip
    # Transport Layer Protocol
    '-p '+ TL_Proto if TL_Proto_not == '0' else '-p ! ' + TL_Proto
    # In Interface
    '-i '+ in_if if in_if_not == '0' else '-i ! ' + in_if
    # Out Interface
    '-o '+ out_if if out_if_not == '0' else '-o ! ' + out_if

    # --- MATCHES ---
    # IP


#    command = 'iptables -A INPUT -i ens3 -p tcp -m tcp --sport 6697 -j ACCEPT'

        for path in execute(['ifquery','-a']):
            print(path, end='')



main()

