# -*- coding: utf-8 -*-
# Client and server for udp (datagram) echo.

import atexit, datetime, hashlib, json, math, random, sys
import socket as socketModule
from threading import Timer
from socket import *
from filehandler import filehandler as FH
from config import config

logger = config.logger 
date = datetime.datetime
messageData = ""

# install at 205 /home/d23kue/development/python


###############################################################################################
##################################### UDP CONNECTION TEST #####################################
###############################################################################################

#################################### PYTHON VERSION VARIANTS ##################################

def v_bytes(string):
    return bytes(string, "utf-8") if sys.version_info[0] == 3 else string

def v_input(string):
    return input(string) if sys.version_info[0] == 3 else raw_input(string)

######################################## PARSE USER INPUT ####################################

def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        FH.FileHandler().logFile("server")
        # streamsocket
        streamServer()
    elif sys.argv[1] == '-c':
        FH.FileHandler().logFile("client")
        global messageData
        messageData = FH.FileHandler().read(config.fileName, config.filePath)
        udpClient()
    else:
        usage()


##################################### USAGE EXPLANATION #####################################

def usage():
    sys.stdout = sys.stderr
    print ('\nThis is a UDP-connection test server and client system.')
    print ('It counts lost packages sent between the client and the server.\n')
    print ('Usage:')
    print ('------')
    print ('To start the server type: python udpEcho.py -s [-p port]')
    print ('To start the client type: python udpEcho.py -c <host_ip> [-p port] [-a packet_amount]')
    print ('The parameters in brackets [] are optional \n')
    print ('the default echoserver port is 49975, the default streamport is 49976.')
    print ('the default packet size is 1024, the default packet amount is 10^6')
    sys.exit(2)

def portOption():
    if "-p" in sys.argv and len(sys.argv) > sys.argv.index("-p") + 1:
        return eval(sys.argv[sys.argv.index("-p") + 1])
    else:
        return config.ECHO_PORT

def packetAmount():
    if "-a" in sys.argv and len(sys.argv) > sys.argv.index("-a") + 1:
        return eval(sys.argv[sys.argv.index("-a") + 1])
    else:
        return config.MAX_PACKAGE_NUM 


############################################ SERVER ############################################

def streamServer():
    logEvent("server ready", "", "", "")
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind((config.SERVER_ADDRESS, config.stream_port))
    serversocket.listen(5)
    while True:
        # accept connections from outside
        (clientsocket, address) = serversocket.accept()
        logEvent("transfer request", "", address, "")
        if address[0] in config.allowed_clients and address[1] in range(10000, 10021):
            udpServer()
            # serversocket.close()
            # streamServer()
        else:
            logEvent("unallowed transfer attempt", "", address, "")

def udpServer():
    # optional port
    port = portOption()
    # create udp socket
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((config.SERVER_ADDRESS, port))
    udpClients = []

    while 1:
        data, addr = sock.recvfrom(config.BUFSIZE)
        packet = jsonLoad(data)
        matchingClients = [client for client in udpClients if client['address'] == addr]
        udpClient = matchingClients[0] if len(matchingClients) > 0 else None
        # initial message
        if packet['serial'] == 0 and udpClient == None:
            registerClient(udpClients, packet, addr)
        # missing initial message, stop the transfer
        if packet['serial'] > 0 and udpClient == None:
            sendTransferAbort(sock, addr)
        # data was not json serializable
        if ((packet['serial'] == None and udpClient != None) or (len(data) < packet['size'])):
            sendWarning(udpClient, sock, addr)
        # serial packets
        elif packet['serial'] > 0 and udpClient != None:
            udpClient['received'] += 1
            udpClient['last_serial'] = packet['serial']
            dataHash = hashlib.md5(json.dumps(packet['data']).encode('utf-8')).hexdigest()
            sock.sendto(data, addr)
            # missing packets
            if udpClient['last_serial'] + 1 < packet['serial']:
                logEvent("missing packets %s - %s" % (udpClient['last_serial'] + 1, packet['serial'] - 1 ), "", addr, "")
            # unequal hashes
            if packet['datahash'] != dataHash:
                logEvent("wrong data hash", "", addr, dataHash)
            # last expected packet 
            if packet['serial'] == udpClient['expected']:
                message = "expected: %d, received: %d, broken: %d " % (udpClient['expected'], udpClient['received'], udpClient['broken_packets'])
                logEvent(message, "", addr, "")
                confirm = messageJSON(udpClient['expected'] + 1, udpClient['received'], message).encode()
                sock.sendto(confirm, addr)
                logEvent("send confirmation", addr, "", "")
                del udpClients[udpClients.index(udpClient)]
               
def registerClient(udpClients, packet, addr):
    udpClients.append({
        'address': addr, 
        'expected': packet['packets'], 
        'received': 0, 
        'last_serial': 0,
        'broken_packets': 0
        })
    print ("\n-------------------------------------------------------------------------------")
    logEvent("expecting %s packets" % (packet['packets']), "", addr, "")

def sendWarning(udpClient, sock, addr):
    jsonwarning = messageJSON(-2, 0, 'server received broken packet (serial >= %d)' % (udpClient['last_serial'] + 1))
    udpClient['received'] += 1
    udpClient['last_serial'] += 1
    udpClient['broken_packets'] += 1
    sock.sendto(jsonwarning, addr)

