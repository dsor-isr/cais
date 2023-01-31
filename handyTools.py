import numpy as np
import math
from scipy import interpolate
import rosbag

def wrapTo360(deg):
    """
    wrap angle in degrees between 0 and 360
    :param deg: angle in degrees
    :return: deg [0 360]
    """
    return deg % 360