import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Connect to the Vehicle (in this case a simulator running the same computer)
vehicle = connect('/dev/serial0', wait_ready=True, baud=921600)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    # base.send("Basic pre-arm checks")
    # while not vehicle.is_armable:
    #     print(" Waiting for vehicle to be armable...")
    #     time.sleep(1)

    # base.send("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        # base.send(" Waiting for arming...")
        time.sleep(1)

    # base.send("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            # base.send("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(10)