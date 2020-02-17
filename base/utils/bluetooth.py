import bluetooth
import time
import sys

size = 1024
scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

class Connection:
	def __init__(self):
		self.socket = None

	def connect(self):
		# try:
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		print("Connecting...")
		self.socket.connect((scout_bt_mac_addr, port))
		print("Connected.")
		# except:
		# 	time.sleep(3)
		# 	self.connect()
	
	def listen(self):
		try:	
			while 1:
				data = self.socket.recv(size)
				if data:
					return data
		except:
			print("[ERROR]: Connection lost.")
			return False

	def send_message(self, message):
		try:
			self.socket.send(message)
			return True
		except:
			print("Sending message failed: {}".format(sys.exc_info()[0]))
			return False
