Backup & Restore
=================
You must create a script to backup all the configuration files of the router which consist of the next files:

---

### DHCP 

	* /etc/dhcpcd.conf
	* /etc/dhcpcd.d/\*
	* /etc/default/isc-dhcp-server

### Ethernet & Routing
	* /etc/network/secrouter.conf
	* /etc/network/interfaces.d/\*
	* /etc/network/vlan.d/\*
	* /etc/network/bridge.d/\*
	* /etc/network/arp.d/\*
	* /etc/bing/named.local.options

### Firewall
	* /etc/iptables.rules

---

Backup
------
You can proceeed with this method:
	1. create the file name directory with the same hierarchy of the system configuration files
	2. Copy all the configurations files inside the file name directory.  
	3. Compress this directory and save it inside the directory *backups*.

Restore
-------
[file name].bck needs to be overwrite the router actual configuration fileswhile realizing a restore process and then it most apply the correc service restarts or reactivating the interfaces

The most suitable processs could be:
	1. Decompress the backup file and start copying each file to the system
	2. Delete the actual configuration files in the  system 
	3. Copy the configuration files to the system directories
	4. After copying all the backup configuration files to the system, restart the services in this order:
		1. Ethernet \& Routing
		2. DHCP
		3. Firewall
	5. delete the uncompressed files from the backup directory

Considerations
--------------
This procedure only conceives the router side view. However, you must consider how the GUI will present this data after the restore procedure.
