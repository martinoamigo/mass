import os,inspect
import sys
import multiprocessing
import utils.bluetooth as bluetooth 
from utils.flight_utils import *
import time

connection_string = '/dev/serial0'
flight_controller = None
global base
global vehicle


def bluetooth_listener(base):
	while 1:
		conn = base.connect()
		if conn:
			while 1:
				message = base.listen()
				message_handler(message)

def message_handler(message):
	global flight_controller
	if message == b'mission':
		base.send("Mission signal received.")
		flight_controller = multiprocessing.Process(name='flight_controller', target=start_mission)
		flight_controller.daemon = True
		flight_controller.start()
		return
	
	elif message == b'land':
		base.send("Land signal received. Connecting to Pixhawk")
		try:
			flight_controller.terminate()
			vehicle = connect(connection_string, wait_ready=True, baud=921600)
			vehicle.mode = 'LAND'
			base.send("Vehicle mode set to 'LAND'.")
		except:
			base.send("Unable to land.")
		return
	
	elif message == b'disarm':
		base.send("Disarm signal received. Connecting to Pixhawk...")
		try:
			flight_controller.terminate()
			vehicle = connect(connection_string, wait_ready=True, baud=921600)
			vehicle.armed = False
			while vehicle.armed:      
				time.sleep(1)
			base.send("Vehicle disarmed.")
		except:
			base.send("Could not disarm vehicle.")
		return
	
	elif message == b'stop':
		try:
			flight_controller.terminate()
			base.send("Mission stopped.")
		except:
			base.send("No mission to stop.")
		return
	
	elif message == b'error':
		print("[ERROR]: Some bluetooth exception. Likely out of range...")

	else:
		base.send("Command not recognized. Valid commands are: \n- mission \n- land\n- disarm\n- stop")
		return

def start_mission():
	# Connect to the Vehicle
	base.send('Connecting to vehicle on: %s' % connection_string)
	vehicle = connect(connection_string, wait_ready=True, baud=921600)

	# Begin mission
	arm_and_takeoff(base,vehicle,10) 

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
		
