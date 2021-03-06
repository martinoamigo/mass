import bluetooth
import sys
import logging
import time

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 3 
backlog = 1
size = 1024

def log_setup():
    logging.basicConfig(
        filename="masterCatalog.log",
        filemode="a",
        format=("%(asctime)s:%(levelname)s:%(message)s"),
        level=logging.INFO)
    global log
    log = logging.getLogger()

log_setup()

class Connection:
	def __init__(self):
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.client = None
		self.socket.bind((scout_bt_mac_addr, port))
		self.socket.listen(backlog)

	def connect(self):
		try:
			msg = "Waiting for base to request connection..."
			print(msg)
			log.info(msg)

			self.client, clientInfo = self.socket.accept()

			msg = "Connection accepted."
			print(msg)
			log.info(msg)
			 
			return True
		except:
			msg = "Not able to connect to client({})".format(sys.exc_info()[0])
			print(msg)
			log.info(msg)
			time.sleep(5)
			return False

	def listen(self):
		try:	
			while 1:
				data = self.client.recv(size)
				if data:
					return data
		except:	
			time.sleep(5)
			return False

	def send(self, message):
		try:
			print(message)
			self.client.send(message)
		except:
			print("Could not send message to base. No action taken.")
