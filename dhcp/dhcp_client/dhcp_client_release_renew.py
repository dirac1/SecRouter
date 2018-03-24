#!/usr/bin/python
# APPLY BUTTON for DHCP tab in the category DHCP Client

import os
import subprocess
import fileinput
import sys

interface = sys.argv[1]
release = sys.argv[2]
# ----------- execute command and print the stout or stderr  ---------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# ------------------------------ main -------------------------------------
def main(interface,release):
    # remove dhclient.leases
    if release==False:
        print(release)
        dhcp_dir = os.listdir('/var/lib/dhcp')
        for files in dhcp_dir:
            # check if the file exist in the directory and erase it
            if files == '/var/lib/dhcp/dhclient.leases':
                print('the file exists')
                os.remove('/var/lib/dhcp/dhclient.leases')
        # release ip from the specified interface
        for path in execute(["dhclient",'-4','-v', interface]):
            print(path, end="")
    else:
        print(release)
        # renew ip from the specified interface
        for path in execute(["dhclient",'-4','-v','-r', interface]):
            print(path, end="")
main(interface,release)

