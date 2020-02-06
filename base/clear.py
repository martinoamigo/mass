import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Pinouts for Relay Connectors
comp       = 16
safety_sol = 13
vent_sol   = 11
launch_sol = 15

# Set Pins
GPIO.setup(comp, GPIO.OUT)
GPIO.setup(safety_sol, GPIO.OUT)
GPIO.setup(vent_sol, GPIO.OUT)
GPIO.setup(launch_sol, GPIO.OUT)

# Clear Pins
GPIO.output(comp, 1)
GPIO.output(safety_sol, 1)
GPIO.output(vent_sol, 1)
GPIO.output(launch_sol, 1)

GPIO.cleanup()
