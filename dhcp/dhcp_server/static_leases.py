#!/usr/bin/python
# APPLY BUTTON for the DHCP TAB in the category Static Leases

import os
import fileinput
import ipaddress
import subprocess
import sys
# testing
#interface_default = 'eth0'
#hostname_default = 'client'
#ip_default = '192.168.1.1'
#mac_default = 'FF:FF:FF:FF:FF:FF'

# variables
interface = sys.argv[1]
hostname = sys.argv[2]
ip = sys.argv[3]
mac = sys.argv[4]

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
# -------------------------- comment function -----------------------------
def comment(interface,input_file,text,do=True,comment_glyph='#'):
    with fileinput.FileInput(input_file, inplace=True) as file:
        for line in file:
            if do:
                print(line.replace(text,comment_glyph + text), end='')
            else:
                print(line.replace(comment_glyph + text,text), end='')

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# -------------------------- main -----------------------------

def main(interface, hostname, ip, mac):

    checkfile = 'include \"/etc/dhcpcd.d/static.leases.' + interface + '\";'
    cow('/etc/dhcpcd.conf', checkfile)

    static_leases = open('/etc/dhcpcd.d/static.leases.' + interface,'a')
    data = [ 'host ' + hostname + '{' \
             ,'hardware ethernet ' + mac + ';' \
             , 'fixed-address ' + ip + ';' \
             , '}\n' ]
    static_leases.writelines('\n'.join(data))

     # Restart the dhcp server   
    for path in execute(['/etc/init.d/isc-dhcp-server','restart']):
        print(path, end='')

main(interface,hostname,ip,mac)
