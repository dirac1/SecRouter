import os
import re
import fileinput

Interface = 'eth0'
dhcp_dir = os.listdir('/home/dirac/fake_etc')
for file in dhcp_dir:
    if file == Interface + '.conf':
        os.rename('/home/dirac/fake_etc/' + Interface + '.conf', '/home/dirac/fake_etc/' + Interface + '.conf.disabled')
        look = ('include \"dhcpd.d/'+ Interface + '.conf\"')
        commented = ('#include \"dhcpd.d/'+ Interface + '.conf\"')
        with fileinput.FileInput('/home/dirac/dhcpd.conf', inplace=True) as file:
            for line in file:
                print(line.replace(look,commented), end='')
    else:
        print('The configuration file doesn\'t exist')
