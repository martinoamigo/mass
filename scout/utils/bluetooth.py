import bluetooth

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 3 
backlog = 1
size = 1024

class Connection:
	def __init__(self):
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.client = None

	def connect(self):
		try:
			self.socket.bind((scout_bt_mac_addr, port))
			self.socket.listen(backlog)
			print("Waiting for base to request connection...")
			self.client, clientInfo = socket.accept()
			print("Connection accepted.")
		except:
			print("[ERROR] accepting base connection({}), retrying...".format(sys.exc_info()[0]))
			self.connect()

	def listen(self):
		try:	
			# print("Listening...")
			while 1:
				data = self.client.recv(size)
				if data:
					print(data)
					self.client.send(data) # Echo back to client
		except:	
			print("[ERROR]: Closed BT socket({})".format(sys.exc_info()[0]))
			self.client.close()
			self.socket.close()