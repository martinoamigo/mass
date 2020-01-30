import bluetooth

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

def connect_to_scout():
	socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	socket.connect((serverMACAddress, port))
	return socket

socket = connect_to_scout()

while 1:
	print("Ready for input...\n")
	text = input()
	if text == "quit":
		break
	socket.send(text)
	
socket.close()
