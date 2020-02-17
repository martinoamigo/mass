import os,inspect
import sys
import multiprocessing
import utils.bluetooth as bluetooth 
from utils.flight_utils import *

connection_string = '/dev/serial0'
global base

def bluetooth_listener(base):
	while 1:
		conn = base.connect()
		if conn:
			while 1:
				message = base.listen()
				if not message:
					return # reconnect
				else:
					message_handler(message)

def message_handler(message):
	if message == b'mission':
		base.send("Mission signal received.")
		flight_controller = multiprocessing.Process(name='flight_controller', target=start_mission)
		flight_controller.start()
		return
	elif message == b'land':
		base.send("Land signal received.")
		flight_controller.terminate()
		vehicle = connect(connection_string, wait_ready=True)
		vehicle.mode = 'LAND'
		return
	elif message == b'disarm':
		base.send("Disarming...")
	elif message == b'kill':
		base.send("Kill signal received")
		return
	else:
		base.send("Message not recognized.")
		return

def start_mission():
	# Connect to the Vehicle
	base.send('Connecting to vehicle on: %s' % connection_string)
	vehicle = connect(connection_string, wait_ready=True, baud=921600)

	# Begin mission
	arm_and_takeoff(base,vehicle,5) 

	#print("Moving forward at 3m/s for 5s")
	# switch to GUIDED or GUIDEDNOGPS
	# send_ned_velocity(vehicle, 5, 0, 0, 10)
	print('Return to launch')
	vehicle.mode = 'RTL'

	print("Close vehicle object")
	vehicle.close()

base = bluetooth.Connection()
bluetooth_listener = multiprocessing.Process(name='bluetooth_listener', target=bluetooth_listener, args=(base,))
bluetooth_listener.start()
		
