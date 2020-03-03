from __future__ import print_function
import os,inspect
import sys
import threading
import time
import math
from ctypes import Structure, c_uint

import utils.bluetooth as bluetooth 
from utils.flight_utils import *
import utils.pixy as pixy

connection_string = '/dev/serial0'
pixy.init()
pixy.change_prog("color_connected_components")

radius = 30
x_center = 158    #center of cam in x dir
y_center = 104    #center of cam in y dir

base_center_target = (158, 104)

upper_x = x_center + radius
lower_x = x_center - radius
upper_y = y_center - radius
lower_y = y_center + radius

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]

blocks = pixy.BlockArray(100)

def get_base_position():
    objects_seen = pixy.ccc_get_blocks(100, blocks)
        
    #TODO: add procedure for if there is no base detected

    if objects_seen > 0:
        lowest_distance_to_center = 1000
        target_block = None
        # choose the most centered block in the frame
        for i in range (0, objects_seen):
            if blocks[i].m_signature == 1:
                #   print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[i].m_signature, blocks[i].m_x, blocks[i].m_y, blocks[i].m_width, blocks[i].m_height))
                distance_to_center = math.sqrt((blocks[i].m_x - x_center)**2 + (blocks[i].m_y - y_center)**2)  
                if distance_to_center < lowest_distance_to_center:
                    lowest_distance_to_center = distance_to_center
                    target_block = blocks[i] 
        
        if target_block:
			position_vector = (target_block.m_x, target_block.m_y)
        	# position_vector = (target_block.m_x - base_center_target[0], base_center_target[1] - target_block.m_y)
            return position_vector


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
		base.send("Stabilize signal received.")
		vehicle.mode = 'STABILIZE'

	elif message == 'guided':
                base.send("Guided signal received.")
                vehicle.mode = 'GUIDED'

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
		except:
			base.send("Invalid arguements for 'move'. Required format is 'move x, y, z, t'")
		try:
			send_ned_velocity(vehicle, args[1],  args[2], args[3], args[4])
		except:
			base.send("Move command failed with '{}'".format(sys.exc_info()[0]))
	
	else:
		base.send("Command not recognized. Valid commands are: \n- mission \n- takeoff (height in meters)\n- land\n- rtl\n- loiter\n- stabilize\n- guided\n- disarm\n- move x y z t")
		return

def start_mission(vehicle):                                                                                                                                                                                                                                                
	# Begin mission
	response = arm_and_takeoff(base,vehicle,2)
	if response:
		base.send("Precision landing...")
		land_on_base(vehicle)
	
def takeoff(vehicle, altitude):
	if altitude < 25:
		response = arm_and_takeoff(base,vehicle,altitude)
		if response:
			base.send("Takeoff complete. Waiting for next command...")
	else:
		base.send("Takeoff height is above 25m, takeoff refused.")

def land_on_base(vehicle):
	landed = False
	# vehicle.mode = 'LAND'
	for _ in range(10000):
		position_vec = get_base_position()
		if position_vec == None:
			# TODO: move up, down, or rotate
			base.send("Base not seen...")
			pass
		else:
			base.send("Sending MAVLINK message 'land({}, {})'".format(position_vec[0], position_vec[1]))
			send_land_message(vehicle, position_vec[0], position_vec[1])
	base.send("Landing loop ended...")

# This can take a while
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, baud=921600)

base = bluetooth.Connection()
bluetooth_listener = threading.Thread(name='bluetooth_listener', target=bluetooth_listener, args=(base,vehicle))
bluetooth_listener.start()
