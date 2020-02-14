import bluetooth
import time

size = 1024
scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

class Connection:
	def __init__(self):
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	def connect(self):
		# try:
		self.socket.connect((scout_bt_mac_addr, port))
		# except:
			# time.sleep(3)
			# print("Could not connect, retrying...")
			# self.connect()

	def send_message(self, message):
		try:	
			self.socket.send(message)
			data = self.socket.recv(size)
			if data:
				print(data)
			return True
		except:
			print("Sending message failed.")
			return False
