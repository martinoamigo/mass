import time
import sys
import utils.bluetooth

scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8'
port = 3

socket = bluetooth.connect_to_scout()

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
