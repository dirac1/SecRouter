#!/usr/bin/python
# coding=utf-8

import sys
import os
import fileinput
import subprocess

# variables 
rule = sys.argv[1]
table = sys.argv[2]
chain = sys.argv[3]

# functions
from misc_rs import cow # check or  write
from misc_rs import cor # check or replace
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main( rule , table, chain ):

    # Enable on boot
    data = ['#!/bin/sh' , \
            '/sbin/iptables-restore < /etc/iptables.rules']
    for value in data:
        cow('/etc/network/if-pre-up.d/iptables', value)
    command = rule.split(' ')
    command.insert(0,'iptables')
    command.insert(1,'-t')
    command.insert(2, table)
    # Apply rule
    print('-----------------------------------')
    print('RULE:')
    print(command)
    print('-----------------------------------')
    for path in execute(command):
        print(path, end='')

    # Making the rules permanent
    iptables_rules = open('/etc/iptables.rules', 'w')
    p = subprocess.Popen(["iptables-save"], stdout=iptables_rules)
    iptables_rules.close()

    # Present updated chain on CLI
    for path in execute([ 'iptables','-n','--line-numbers','-t', table, '-L', chain ]):
        print(path, end='')
    print('-----------------------------------')

main( rule , table, chain )
