#!/usr/bin/python
# coding=utf-8

import os
import sys
import fileinput
import subprocess

# variables 
enable = sys.argv[1]
server1 = sys.argv[2]
server2 = sys.argv[3]

# functions
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main(enable,server1,server2):
    # ENABLE
    if enable == '0':

        if server2 == '':
            server2 = server1

        data = [ '# /etc/ntp.conf, configuration for ntpd; see ntp.conf(5) for help',\
                 'driftfile /var/lib/ntp/ntp.drift', \
                 '# Enable this if you want statistics to be logged.', \
                 '#statsdir /var/log/ntpstats/', \
                 'statistics loopstats peerstats clockstats', \
                 'filegen loopstats file loopstats type day enable', \
                 'filegen peerstats file peerstats type day enable', \
                 'filegen clockstats file clockstats type day enable', \
                 '#Servers', \
                  'pool ' + server1, \
                  'pool ' + server2, \
                 '# By default, exchange time with everybody, but dont allow configuration.', \
                 'restrict -4 default kod notrap nomodify nopeer noquery limited', \
                 '# Local users may interrogate the ntp server more closely.', \
                 'restrict 127.0.0.1', \
                 'restrict ::1', \
                 ' # Needed for adding pool entries', \
                 'restrict source notrap nomodify noquery' ]

        file_dir = '/etc/ntp.conf'
        named = open( file_dir , 'w+' )
        named.writelines('\n'.join(data))
        named.close()

        # Restart the DNS server to apply the changes     
        for path in execute(["systemctl","restart","ntp"]):
            print(path , end = '')
        for path in execute(["systemctl","enable","ntp"]):
            print(path , end = '')
        for path in execute(["ntpq","-p"]):
            print(path , end = '')

    # DISABLE
    else:

        for path in execute(["systemctl","stop","ntp"]):
            print(path , end = '')
        for path in execute(["systemctl","disable","ntp"]):
            print(path , end = '')
main(enable,server1,server2)
