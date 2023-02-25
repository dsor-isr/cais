import rosbag
import time
from Bag import Bag
from handyTools import *
from datetime import datetime

class PlotData(object):

  # Constructor
  def __init__(self, bag, config_type, plot_key, plot_value, topics_read_list):
    self.id = plot_key
    self.title = None
    self.curves = []
    self.axes_labels = dict()
    self.topics_read_list = topics_read_list
    self.flag_all_topics_read = False

    # get all data into the appropriate structure
    self.__loadPlotData(bag, config_type, plot_value)
    

  # Private Methods

  def __foundDesiredTopic(self, topic_name, config_topic, config_field):
    # if the topic to be plotted (config) is not in the current topic being checked
    if config_topic.lower() not in topic_name.lower():
      return False

    # if the currently checked topic and config filed have already been analysed
    if [topic_name, config_field] in self.topics_read_list:
      return False

    # since at this point config_topic is in the topic_name, let's know what's before and after
    try:
      before, after = topic_name.lower().split(config_topic.lower())
    except:
      # if failed, let it consider the topic has been found
      return True
    
    # check if there is anything other than the vehicle name before the config topic 
    # (== occurences of "/*" is 0 or 1, * being a wildcard for any character)
    nr_of_slashes = 0 # number of '/' with characters after
    for c in before:
      try:
        if (c == '/') and (before.index(c)+1 >= len(before)):
          nr_of_slashes += 1
      except:
        pass
    
    if nr_of_slashes > 1:
      return False

    # check if there is anything after the config_topic
    if len(after) != 0:
      if (after[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
        return False

    print("config_topic: " + config_topic + "\ttopic_name: " + topic_name + " AFTER: " + after)

    return True

  def __getDataFromConfigTopic(self, bag, config_topic, config_field):
    axis_data = []
    axis_data_topic = None

    # check through all topics in the bag
    for topic_name in bag.topics_list:
      # print(topic_name)
      # if a topic to be plotted is found and has not been plotted for the current plot configuration
      if self.__foundDesiredTopic(topic_name, config_topic, config_field):

        print("Found topic: " + topic_name)

        # extract message from the topic data
        for topic, msg, t in bag.getBagTopicData(topic_name):
          # add new topic used for this axis
          axis_data_topic = topic
          
          # add value to list
          try:
            axis_data.append(nestedGetAttribute(msg, config_field))
          except:
            print("[Error] Topic data msg has no attribute named " + config_field + ".")
            axis_data = None
            break

        return axis_data, axis_data_topic, False

    # did not find any more topics with that config_topic or did not find any, but reached the end
    # of all topics in the bag list
    return None, None, True

  def __getTimeDataFromConfigTopic(self, bag, config_topic):
    axis_data = []

    # check through all topics in the bag
    for topic_name in bag.topics_list:
      # if a topic to be plotted is found
      if config_topic in topic_name:
        # extract message from the topic data
        for topic, msg, t in bag.getBagTopicData(topic_name):
          # add value to list
          axis_data.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])       
        return axis_data, None

    # did not find any topic with that config_topic
    return None, None

  def __getPlotLabel(self, new_curve_y_topic, config_field, x_axis_is_time):
    # the label starts as the string after the last "/" in the topic name
    label = new_curve_y_topic.split("/")[-1] + "."
    
    # add to the label the fields of the config_field
    if type(config_field) == list:
      label += '.'.join(config_field)
    else:
      label += config_field

    # if x axis is not time, then the label should not be specific to the y_topic
    # as a workaround, we suppose that taking the string after the last "." in the label
    # generalises it
    if not x_axis_is_time:
      label = label[:label.rfind(".")]

    return label

  def __loadPlotData(self, bag, config_type, plot_value):    
    # number of curves in the plot
    try:
      nr_curves = len(plot_value["axes"]["y"]["topics"])
    except: # if no y values are specified for this plot
      print("[Error] " + config_type + "(" + self.id + "): no curves were specified.")
      self.curves = None
      return

    # if the number of topics and fields is different for the y axis, there's an error
    if len(plot_value["axes"]["y"]["fields"]) != nr_curves:
      print("[Error] " + config_type + "(" + self.id + "): different number of topics and fields.")
      self.curves = None
      return
    
    # if the number of topics or fields is different for the x axis, there's an error
    if plot_value["axes"]["x"] is not None:
      if len(plot_value["axes"]["x"]["fields"]) != nr_curves or len(plot_value["axes"]["x"]["topics"]) != nr_curves:
        print("[Error] " + config_type + "(" + self.id + "): different number of topics and fields.")
        self.curves = None
        return
    
    # if the number of plot_markers is different from the number of curves
    if len(plot_value["plot_markers"]) != nr_curves:
      print("[Warning] " + config_type + "(" + self.id + "): different number of plot_markers. Default configuration used (lines).")
      
      # define default value
      plot_value["plot_markers"] = []
      for i in range(nr_curves):
        plot_value["plot_markers"].append("lines")

    print("YAML CONFIG: " + config_type)

    # add curves' y values
    for config_topic, config_field, plot_marker in zip(plot_value["axes"]["y"]["topics"], plot_value["axes"]["y"]["fields"], plot_value["plot_markers"]):
      new_curve = dict()
      new_curve["y"], new_curve["y_topic"], self.flag_all_topics_read = self.__getDataFromConfigTopic(bag, config_topic, config_field)

      # update list of topics/fields read
      self.topics_read_list.append([new_curve["y_topic"], config_field])

      # if no curve was found to be plotted
      if new_curve["y"] is None:
        # if no curve has been plotted for this plot configuration
        if len(self.topics_read_list) == 0:
          print("[Warning] " + config_type + "(" + self.id + "): no topic corresponding to the one specified was found.")
          self.curves = None
          self.flag_all_topics_read = True
          return
        # if no more curves are found for this plot configuration
        else:
          self.curves = None
          return

      # set label for this curve
      new_curve["label"] = self.__getPlotLabel(new_curve["y_topic"], config_field, plot_value["axes"]["x"] is None)

      # load plot_marker for each curve
      new_curve["plot_marker"] = plot_marker

      # add new curve to this plot
      self.curves.append(new_curve)

    # add curves' x values
    if plot_value["axes"]["x"] is None: # if x axis should be Time
      for curve, config_topic in zip(self.curves, plot_value["axes"]["y"]["topics"]):
        curve["x"], curve["x_topic"] = self.__getTimeDataFromConfigTopic(bag, curve["y_topic"])
    else: # if x axis data comes from a specific topic
      for curve, config_topic, config_field in zip(self.curves, plot_value["axes"]["x"]["topics"], plot_value["axes"]["x"]["fields"]):
        curve["x"], curve["x_topic"], _ = self.__getDataFromConfigTopic(bag, config_topic, config_field)

    # set plot title
    if plot_value["name"] is None:
      self.title = ""
      print("[Warning] " + config_type + "(" + self.id + "): no plot title was specified.")
    else:
      self.title = plot_value["name"]

    # set axes labels
    for axis in ["x", "y"]:
      # if x axis is time
      if axis == "x" and plot_value["axes"]["x"] is None:
        self.axes_labels[axis] = "Time"
        continue
      
      # if axis label was not defined
      if plot_value["axes"][axis]["label"] is None:
        self.axes_labels[axis] = ""
        print("[Warning] " + config_type + "(" + self.id + "): no label was specified for " + axis + " axis.")
      else: # otherwise
        self.axes_labels[axis] = plot_value["axes"][axis]["label"]
    
    print("New plot data added for CONFIG_TYPE: " + config_type)