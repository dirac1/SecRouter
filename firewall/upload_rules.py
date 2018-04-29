#!/usr/bin/python
# coding=utf-8

import sys
import os
import subprocess
import shutil

# variables 
filename = sys.argv[1]

# functions
from misc_rs import cow # check or  write
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main(filename):

    # Enable on boot
    data = ['#!/bin/sh' , \
            '/sbin/iptables-restore < /etc/iptables.rules']
    for value in data:
        cow('/etc/network/if-pre-up.d/iptables', value)

    # Flusing old rules
    for path in execute(["iptables",'-t','filter','-F']):
        print(path, end="")
    for path in execute(["iptables",'-t','nat','-F']):
        print(path, end="")

    shutil.copy2( '/home/secrouter/tmp/'+filename , '/etc/iptables.rules' )
    for path in execute(["sh",'/etc/network/if-pre-up.d/iptables']):
        print(path, end="")

    # Retrieving new rules from uploaded file
    #iptables_rules = open('/home/secrouter/tmp/' + filename, 'r')
    #for line in iptables_rules:
    #    print(line)
    #p = subprocess.Popen(["iptables-restore"], stdin=iptables_rules)
    #p = subprocess.Popen(["iptables-restore"])
    #p.stdin.readline(iptables_rules)
    #p.stdin.close()
    # Updating chains
    #iptables_rules.close()

    print('-------------FIREWALL--------------')
    print('-----------------------------------')
    print('NEW FILTER RULES:')
    for path in execute(["iptables",'-v','-L','-t', 'filter']):
        print(path, end="")
    print('-----------------------------------')
    print('NEW NAT RULES:')
    for path in execute(["iptables",'-v','-L','-t', 'nat']):
        print(path, end="")
    print('-----------------------------------')

main(filename)