def sendTransferAbort(sock, addr):
    logEvent("missing intitial message from %s" % (str(addr)), "", "", "")
    message = messageJSON(-1, 0, 'missing initial message, please start again')
    sock.sendto(message, addr)


############################################# CLIENT ############################################
            
def udpClient():
    if len(sys.argv) < 3:
        usage()
    host = sys.argv[2]
    streamClient(host)

def streamClient(host):
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientaddress = (FH.FileHandler().get_ip(), random.randint(10000, 10020)) 
    clientsocket.bind(clientaddress)

    try: 
        print ("\n-------------------------------------------------------------------------------")
        logEvent("test connection", str((host, config.stream_port)), "", "")
        clientsocket.connect((host, config.stream_port))
        startclient = True
    except:
        logEvent("SERVER NOT RUNNING", "", "", "")
        startclient = False

    if startclient == True:
        Timer(1.0, startClient, (clientaddress, host)).start()
    clientsocket.close()

def startClient(clientaddress, host):
    # optional port
    port = portOption()
    # optional packet amount
    max_packet_num = packetAmount()
    # create socket
    addr = host, port
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(clientaddress)
    sock.settimeout(config.ECHO_TIMEOUT)
    # sending opener
    opener = messageJSON(0, max_packet_num, 'transfer begins')
    logEvent('sending opener', addr, "", "")
    logEvent("expecting %s packets" % (max_packet_num), "", addr, "")
    sock.sendto(opener, addr)
    # sending packets
    packetEcho(0, max_packet_num, sock, addr)

def packetEcho(serial, max_packet_num, sock, addr):
    start_time = date.now()
    while serial < max_packet_num:
        serial += 1
        packet = messageJSON(serial, max_packet_num, messageData)
        sock.sendto(packet, addr)
        # receiving echo
        try:  
            data, fromaddr = sock.recvfrom(config.BUFSIZE)
            packet = jsonLoad(data)
            config.lastSentPacket['received_packets'] += 1
            # data was not json serializable
            if ((packet['serial'] == None) or (len(data) < packet['size'])):
                config.lastSentPacket['broken_packets'] += 1
            if packet['serial'] != None:
                # print every 'INTER_PRINT'-th packet (None for no intermediate printing)
                if config.INTER_PRINT != None and packet['serial'] % config.INTER_PRINT == 0:
                    print ("received packet %d" % (packet['serial']))
                dataHash = hashlib.md5(json.dumps(packet['data']).encode('utf-8')).hexdigest()
                # no initial message or server sided broken packet
                if packet['serial'] == -1:
                    logEvent("SERVER: " + packet['data'], "", "", "")
                    return
                # server sided json error
                if packet['serial'] == -2:
                    config.lastSentPacket['broken_packets'] += 1
                    logEvent(packet['data'], "", "", "")
                # missing packets
                if serial < packet['serial']:
                    logEvent("missing packets %s - %s" % (serial, packet['serial'] - 1 ), "", addr, "")
                    # unequal hashes
                if packet['datahash'] != dataHash:
                    logEvent("wrong data hash", "", addr, dataHash)
                if packet['serial'] == max_packet_num:
                    config.runWhile = 0
                    confirmation(sock, start_time, max_packet_num)
        except:
            logEvent("%ds timeout after sending packet %d" % (config.ECHO_TIMEOUT, serial), addr, "", "")


def confirmation(sock, start_time, max_packet_num):
    data, fromaddr = sock.recvfrom(config.BUFSIZE)
    packet = jsonLoad(data)
    logEvent("SERVER: " + packet['data'], "", "", "")
    transfer_duration = date.now() - start_time
    lost_packets = max_packet_num - config.lastSentPacket['received_packets']
    failure_rate = (float(lost_packets)*100)/max_packet_num
    success_rate = 100 - failure_rate
    failure_rate = str(failure_rate) + "%"
    success_rate = str(success_rate) + "%"
    logEvent("CLIENT: expected %d, received: %d, lost: %d, broken: %d, success rate: %s, failure rate: %s, transfer duration: %s" % (
        max_packet_num, 
        config.lastSentPacket['received_packets'], 
        lost_packets, 
        config.lastSentPacket['broken_packets'],
        success_rate, 
        failure_rate,
        str(transfer_duration)
        ), "", "", "")
    sock.close()
    

############################################ MESSAGES ########################################### 

def messageJSON(serial, last_packet, data):
    message = {
        'serial': serial,
        'packets': last_packet,
        'data': data,
        'size': 0,
        'datahash': hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
    }
    messageSize = len(str(message))
    message['size'] = messageSize + len(str(messageSize)) - 1
    return json.dumps(message)

def jsonLoad(data):
    try:
        packet = json.loads(data)
        return packet
    except:
        return {'serial': None, 'data': 'no json', 'size': 47}


############################################# LOGGING ###########################################        

def logEvent(event, sent_to, received_from, error):
    # logger.info("#datetime;#system_name;#system_location;#event;#sent_to;#received_from;#error;")
    now = str(date.now())
    receiver = "to " + str(sent_to) if sent_to != "" else ""
    sender = "from " + str(received_from) if received_from != "" else ""
    print (now, event, sender, receiver)
    logger["events"].info("%s;%s;%s;%s;%s;%s;%s;" % (
        now, 
        socketModule.gethostname(), 
        FH.FileHandler().get_ip(), 
        event,
        sent_to, 
        received_from, 
        error 
        )
    )

@atexit.register
def goodbye():
    if logger["events"] != "":
        logEvent("exit script", "", "", "")

main()