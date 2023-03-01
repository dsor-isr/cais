import rosbag
import time
from Bag import Bag
from handyTools import *
import datetime
import pandas as pd

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

  def __foundDesiredTopic(self, topic_name, config_topic, config_field, plot_value, axis, i):
    # if the topic to be plotted (config) is not in the current topic being checked
    if config_topic.lower() not in topic_name.lower():
      return False

    # create key with currently checked topic, config field and index
    topic_config_index_key = [topic_name, config_field]

    # if indexes are not specified for this axis...
    if "indexes" not in plot_value["axes"][axis].keys():
      topic_config_index_key.append(None)
    else: # otherwise
      index = plot_value["axes"][axis]["indexes"][i]
      topic_config_index_key.append(index)

    # if the currently checked topic, config field and index have already been analysed
    if topic_config_index_key in self.topics_read_list:
      return False

    # since at this point config_topic is in the topic_name, let's know what's before and after
    try:
      before, after = topic_name.lower().split(config_topic.lower())
    except:
      # if failed, let it consider the topic has been found
      return True
    
    # print("config_topic: " + config_topic + "\ttopic_name: " + topic_name + " AFTER: " + after)
    
    # check if there is anything other than the vehicle name before the config topic 
    # (== occurences of "/*" is 0 or 1, * being a wildcard for any character)
    nr_of_slashes = 0 # number of '/' with characters after
    for i, c in enumerate(before):
      try:
        if (c == '/') and (i+1 < len(before)):
          nr_of_slashes += 1
      except:
        pass
    
    if nr_of_slashes > 1:
      return False

    # check if there is anything after the config_topic
    if len(after) != 0:
      if (after[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
        return False

    return True

  def __getIndexedValueIfNeeded(self, new_value, plot_value, axis, i):
    # if indexes are not specified for this axis...
    if "indexes" not in plot_value["axes"][axis].keys():
      return new_value, None
    
    # if indexes are specified...
    # get index for this curve
    index = plot_value["axes"][axis]["indexes"][i]

    # if index is not specified for this curve
    if index is None:
      return new_value, None

    # return the indexed value since the index is not None
    return new_value[index], index

  def __getDataFromConfigTopic(self, axis, bag, config_topic, config_field, plot_value, i):
    axis_data = []
    axis_data_topic = None
    index = None

    # check through all topics in the bag
    for topic_name in bag.topics_list:
      # print(topic_name)
      # if a topic to be plotted is found and has not been plotted for the current plot configuration
      if self.__foundDesiredTopic(topic_name, config_topic, config_field, plot_value, axis, i):

        print("Found topic: " + topic_name)

        # extract message from the topic data
        for topic, msg, t in bag.getBagTopicData(topic_name):
          # add new topic used for this axis
          axis_data_topic = topic
          
          # add value to list
          try:
            # value
            value = nestedGetAttribute(msg, config_field)

            # updated value
            new_value, index = self.__getIndexedValueIfNeeded(value, plot_value, axis, i)

            axis_data.append(new_value)
          except:
            print("[Error] Topic data msg has no attribute named " + config_field + ".")
            axis_data = None
            break

        return axis_data, axis_data_topic, index, False

    # did not find any more topics with that config_topic or did not find any, but reached the end
    # of all topics in the bag list
    return None, None, index, True

  def __getTimeDataFromConfigTopic(self, bag, config_topic):
    axis_data = []

    # check through all topics in the bag
    for topic_name in bag.topics_list:
      # if a topic to be plotted is found
      if config_topic in topic_name:
        # extract message from the topic data
        for topic, msg, t in bag.getBagTopicData(topic_name):
          # add value to list
          # axis_data.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
          # axis_data.append(t.to_sec())
          # axis_data.append(datetime.timedelta(seconds=int(t.to_sec()), microseconds=int((t.to_sec()%1)*1000000)))
          axis_data.append(pd.to_datetime(t.to_sec(), unit='s'))
        return axis_data, "time"

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
    
    # if x axis is specified
    if plot_value["axes"]["x"] is not None:
      # if the number of topics or fields is different for the x axis, there's an error
      if len(plot_value["axes"]["x"]["fields"]) != nr_curves or len(plot_value["axes"]["x"]["topics"]) != nr_curves:
        print("[Error] " + config_type + "(" + self.id + "): different number of topics and fields.")
        self.curves = None
        return
      
      # if indexes are specified for the x axis...
      if ("indexes" in plot_value["axes"]["x"].keys()):
        # ... but the length doesn't match the number of curves, there's an error
        if len(plot_value["axes"]["x"]["indexes"]) != nr_curves:
          print("[Error] " + config_type + "(" + self.id + "): x indexes length is not correct.")
          self.curves = None
          return

    # if indexes are specified for the y axis...
    if "indexes" in plot_value["axes"]["y"].keys():
      # ... but the length doesn't match the number of curves, there's an error
      if len(plot_value["axes"]["y"]["indexes"]) != nr_curves:
        print("[Error] " + config_type + "(" + self.id + "): y indexes length is not correct.")
        self.curves = None
        return
      
    # if the number of plot_markers is different from the number of curves
    if len(plot_value["plot_markers"]) != nr_curves:
      print("[Warning] " + config_type + "(" + self.id + "): different number of plot_markers. Default configuration used (lines).")
      
      # define default value
      plot_value["plot_markers"] = []
      for i in range(nr_curves):
        plot_value["plot_markers"].append("lines")

    print("YAML CONFIG: " + config_type + "-> " + self.id)

    # add curves' y values (i is index)
    for i, (config_topic, config_field, plot_marker) in enumerate(zip(plot_value["axes"]["y"]["topics"], plot_value["axes"]["y"]["fields"], plot_value["plot_markers"])):
      new_curve = dict()
      new_curve["y"], new_curve["y_topic"], index_read, self.flag_all_topics_read = self.__getDataFromConfigTopic("y", bag, config_topic, config_field, plot_value, i)

      # update list of topics/fields/indexes read for y axis
      self.topics_read_list.append([new_curve["y_topic"], config_field, index_read])
      # self.topics_read_list.append([new_curve["y_topic"], config_field])

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
      for i, (curve, config_topic, config_field) in enumerate(zip(self.curves, plot_value["axes"]["x"]["topics"], plot_value["axes"]["x"]["fields"])):
        curve["x"], curve["x_topic"], _, __ = self.__getDataFromConfigTopic("x", bag, config_topic, config_field, plot_value, i)

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