# -*- coding: utf-8 -*-
##############################################################################################################
#################################### UDP CONNECTION TEST CONFIGURATION #######################################
##############################################################################################################

# name of provider
PROVIDER = "Fantasy"
# Ethernet/LAN ipv4 of server (local if running server, 'localhost or '127.0.0.1' are not valid)
SERVER_ADDRESS = 'localhost' 
# echo port
ECHO_PORT = 49975
# max number of bytes to receive per package
BUFSIZE = 4096


########################################## ONLY RELEVANT FOR CLIENT ##########################################

# number of packages to send
MAX_PACKAGE_NUM = 10**6
# timeout in seconds to wait for echo from server
ECHO_TIMEOUT = 10.0
# print every 'INTER_PRINT'-th package (set to None for no intermediate printing)
INTER_PRINT = 5*10**3


##############################################################################################################
###################################### fixed parameters, don't change ########################################
##############################################################################################################

import os, datetime

############################################## FILES AND LOGGING #############################################

# paths
cwd = os.getcwd()
logPath = cwd + "/logfiles"
filePath = cwd + "/textfiles"
fileName = "Mitra.txt"

# logger object
logger = {
	"events": ""
}


################################################ SERVER PARAMS ###############################################

# streamserver to let clients check running server
stream_port = 49976

# allowed clients
allowed_clients = [
	'localhost',
	'127.0.0.1',
	'192.168.2.114'
]


################################################# CLIENT PARAMS ###############################################

# checking echo
lastSentPacket = {
	"serial": 0,
	"sent": datetime.datetime.now(),
	"received_echo": False,
	"received_packets": 0,
	"broken_packets": 0,
}

