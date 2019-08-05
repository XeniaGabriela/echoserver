UDP ECHO SERVER AND CLIENT

Installation
------------

1. clone git repository 
2. install python 3.X and add its path to system path variables
3. cd udp/config and open config.py
4. set mandatory configuration parameters

		PROVIDER = name of provider
		SERVER_ADDRESS = 'XXX.XXX.XXX.XXX' # Ethernet/LAN ipv4

5. add Ethernet/LAN ipv4 of allowed clients to allowed_clients = ['localhost', '127.0.0.1']

------------- OPTIONAL --------------

6. change optional parameters if desired

		------------------------------------------ general ---------------------------------------
		
		ECHO_PORT = integer (range 49152–65535)                   --> override option in cmd/shell      
	        BUFSIZE = integer (max number of bytes to receive per package)
	    
	    ------------------------------- only relevant for client ---------------------------------

		MAX_PACKAGE_NUM = integer (number of packages to send)    --> override option in cmd/shell 
		ECHO_TIMEOUT = float (timeout in seconds to wait for echo from server)
		INTER_PRINT = integer (print every 'INTER_PRINT'-th package (set to None for no intermediate printing)
7. add client ip to allowed clients

		# allowed clients
		allowed_clients = [
			'localhost',
			'127.0.0.1',
			...
		]


Run Server
----------

- cd path/to/udp

- click on echoserver.bat
or
- run 'python udpEcho.py -s [-p port]' in cmd/shell, where
	1. [-p port] is an option to override ECHO_PORT in config.py


Run Client
----------

- run 'python udpEcho.py -c host [-p port] [-a package_amount]' in cmd/shell, where
	1. host is the Ethernet/LAN ipv4 address of the server,
	2. [-p port] is an option to override ECHO_PORT in config.py,
	3. [-a package_amount] is an option to override MAX_PACKAGE_NUM in config.py


Logfiles
--------

Log files will be automatically generated on both client and server side in the folder udp/logfiles. 
