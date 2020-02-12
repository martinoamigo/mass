from picamera import PiCamera
from time import sleep
import datetime
import os

camera = PiCamera()

def Pic():
    camera.capture(path + '/' + time + '.jpg')
    print('Picture saved: ', path + '/' + time + '.jpg')


def Vid():
    length = int(input("Length of Video in seconds: "))
    camera.start_recording(path + '/' + time + '.h264')
    print('Shleep......')
    sleep(length)
    print('AWAKE!!!!!!')
    camera.stop_recording()
    print('Video saved: ', path + '/' + time + '.h264')


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
    action = input('\nInput action letter: \nP for Picture\nV for Video\nAnything else to leave Camera mode:')
    now = datetime.datetime.now() # Current Date and Time
    time = now.strftime('%Hh_%Mm_%Ss')
    if action.upper() == 'P':
        Pic()
    elif action.upper() == 'V':
        Vid()
    else: break
