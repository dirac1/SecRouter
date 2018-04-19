#!/usr/bin/python
# coding=utf-8

import sys
import os
import fileinput
import subprocess

# variables 
rule = sys.argv[1]
chain = sys.argv[2]

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

# ---------------------------------- main --------------------------------
def main( rule , chain ):

    # Enable on boot
    data = ['#!/bin/sh' , \
            '/sbin/iptables-restore < /etc/iptables.rules']
    for value in data:
        cow('/etc/network/if-pre-up.d/iptables', value)
    command = rule.split(' ')
    command.insert(0,'iptables')
    # Apply rule
    for path in execute(command):
        print(path, end='')

    # Making the rules permanent
    iptables_rules = open('/etc/iptables.rules', 'w')
    p = subprocess.Popen(["iptables-save"], stdout=iptables_rules)
    iptables_rules.close()

    # Present updated chain on CLI
    for path in execute([ 'iptables','-n','--line-numbers','-L', chain ]):
        print(path, end='')

main( rule , chain )
# Test with this rule:
# iptables -A INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT
