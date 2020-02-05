import bluetooth

def connect_to_scout():
	try:
		socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		socket.connect((scout_bt_mac_addr, port))
		return socket
	except:
		time.sleep(2)
		print("Scout not listening, retrying...")
		connect_to_scout()

def accept_base_connection():
	try:
		socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		socket.bind((scout_bt_mac_addr, port))
		socket.listen(backlog)
		print("Waiting for base to request connection...")
		client, clientInfo = socket.accept()
		print("Connection accepted.")
	except e:
		print("Error accepting base connection: ", sys.exc_info()[0])
	return client, socket


def listen(client, socket):
	try:	
		print("Listening...")
		while 1:
			data = client.recv(size)
			if data:
				print(data)
				client.send(data) # Echo back to client
	except:	
		print("Exception, closing BT socket and attempting to reopen: ", sys.exc_info()[0])
		client.close()
		socket.close()
		client = accept_base_connection()
		listen(client, socket)