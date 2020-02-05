import os,sys,inspect
from flight_utils import *
import sys
import multiprocessing
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
# import utils.bluetooth 

connection_string = '127.0.0.1:14550'
sitl = None

def bluetooth_listener():
	scout_bt_mac_addr = 'DC:A6:32:3B:BD:A8' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
	port = 3 
	backlog = 1
	size = 1024

	# Connect to bluetooth
	# client, socket = bluetooth.accept_base_connection()
	# bluetooth.listen(client, socket)

def flight_controller():
	# Connect to the Vehicle
	print('Connecting to vehicle on: %s' % connection_string)
	vehicle = connect(connection_string, wait_ready=True)

	# Begin mission
	arm_and_takeoff(vehicle,10)
	print("Moving north at 3m/s for 5s")
	send_ned_velocity(vehicle, 3, 0, 0, 5)
	print('Return to launch')
	vehicle.mode = 'RTL'

	print("Close vehicle object")
	vehicle.close()

bluetooth_listener = multiprocessing.Process(name='bluetooth_listener', target=bluetooth_listener)
flight_controller = multiprocessing.Process(name='flight_controller', target=flight_controller)
bluetooth_listener.start()
flight_controller.start()