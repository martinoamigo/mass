from __future__ import print_function
from ctypes import Structure, c_uint
import time
import math
if __name__ == "__main__":
    import pixy
else:
    from . import pixy


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
            position_vector = (target_block.m_x - base_center_target[0], base_center_target[1] - target_block.m_y)
            return position_vector

