import os,inspect
import sys
# import multiprocessing
import threading
import utils.bluetooth as bluetooth 
from utils.flight_utils import *
import time

connection_string = '/dev/serial0'

def bluetooth_listener(base, vehicle):
	""" Runs in the background to receive any messages sent from the base. Will only process one message at a time."""
	conn = base.connect()
	base.send("Connected to vehicle on {}\nType: {}\nArmed: {}\nSystem Status: {}\nGPS: {}\nAlt: {}\n".format(connection_string, vehicle._vehicle_type,vehicle.armed, vehicle.system_status.state, vehicle.gps_0, vehicle.location.global_relative_frame.alt))
	while 1:
		message = base.listen()
		if not message:
			# reconnect
			base = bluetooth.Connection()
			base.connect()
		message_handler(base, vehicle, message)

def message_handler(base, vehicle, message):
	if message == b'mission':
		base.send("Mission signal received.")
		flight_controller = threading.Thread(name='flight_controller', target=start_mission, args=(vehicle,))
		flight_controller.daemon = True
		flight_controller.start()
		return
	
	elif message == b'land':
		base.send("Land signal received.")
		vehicle.mode = 'LAND'
		return
	
	elif message == b'disarm':
		try:
			base.send("Disarming...")
			vehicle.armed = False
			while vehicle.armed:      
				time.sleep(1)
			base.send("Vehicle disarmed.")
		except:
			base.send("Could not disarm vehicle.")
	
	elif message == b'error':
		print("[ERROR]: Some bluetooth exception. Likely out of range...")

	else:
		base.send("Command not recognized. Valid commands are: \n- mission \n- land\n- disarm\n- stop")
		return

def start_mission(vehicle):
	# Begin mission
	response = arm_and_takeoff(base,vehicle,3)
	if response:
		#print("Moving forward at 3m/s for 5s")
		# switch to GUIDED or GUIDEDNOGPS
		# send_ned_velocity(vehicle, 5, 0, 0, 10)
		print('Return to launch')
		vehicle.mode = 'RTL'


# This can take a while, but we do it first for simplicity
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, baud=921600)

base = bluetooth.Connection()
bluetooth_listener = threading.Thread(name='bluetooth_listener', target=bluetooth_listener, args=(base,vehicle))
bluetooth_listener.start()