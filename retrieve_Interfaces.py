#!/usr/bin/python
import netifaces

mylist = netifaces.interfaces()
print('[%s]' % ', '.join(map(str, mylist)))
