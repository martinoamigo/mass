import time
import sys
import utils.bluetooth as bluetooth

#connect to scout
scout = bluetooth.Connection()
scout.connect()

#TODO handle disconnect error

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


