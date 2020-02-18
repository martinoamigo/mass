import bluetooth
import time
import sys

size = 1024
scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

class Connection:
	def __init__(self):
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	def connect(self):
		try:
			print("Connecting...")
			self.socket.connect((scout_bt_mac_addr, port))
			print("Connected.")
		except:
			self.socket.close()
			time.sleep(5)
			self.connect()
	
	def listen(self):
		try:	
			while 1:
				data = self.socket.recv(size)
				if data:
					return data
		except:
			print("[BASE]: Receiving message failed: {}".format(sys.exc_info()[0]))
			return b'error'

	def send_message(self, message):
		try:
			self.socket.send(message)
			return b'success'
		except:
			print("[BASE]: Sending message failed: {}".format(sys.exc_info()[0]))
			return b'error'
