import os,sys,inspect
import sys
import multiprocessing
import utils.bluetooth 
from utils.flight_utils import *

# vehicle = None
connection_string = '/dev/serial0'

def bluetooth_listener():
	# Connect to bluetooth indefinitely
	while 1:
		base = bluetooth.Connection()
		base.connect()
		while 1:
			message = base.listen()
			if not message:
				break # Reconnect
			else:
				message_handler(message)

def message_handler(message):
	if message == "mission":
		print("Mission signal received.")
		flight_controller = multiprocessing.Process(name='flight_controller', target=start_mission)
		flight_controller.start()
		return
	elif message == "land":
		print("Land signal received.")
		flight_controller.terminate()
		vehicle = connect(connection_string, wait_ready=True)
		vehicle.mode = 'LAND'
		return
	elif message == "kill":
		print("Kill signal received")
	else:
		print("Message not recognized.")

def start_mission():
	# Connect to the Vehicle
	print('Connecting to vehicle on: %s' % connection_string)
	vehicle = connect(connection_string, wait_ready=True, baud=921600)

	# Begin mission
	arm_and_takeoff(vehicle,10) 

	print("Moving forward at 3m/s for 5s")
	# send_ned_velocity(vehicle, 5, 0, 0, 10)
	print('Return to launch')
	vehicle.mode = 'RTL'

	print("Close vehicle object")
	vehicle.close()

bluetooth_listener = multiprocessing.Process(name='bluetooth_listener', target=bluetooth_listener)
bluetooth_listener.start()
		
