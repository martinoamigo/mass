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
