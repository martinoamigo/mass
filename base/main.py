import bluetooth
import time

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

def connect_to_scout():
	try:
		socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		socket.connect((scout_bt_mac_addr, port))
		return socket
	except:
		time.sleep(2)
		print("Scout not listening, retrying...")
		connect_to_scout()

socket = connect_to_scout()

print("Ready for input...\n")
while 1:
	text = input()
	if text == "quit":
		break
	socket.send(text)
	data = socket.recv(1024)
	if data:
		print(data)

socket.close()
