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
dst_network =  sys.argv[4]
prefix = sys.argv[5]
gw = sys.argv[6]

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
             print("cow: data not found")
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
def rwl(directory,filename):
    file_to_clean = directory+filename
    for files in os.listdir(directory):
        if files == filename:
            with open(file_to_clean) as infile, open('output', 'w') as outfile:
                for line in infile:
                    if not line.strip(): continue  # skip the empty line
                    outfile.write(line)  # non-empty line. Write it to output
            os.remove(file_to_clean)
            os.rename('output',file_to_clean)
        else:
            print('rwl: The file does not exist')

# ---------------------------------- main --------------------------------
def main(enable,conf_type,interface,dst_network,prefix,gw):
    print(" ### Starting configuration ### ")
    # -------------------------- ip calculations -----------------------------
    networkprefix = dst_network+'/'+prefix
    netmask = str(ipaddress.ip_network(networkprefix).netmask)
    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ip route add [dst_network]+/+[prefix] via [gw] dev [interface]

    # ----------- remove white lines -------------
    rwl('/etc/network/interfaces.d/',interface)
    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the route 
        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_int = '/etc/network/interfaces.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_int = '/etc/network/vlan.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_int = '/etc/network/bridge.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        print(" ### Actual configuration ### ")
        for path in execute(['ip','route','add',dst_network+'/'+prefix,'via',gw,'dev',interface]):
            print(path, end='')
        for path in execute(['ifquery','-a']):
            print(path, end='')

    else: # Disable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_int = '/etc/network/interfaces.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_int = '/etc/network/vlan.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_int = '/etc/network/bridge.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        print(" ### Actual configuration ### ")
        for path in execute(['ip','route','delete',dst_network+'/'+prefix]):
            print(path, end='')
        for path in execute(['ifquery','-a']):
            print(path, end='')

main(enable,conf_type,interface,dst_network,prefix,gw)

