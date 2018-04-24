#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import fileinput
import subprocess
import shutil

# variables 
bor = sys.argv[1]
filename = sys.argv[2]

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
def main(bor,filename):
# BACKUP 
    if bor == '0':
        # 1. create the file name directory with the hierarchy
        # You must create the directories for DHCP, ETH&ROUTING and FIREWALL
        secrouter_backup_dir = '/home/secrouter/backup'
        backup_dir = '/home/secrouter/backup/'+filename
        os.mkdir(backup_dir)

	# 2. Copy all the configurations files inside the file name directory.  
        # DHCP
        if os.path.isfile('/etc/dhcpcd.conf') == True:
            shutil.copy2('/etc/dhcpcd.conf',backup_dir)
        if os.path.isfile('/etc/default/isc-dhcp-server') == True:
            shutil.copy2('/etc/default/isc-dhcp-server',backup_dir)

        dhcpcd_d = os.listdir('/etc/dhcpcd.d/')
        for value in dhcpcd_d:
            if os.path.isfile( dhcpcd_d + value ) == True:
                shutil.copy2(dhcpcd_d + value , backup_dir )

        # Ethernet & Routing
        if os.path.isfile( '/etc/network/secrouter.conf' ) == True:
            shutil.copy2('/etc/network/secrouter.conf' , backup_dir)
        if os.path.isfile( '/etc/bing/named.local.options' ) == True:
            shutil.copy2('/etc/bing/named.local.options' , backup_dir)

        eth_multi_files = ['/etc/network/interfaces.d/', \
                           '/etc/network/vlan.d/', \
                           '/etc/network/bridge.d/', \
                           '/etc/network/arp.d/' ]
        for files in eth_multi_files:
            this = os.listdir(file)
            if this == []:
               break
            for value in files:
                shutil.copy2(files + value , backup_dir )

        # Firewall
        if os.path.isfile('/etc/iptables.rules') == True:
            shutil.copy2('/etc/iptables.rules' , backup_dir)

        # Compressing ../backup/filename
        backup = secrouter_backup_dir + '/' + filename + 'tar.gz'
        for path in execute(['tar','-czvf',backup_dir,backup]):
            print(path, end='')

# RESTORE

    else:

    # 1. Descompress the backup file from the backup directory
        secrouter_backup_dir = '/home/secrouter/backup'
        backup = secrouter_backup_dir + '/' + filename + 'tar.gz'
        for path in execute(['tar','-xzvf',backup,backup_dir]):
            print(path, end='')

    # 3. delete old configuration files
    # 2. Copy the backup files from the filename to the system
    # 5. delete the uncompressed files from the backup directory

    # 4. Restart The services 
        # Restart Networking
        for path in execute(['systemctl','restart','networking']):
            print(path, end='')
        print(' ### New Ethernet & Routing configuration ###')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        print(' ### ################## ###')

        # Restart DHCP
        for path in execute(["systemctl","restart","isc-dhcp-server"]):
            print(path , end = '')

        # Release/Renew DHCP Client
        # You have to lookup the interface inside the configuration files
    #        for path in execute(['ip','link','set','dev',interface,'down']):
    #            print(path, end='')
    #        for path in execute(['ip','link','set','dev',interface,'up']):
    #            print(path, end='')
        for path in execute(["dhclient",'-4','-v', dhclient_interface]):
            print(path, end="")
        # Restart Firewall
        iptables_rules = open('/etc/iptables.rules', 'w')
        p = subprocess.Popen(["iptables-restore"], stdout=iptables_rules)
        iptables_rules.close()
        print('-----------------------------------')
        print('NEW FILTER RULES:')
        for path in execute(["iptables",'-v','-L','-t', 'filter']):
            print(path, end="")
        print(command)
        print('-----------------------------------')
        print('NEW NAT RULES:')
        for path in execute(["iptables",'-v','-L','-t', 'nat']):
            print(path, end="")
        print(command)
        print('-----------------------------------')

main(bor,filename)

