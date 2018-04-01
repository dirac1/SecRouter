#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import fileinput
import subprocess

# variables 
enable = sys.argv[1]
conf_type = sys.argv[2]
interface = sys.argv[3]
network =  sys.argv[4]
prefix = sys.argv[5]
ip = sys.argv[6]
gw = sys.argv[7]

# --------------------------  check and replace  -----------------------------
# function to check if the file contain the value, if it is there the function will delete it
def cor(file_dir,data,replace):
    with fileinput.FileInput(file_dir,inplace=True) as file:
        for line in file:
            print(line.replace(data,replace),end=' ')

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will replace it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
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
def main(enable,conf_type,interface,network,prefix,ip,gw):
    file_test='/home/dirac/SecRouter/interfaces.d/'+interface
    file_dir = '/etc/network/interfaces.d/'
    file_int = '/etc/network/interfaces.d/'+interface

    # -------------------------- ip calculations -----------------------------
    networkprefix = network+'/'+prefix

    netmask = str(ipaddress.ip_network(networkprefix).netmask)
    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_test, 'a').close()
            for value in data:
                cow(file_test,value)

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_test, 'a').close()
            for value in data:
                cow(file_test,value)

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_test, 'a').close()
            for value in data:
                cow(file_test,value)

    for path in execute(['ifreload','-a']):
        print(path, end='')
    for path in execute(['ifquery','-a']):
        print(path, end='')
    else: # Disable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_test, 'a').close()
            for value in data:
                cor(file_test,value,'')

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_test, 'a').close()
            for value in data:
                cor(file_test,value,'')

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_test, 'a').close()
            for value in data:
                cor(file_test,value,'')
    for path in execute(['ifreload','-a']):
        print(path, end='')
    for path in execute(['ifquery','-a']):
        print(path, end='')

main(enable,conf_type,interface,network,prefix,ip,gw)
