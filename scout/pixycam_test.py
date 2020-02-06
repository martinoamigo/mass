from __future__ import print_function
import pixy 
from ctypes import *
from pixy import *
import time

pixy.init()
pixy.change_prog("color_connected_components")

radius = 30
x_center = 158    #center of cam in x dir
y_center = 104    #center of cam in y dir

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

blocks = BlockArray(100)

while 1:
  count_in_frame = pixy.ccc_get_blocks(100, blocks)

  if count_in_frame > 0:
    for i in range (0, count_in_frame):
        #   print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[i].m_signature, blocks[i].m_x, blocks[i].m_y, blocks[i].m_width, blocks[i].m_height))
        target_block = blocks[i] # temporarily choose the last block in the frame as the target

    if target_block.m_x < lower_x:
        # brightness = map(lower_x - target_block.m_x, 0, lower_x, 255, 0)
        print("Left")

    if target_block.m_x > upper_x:
        # brightness = map(target_block.m_x - upper_x, 0, upper_x, 255, 100)
        print("Right")

    if target_block.m_y < upper_y:
        # brightness = map(upper_y - target_block.m_y, 0, upper_y, 255, 100)
        print("Up")

    if target_block.m_y > lower_y:
        # brightness = map(target_block.m_y - lower_y, 0, lower_y, 255, 100)
        print("Down")

    if target_block.m_x < upper_x and target_block.m_y > upper_y and target_block.m_x > lower_x and target_block.m_y < lower_y:
    	print("Centered, lower.")
    time.sleep(1)
    
  
