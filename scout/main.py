import bluetooth 

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 3 
backlog = 1
size = 1024

def accept_base_connection():
	try:
		socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		socket.bind((scout_bt_mac_addr, port))
		socket.listen(backlog)
		client, clientInfo = socket.accept()
		print("Connection accepted.")
	except e:
		print("Error accepting base connection: ", sys.exc_info()[0])
	return client


def listen(client):
	try:	
		print("Listening...")
		while 1:
			data = client.recv(size)
			if data:
				print(data)
				client.send(data) # Echo back to client
				client.send("echooooo") # Echo back to client
	except:	
		print("Exception, closing BT socket and attempting to reopen")
		client.close()
		socket.close()
		client = accept_base_connection()
		listen(client)

client = accept_base_connection()
listen(client)