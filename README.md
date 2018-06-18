SecRouter
=========

SecRouter is a prototype security router for SMEs and SOHO made by engineering students from The University Of Carabobo in Venezuela, applying, network dissagregation, and FOSS.

Based on these premises and using python as the main framework. We achieved a functional GUI controller for Debian-Based Raspberry Pi B2 OS (Raspbian), Adding simplicity to the network facilities already embedded in the Linux Kernel with the next capabilities:

* Remote login using ssh with the module paramiko
* Stateful Firewall using xtables
* GeoIP (Xtables-addons) for Geographic filtering using iptables
* Basic ethernet configuration for Interfaces, Vlan and Bridges
* DHCP server instances for multiple interfaces
* DNS Caching and forwarding server
* System administration module rich in network tools
* netdata as system monitoring tool

---
### Es:
SecRouter es un enrutador de seguridad prototipo para pequeñas y medianas empresas hecho por estudiantes de ingeniería de la Universidad de Carabobo en Venezuela, aplicando los conceptos de desagregación de redes y el Software libre.

Basado en estas premisas y utilizando Python como infraestructura principal, Nosotros logramos construir una interfaz gráfica que controla a un Raspberry Pi B2 basado en Raspbian (Distribución de Linux basada en Debian), Añadiendo simpleza a los elementos de red existentes en el Kernel de Linux. El software posee las siguientes características:
* Conexión remota utilizando SSH mediante el modulo Paramiko de Python
* Cortafuegos de estados utilizando xtables
* GeoIP (Xtables-addons) para filtrado geografico utilizando iptables
* Configuración básica de ethernet para interfaces, vlans y bridges
* Servidor de DHCP multi-instancias
* Servidor de DNS para caché y forwarding
* Un modulo especializado para la administración del sistema, rico en herramientas de redes
* Sistema de monitoreo gracias a la herramienta web netdata

Instalación Raspberry PI
------------------------
1. Descargue el repositorio e instale los scripts en el raspberry PI (Si utiliza Windows utilice un cliente ssh como puTTY), empleando las siguientes credenciales para realizar la conexión:
	* user: pi
	* password: raspberry

2. Luego de establecida la conexión SSH con el dispositivo aplique los siguientes comandos:
```
# git clone https://github.com/dirac1/SecRouter.git && cd SecRouter
# sudo sh init_script.sh
```

3. Este procedimiento puede durar varios minutos dependiendo de su conexión al Internet

4. Luego de que la instalación haya culminado exitosamente el dispositivo estará listo para ser utilizado

Instalación Controlador (Windows)
---------------------------------
1. Descargue nuevamente el respositorio pero esta vez en su ordenador utilizando el siguiente comando dentro del cmd de Windows
```
# git clone https://github.com/dirac1/SecRouter.git && cd SecRouter
```

2. Dentro de la carpeta GUI del repositorio SecRouter se encuentra una carpeta con el nombre SecRouter en donde se encuentra el controlador, para mayor comodidad colóquelo dentro del directorio "archivos de programas" de su sistema y genere un acceso director del ejecutables "start.exe" por donde podrá acceder directamente a la aplicación

3. Luego de ejecutar la aplicación podra conectarse a su dispositivo, la clave y usuario por defecto del dispositivo serán
	* user: secrouter
	* password: routersec

Screenshots
-----------
### Home
![home](https://raw.githubusercontent.com/dirac1/SecRouter/master/screenshots/home.png)
### Filter
![filter](https://raw.githubusercontent.com/dirac1/SecRouter/master/screenshots/filter.png)
### DHCP Server
![dhcp-server](https://raw.githubusercontent.com/dirac1/SecRouter/master/screenshots/dhcp-server.png)
### Tools
![tools](https://raw.githubusercontent.com/dirac1/SecRouter/master/screenshots/tools.png)
