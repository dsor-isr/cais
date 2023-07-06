import numpy as np
import math
from scipy import interpolate
import rosbag
import os

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
    :param topic_name: the name of the topic that we want to obtain 
    :return: all messages of the topic_name
    """
    return bag.read_messages(topic_name)

def searchInTopics(bag, topic_word):
    """ 
    :param bag: a read bag
    :return: all topic into the bag that contain the word topic_word
    """
    return [name for name in bag.get_type_and_topic_info()[1].keys() if topic_word in name]


def createFlagTopicVec(flag_topic):
    """
    Get messages from Flag topic
    :param flag_topic: the flag topic name
    :return two vectors containg the Flag value and the time
    """
    flag_value_vec = []
    flag_time_vec = []
    
    for topic, msg, t in flag_topic:
        flag_value_vec.append(msg.data)
        flag_time_vec.append(t)

    return flag_value_vec, flag_time_vec

def createMissionsVec(flag_topic, pattern):
    """
    Find in the Flag messages the pattern for the mission, and save the start time and end time of the mission
    """
    missions = []

    flag_value_vec, flag_time_vec = createFlagTopicVec(flag_topic)

    for i in range(0, len(flag_value_vec)):
        if flag_value_vec[i] == pattern[0] and flag_value_vec[i:i+len(pattern)] == pattern:
            if (i < len(flag_value_vec)) and (i+len(pattern) <= len(flag_value_vec)):
                missions.append([flag_time_vec[i+1], flag_time_vec[i+len(pattern)-1]])

    return missions

def createMissionBags(bag, flag_topic, pattern, datafolder):
        """
        Divide the .bag into a small mission bag according the choosen pattern
        The output bag have a especific name
        """
        missions = createMissionsVec(flag_topic, pattern)
        
        # if there is no missions in the entire bag
        if not missions:
            return

        # create the missions folder
        try:  # else already exists
            os.makedirs(datafolder)
        except:
            pass

        j = 1
        outbag = rosbag.Bag(datafolder + "/%d_mission.bag" % j, 'w')

        for topic, msg, t in bag.read_messages():
            if t >= missions[j-1][0]:
                outbag.write(topic, msg, t)
            if t == missions[j-1][1]:
                outbag.close()
                if j < len(missions):
                    j+=1
                    outbag = rosbag.Bag(datafolder + "/%d_mission.bag" % j, 'w')
                else:
                    return

def getNameOfVehicle(bag):
    # Get name of the vehicle
    if searchInTopics(bag, 'Flag')[0]:
        return searchInTopics(bag, 'Flag')[0].split("/")[1]
