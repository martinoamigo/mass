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
			self.socket.connect((scout_bt_mac_addr, port))
			return True
		except:
			# self.socket.close()
			time.sleep(5)
			return False
	
	def listen(self):
		try:	
			while 1:
				data = self.socket.recv(size)
				if data:
					return data
		except:
			return False

	def send_message(self, message):
		try:
			self.socket.send(message)
			return True
		except:
			return False
