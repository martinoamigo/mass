from picamera import PiCamera
from time import sleep
import datetime
import os

camera = PiCamera()

def Pic():
    camera.capture(path + '/' + time)
    return

def Vid():
    length = int(input("Length of Video in seconds: "))
    camera.start_recording(path + '/' + time)
    sleep(length)
    camera.stop_recording()
    return


now = datetime.datetime.now() # Current Date and Time
date = now.strftime('%Y_%m_%d')
time = now.strftime('%Hh_%Mm_%Ss')
print(date, time)

path = 'Desktop/Media/' + date
try:
    os.mkdir(path)
except OSError:
    print('Creation of directory ', path, ' failed')

while True:
    action = input('Input action letter: /nP for Picture/nV for Video/nExit (or anything else) to leave Camera mode:')
    if action is 'P':
        Pic()
    elif action is 'V':
        Vid()
    else: break
