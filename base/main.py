import time
import sys
import utils.bluetooth as bluetooth
import threading

#connect to scout
scout = bluetooth.Connection()

def bluetooth_listener():
	global scout
	connected = scout.connect()
	while 1:	
		while not connected:
			print("Connecting...")
			scout = bluetooth.Connection()
			connected = scout.connect()
			if connected:
				print("Connected.")
		
		message = scout.listen()
		if not message:
			print("[BASE]: Receiving message failed: {}".format(sys.exc_info()[0]))
			connected = False
		else:
			try:
				print("[SCOUT]: {}".format(message.decode()))
			except:
				print("[BASE]: Error decoding message: {}".format(message))

bluetooth_listener = threading.Thread(name='bluetooth_listener', target=bluetooth_listener)
bluetooth_listener.start()

while 1:
	message = input()
	if message == "exit":
		break
	response = scout.send_message(message)
	if not response:
		print("[BASE]: Sending message failed: {}".format(sys.exc_info()[0]))
		connected = False


self.socket.close()


