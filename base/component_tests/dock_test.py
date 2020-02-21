import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Pinouts for Relay Connectors

sol_act1 = 31
sol_act2 = 33

lin_act1 = 35
lin_act2 = 37

# Set Pins
GPIO.setup(sol_act1, GPIO.OUT)
GPIO.setup(sol_act2, GPIO.OUT)
GPIO.setup(lin_act1, GPIO.OUT)
GPIO.setup(lin_act2, GPIO.OUT)

# Clear Pins
GPIO.output(sol_act1, 1)
GPIO.output(sol_act2, 1)
GPIO.output(lin_act1, 1)
GPIO.output(lin_act2, 1)
#inout
GPIO.output(sol_act1, 0)
GPIO.output(sol_act2, 0)
GPIO.output(lin_act1, 1)
GPIO.output(lin_act2, 0)
time.sleep(10)
GPIO.output(lin_act1, 0)
GPIO.output(lin_act2, 1)
GPIO.output(sol_act1, 1)
GPIO.output(sol_act2, 1)
time.sleep(10)



GPIO.cleanup()


