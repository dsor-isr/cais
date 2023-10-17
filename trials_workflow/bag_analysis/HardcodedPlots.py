import rosbag
import time
from Bag import Bag
from PlotData import PlotData
# from handyTools import *
# import datetime
import pandas as pd

def tensionPack(bag, tension_pack_nr):
  plot_data = PlotData(bag, "", "tension_pack" + tension_pack_nr, "", [], to_load = False)

  plot_data.title = "Tension per cell in Pack " + tension_pack_nr
  plot_data.axes_labels["x"] = "Time"
  plot_data.axes_labels["y"] = "Tension [mV]"

  # get x/y curves data
  # check through all topics in the bag
  for topic_name in bag.topics_list:
    # if topic is found
    if "/bat_monit/raw" in topic_name:
      print("Found topic: " + topic_name)

      # initialise each curve as dict
      plot_data.curves = [dict() for i in range(7)]

      # set y_topic as the data's topic
      for i in range(7):
        plot_data.curves[i]["y_topic"] = topic_name
        plot_data.curves[i]["x_topic"] = topic_name
        plot_data.curves[i]["plot_marker"] = "lines"
        plot_data.curves[i]["label"] = "cell" + str(i+1)
        plot_data.curves[i]["y"] = []
        plot_data.curves[i]["x"] = []

      # extract message from the topic data
      for topic, msg, t in bag.getBagTopicData(topic_name):
        # add new topic used for this axis
        axis_data_topic = topic

        # parse raw string
        raw_splited = msg.sentence.split(',')

        # if message has the correct information
        if len(raw_splited) > 7:
          if raw_splited[1] == tension_pack_nr:
            for i in range(7):
              plot_data.curves[i]["y"].append(int(raw_splited[i+3]))
              plot_data.curves[i]["x"].append(pd.to_datetime(t.to_sec(), unit='s'))

      break

  return [plot_data, "drivers/batMonit"]

def getHardcodedPlotsData(bag):
  # list for plot data and config_types
  plot_data_list = list()

  # add here the new hardocoded plots
  try:
    plot_data_list.append(tensionPack(bag, "1"))
  except:
    print("[FAILED] Hardcoded Plots (tension pack 1) : " + bag.filename)

  try:
    plot_data_list.append(tensionPack(bag, "2"))
  except:
    print("[FAILED] Hardcoded Plots (tension pack 2) : " + bag.filename)

  # return the list
  return plot_data_list