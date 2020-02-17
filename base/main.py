import time
import sys
import utils.bluetooth as bluetooth

#connect to scout
scout = bluetooth.Connection()

def bluetooth_listener(scout):
	# Connect to bluetooth indefinitely
	while 1:
		scout.connect()
		while 1:
			message = scout.listen()
			if not message:
				break # Reconnect
			else:
				print(message)

print("Input message for scout (or 'exit')...\n")
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


