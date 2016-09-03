# -*- coding: utf-8 -*-

import chardet, datetime, codecs, io, logging, os, socket
from config import config

date = datetime.datetime
logger = config.logger

##################################################################################################
########################################### HANDLING FILES ########################################
##################################################################################################


class FileHandler(object):

    def encoding(self, fileName):
        with open(fileName, "rb") as readFile:
            raw = readFile.read(32)
            readFile.close()
            if raw.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'
            else:
                result = chardet.detect(raw)
                encoding = result['encoding']
        return encoding

    def read(self, fileName, path):
        os.chdir(path)
        if fileName in os.listdir("."):
            encoding = self.encoding(fileName)
            openFile =  io.open(fileName, "r", encoding = encoding)
            fileText = openFile.read()
            openFile.close()
        os.chdir(config.cwd)
        return fileText

    def logFile(self, side):
        logFile = config.PROVIDER + "_" + side + "_log.csv"
        os.chdir(config.logPath)
        logger["events"] = logging.getLogger(logFile[:-4])
        fileHandler = logging.FileHandler(config.logPath + "/" + logFile)
        logger["events"].addHandler(fileHandler) 
        logger["events"].setLevel(logging.DEBUG)
        if os.stat(logFile).st_size == 0:
            logger["events"].info("#datetime;#system_name;#system_location;#event;#sent_to;#received_from;#error;")
            logger["events"].info("%s;%s;%s;udp log file created;;;;" % (str(date.now()), socket.gethostname(), self.get_ip()) )
        os.chdir(config.cwd)

    # returns 127.0.0.1 on VM Ubuntu
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP



    

    