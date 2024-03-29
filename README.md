# UDP ECHO SERVER AND CLIENT

This repository contains a UDP server and a UDP client for testing UDP connections by counting lost packages.

## Requirements

Python 3 on any compatible OS

## Installation

1. clone this repository 
2. install python 3.X and add its path to system path variables
3. cd udp/config and open config.py
4. set mandatory configuration parameters in config.py
```
PROVIDER = name of provider
SERVER_ADDRESS = 'XXX.XXX.XXX.XXX' # Ethernet/LAN ipv4
```
5. add Ethernet/LAN ipv4 of allowed clients to allowed_clients = ['localhost', '127.0.0.1']

------------- OPTIONAL --------------

6. change optional parameters if desired
```
# general
ECHO_PORT = integer (range 49152–65535)   # can be overriden with command   
BUFSIZE = integer (max number of bytes to receive per package)

# only relevant for client
MAX_PACKAGE_NUM = integer (number of packages to send)  # can be overriden with command 
ECHO_TIMEOUT = float (timeout in seconds to wait for echo from server)
INTER_PRINT = integer (print every 'INTER_PRINT'-th package (set to None for no intermediate printing)

```
7. add client ip to allowed clients
```
# allowed clients
allowed_clients = [
	'localhost',
	'127.0.0.1',
	...
]
```

## Run Server

* cd path/to/udp
* run `python udpEcho.py -s [-p port]` in cmd/shell, where [-p port] is an option to override ECHO_PORT in config.py


## Run Client

* run `python udpEcho.py -c host [-p port] [-a package_amount]` in cmd/shell, where
	1. host is the Ethernet/LAN ipv4 address of the server,
	2. [-p port] is an option to override ECHO_PORT in config.py,
	3. [-a package_amount] is an option to override MAX_PACKAGE_NUM in config.py


# Log Files

Log files will be automatically generated on both client and server side in the folder udp/logfiles. 
For a production environment, you should store the log files on a system location which is dedicated for log files.
