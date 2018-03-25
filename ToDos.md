TODOS
======

**2018-03-18**

DHCP Server 
-----------

* Add the other files being used in the dhcp server to the enable and disable script
    - you must comment the interface on isc-dhcp-server 
    - you must comment the interface configuration on interface.d/[interface] **DONE**

* Start building the Static leases script 

* Create a new user inside de router 

* Give new user, super user access to the network characteristics **DONE** 
    - created a new group called network
    - allowed the user to run commands without password
 
* Enable one interface at a time 
    - Found a way to do it without involving modifying system services


DHCP CLIENT
-----------

* Start building the dhcp client script (you'll need extra scripts to do the renew/release buttons) **DONE**
    - Created a separated script for release/renew


**2018-03-20**

Debugging DHCP Server
---------------------

* Fix disable.py/enable.py to comment and uncomment the statement 'include /etc/dhcpcd.d/[interface]';



**2018-03-21**

Debugging DHCP Server
---------------------

* All scripts in dhcp\_server are working after debug with the prototype
    - You should find the way to show in leases status tab which hostnames are in static mode 
 

**2018-03-22**

Debugging DHCP Client
---------------------

* Debugged dhcp\_client scripts

**2018-03-24**

Ethernet & Routing
---------------------

* After all the conversations to consider the way to build this module, most of the requirment in it will be satisfied using the same methodology (writing on configuration files).
    - Vlan, Bridges, and Interfaces will be configured using ifupdown2 package
    - DNS will be configured using BIND9 
    - ARP will be configured using ip neigh (reviewing to make it permanent changes)
