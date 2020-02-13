import time
import sys
import utils.bluetooth

#connect to scout
scout = bluetooth.Connection()
scout.connect()

#TODO handle disconnect error

print("Input message for scout (or 'exit')...\n")
while 1:
	message = input()
	if message == "exit":
		break
	scout.send_message(message)
self.socket.close()


