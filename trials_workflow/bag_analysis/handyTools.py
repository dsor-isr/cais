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

def nestedGetAttribute(obj, config_field):
    # if the config_field is a single string
    if type(config_field) != list:
        return getattr(obj, config_field)

    # if the config field is a list of strings, we need to nest the attributes
    obj_iter = obj
    for attr in config_field:
        field = getattr(obj_iter, attr)
        obj_iter = field

    return field