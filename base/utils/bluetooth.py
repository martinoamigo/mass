import bluetooth

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

class Connection:
	def __init__(self):
		self.socket = bluetooth.connect()

	def connect(self):
		try:
			self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			self.socket.connect((scout_bt_mac_addr, port))
		except:
			time.sleep(3)
			print("Could not connect, retrying...")
			self.connect()

	def send_input(self, message):
			self.socket.send(mesasge)
			data = self.socket.recv(1024)
			if data:
				print(data)
