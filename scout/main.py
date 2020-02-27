import os,inspect
import sys
import threading
import time

import utils.bluetooth as bluetooth 
from utils.flight_utils import *
# import utils.pixycam as mypixy

connection_string = '/dev/serial0'

def bluetooth_listener(base, vehicle):
	""" Runs in the background to receive any messages sent from the base. Will only process one message at a time."""
	base.connect()
	base.send("Connected to vehicle on {}\nType: {}\nArmed: {}\nSystem Status: {}\nGPS: {}\nAlt: {}\n".format(connection_string, vehicle._vehicle_type,vehicle.armed, vehicle.system_status.state, vehicle.gps_0, vehicle.location.global_relative_frame.alt))
	while 1:
		message = base.listen()
		if not message or message == b'error':
			# reconnect
			# vehicle.mode = 'LAND'
			base.client.close()
			base.socket.close()
			base = bluetooth.Connection()
			base.connect()
		try:
			message_handler(base, vehicle, message.decode())
		except:
			base.send("Could not decode message '{}'".format(message))

def message_handler(base, vehicle, message):
	if message == 'mission':
		base.send("Mission signal received.")
		flight_controller = threading.Thread(name='flight_controller', target=start_mission, args=(vehicle,))
		flight_controller.daemon = True
		flight_controller.start()
		
	elif 'takeoff' in message:
		try:
			args = message.split()
			if len(args) != 2:
				raise Exception()
			args[1] = int(args[1])
			base.send("Takeoff signal received.")
			flight_controller = threading.Thread(name='flight_controller', target=takeoff, args=(vehicle,args[1]))
			flight_controller.daemon = True
			flight_controller.start()
		except:
			base.send("Invalid arguements for 'takeoff'. Required format is 'takeoff (height in meters)'")
	
	elif message == 'land':
		base.send("Land signal received.")
		vehicle.mode = 'LAND'

	elif message == 'rtl':
		base.send("RTL signal received.")
		vehicle.mode = 'RTL'

	elif message == 'loiter':
		base.send("Loiter signal received.")
		vehicle.mode = 'LOITER'
	
	elif message == 'stabilize':
		base.send("Loiter signal received.")
		vehicle.mode = 'STABILIZE'
	
	elif message == 'disarm':
		try:
			base.send("Disarming...")
			vehicle.armed = False
			while vehicle.armed:      
				time.sleep(1)
			base.send("Vehicle disarmed.")
		except:
			base.send("Could not disarm vehicle.")
	
	elif 'move' in message:
		try:
			args = message.split()
			if len(args) != 5:
				raise Exception()
			base.send("this is proper format, wrong exception")
			send_ned_velocity(vehicle, args[1],  args[2], args[3], args[4])
		except:
			base.send("Invalid arguements for 'move'. Required format is 'move x, y, z, t'")
	
	else:
		base.send("Command not recognized. Valid commands are: \n- mission \n- takeoff (height in meters)\n- land\n- rtl\n- loiter\n- stabilize\n- disarm\n- move x y z t")
		return

def start_mission(vehicle, altitude):                                                                                                                                                                                                                                                
	# Begin mission
	if vehicle.armed == False and altitude < 25:
		response = arm_and_takeoff(base,vehicle,altitude)
		if response:
			# base.send("Moving forward in the x direction")
			# send_ned_velocity(vehicle, .1, 0, 0, 3)
			base.send('Waiting')
			time.sleep(5)
			base.send("Landing...")
			vehicle.mode = 'LAND'
	else:
		base.send("Vehicle is armed or takeoff height is above 25m, cannot begin new mission.")
	
def takeoff(vehicle):
	response = arm_and_takeoff(base,vehicle,1)
	if response:
		base.send("Takeoff complete. Waiting for next command...")

# def move(x,y,z,t):
# 	base.send("({}, {}, {}, {})".format(x, y, z, t))

# def land_on_base(vehicle):
# 	position_vec = pixy.get_base_position()
# 	if position_vec = None:
# 	else:


# This can take a while
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, baud=921600)

base = bluetooth.Connection()
bluetooth_listener = threading.Thread(name='bluetooth_listener', target=bluetooth_listener, args=(base,vehicle))
bluetooth_listener.start()
