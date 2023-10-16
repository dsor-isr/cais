import numpy as np
import math
from scipy import interpolate
import rosbag

def wrapTo2PI(rad):
    """
    wrap angle in radians between 0 and 2pi
    :param rads: angle in radians
    :return: rad [0 2pi]
    """
    return rad % (2*math.pi)

def wrapTo360(deg):
    """
    wrap angle in degrees between 0 and 360
    :param deg: angle in degrees
    :return: deg [0 360]
    """
    return deg % 360

def rms(x_gt, y_gt, x_other, y_other):
    """
    :param x_gt: points that are the x of ground truth
    :param y_gt: points that are the y of ground truth
    :param x_other: points that are the x of the points to be compared with ground truth
    :param x_other: points that are the y of the points to be compared with ground truth
    :return: root mean square error
    """
    x_other, y_other = interpolate_path(np.array(x_gt), np.array(y_gt), np.array(x_other), np.array(y_other))
    return np.ndarray.tolist(np.sqrt((np.array(x_gt)-np.array(x_other))**2+(np.array(y_gt)-np.array(y_other))**2))

def interpolate_path(x_gt, y_gt, x_other, y_other):
    """
    :param x_gt: points that are the x of ground truth
    :param y_gt: points that are the y of ground truth
    :param x_other: points that are the x of the other
    :param x_other: points that are the y of the other
    :return: two vectors with same size
    """
    fx = interpolate.interp1d(np.arange(x_other.size), x_other)
    fy = interpolate.interp1d(np.arange(y_other.size), y_other)
    return np.array(fx(np.linspace(0, x_other.size-1, x_gt.size, endpoint=True))), np.array(fy(np.linspace(0, y_other.size-1, y_gt.size, endpoint=True)))

def readBag(bag_name):
    """ 
    :param bag_name: name of the .bag file
    :return: a read bag
    """
    return rosbag.Bag(bag_name)

def getTopics(bag):
    """ 
    :param bag: a read bag
    :return: all topics into the bag
    """
    return bag.get_type_and_topic_info()[1].keys()
    
def findTopic(bag, topic_name):
    """ 
    :param bag: a read bag
    :param topic_name: the name of the topic that we wanto to obtain 
    :return: all messages of the topic_name
    """
    return bag.read_messages(topic_name)

def searchInTopics(bag, topic_word):
    """ 
    :param bag: a read bag
    :return: all topic into the bag that contain the word topic_word
    """
    return [name for name in bag.get_type_and_topic_info()[1].keys() if topic_word in name]
