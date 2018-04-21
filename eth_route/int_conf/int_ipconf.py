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

# TO BE TESTED
# ----------- remove white lines -------------
def rwl(filename):
    with open(filename) as infile, open('output', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
    os.remove(filename)
    os.rename('output',filename)

# ---------------------------------- main --------------------------------
def main(enable,conf_type,interface,network,prefix,ip,gw):
    file_dir = '/etc/network/interfaces.d/'
    file_int = '/etc/network/interfaces.d/'+interface

    if network=='':
        print('manual/dhcp type')
    else:
        # -------------------------- ip calculations -----------------------------
        networkprefix = network+'/'+prefix
        netmask = str(ipaddress.ip_network(networkprefix).netmask)
        broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        for path in execute(['ifquery','-a']):
            print(path, end='')
        #for path in execute(['systemctl','restart','networking']):
        #    print(path, end='')
        for path in execute(['ip','link','set','dev',interface,'down']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',interface,'up']):
            print(path, end='')
    else: # Disable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        #for path in execute(['systemctl','restart','networking']):
        #    print(path, end='')

main(enable,conf_type,interface,network,prefix,ip,gw)

