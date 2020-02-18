import time
import sys
import utils.bluetooth as bluetooth
import multiprocessing

#connect to scout
scout = bluetooth.Connection()

def bluetooth_listener(scout):
	# Connect to bluetooth indefinitely
	while 1:
		scout.connect()
		while 1:
			message = scout.listen()
			if message == b'error':
				print("[BASE]: Some bluetooth exception.")
				# break # Reconnect
			else:
				print("[SCOUT]: {}".format(message))

bluetooth_listener = multiprocessing.Process(name='bluetooth_listener', target=bluetooth_listener, args=(scout,))
bluetooth_listener.start()

while 1:
	message = input()
	if message == "exit":
		break
	response = scout.send_message(message)
	if not response:
		# Reconnect
		del scout
		scout = bluetooth.Connection()
		scout.connect()

self.socket.close()


