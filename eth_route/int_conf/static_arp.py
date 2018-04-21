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
ip =  sys.argv[4]
mac = sys.argv[5]

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
def main(enable,conf_type,interface,ip,mac):
    print(" ### Starting configuration ### ")
    # ----------- remove white lines -------------
    rwl('/etc/network/arp.d/','ether.'+interface)
    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/interfaces.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/vlan.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')


        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/bridge.d/'+interface
            data_arp = mac + ' ' + ip
            data_int = 'post-up arp -f '+ file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')

        print(" ### Actual configuration ### ")
        for path in execute(['ifquery','-a']):
            print(path, end='')

    else: # Disable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/interfaces.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/vlan.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/bridge.d/'+interface
            data_arp = mac + ' ' + ip
            data_int = 'post-up arp -f '+ file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        print(" ### Actual configuration ### ")
        for path in execute(['ifquery','-a']):
            print(path, end='')



main(enable,conf_type,interface,ip,mac)

