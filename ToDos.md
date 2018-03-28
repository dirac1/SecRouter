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
* All scripts in dhcp_server are working after debug with the prototype
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

**2018-03-26**

Ethernet & Routing
---------------------
* ARP will be configured using the command ''arp'' inside the configuration file ''/etc/network/interfaces''
    - the next value needs to be added: ''post-up arp -f /etc/ethers''
    - inside the file /etc/ethers/ you'll add the entries using this format: ''\[MAC\] \[IP\]''
    - And restarting the interface

**2018-03-27**

Ethernet & Routing
---------------------
* Bridge an Vlans will be configured using the ifupdown2 configuration file in ''/etc/network/interfaces'' using individual files with the 'include source/to/file' statement

* DNS will be possible using the package BIND9, it just needs to configure one file and it'll accept just one variable, servers. It'll be possible to show the actual cache and to flush it.
    - DNS will have 1 toggle button (enable/disable) and 2 normal buttons to flush the cache and to view cache
    - DNS enable button will run a script in the router while disable will simply stop and disable (don't start on boot) the bind9 service
    - view cache will adquire data from the 
TO FIX: The cache isn't showed inside the database but the DNS server is working 
* Static configuration and static routing  
