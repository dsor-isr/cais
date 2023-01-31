import rosbag
import os
import time
from Bag import Bag
from handyTools import *
import plotly.graph_objs as go
import plotly.offline as py
from datetime import datetime

# I wanted to name this class "Baggy Plotter",
# in a reference to our favourite scarred wizard,
# but didn't, in an effort to make this understandable
# for future generations.
# - ecunhado
class Plotter(object):

  # Constructor
  def __init__(self, bag_list, configs):
    self.bag_list = bag_list
    self.configs = configs

  # Private Methods

  def __getPathToPlotsFolder(self, bag_path):
    # here it is assumed that the bag_path has a format of type:
    # /home/{{username}}/trials_raw/{{day_of_trials}}/vehicles/{{vehicle_name}}/ROSData/{{bag_name}}.bag
    # ex: /home/ecunhado/trials_raw/20230120/vehicles/mblack/ROSData/mblack__2023-01-20-09-59-09.bag
    
    # get string to subtract to the original one
    str1 = bag_path.split("/vehicles/")[1]
    str2 = str1[str1.find("/")+1:]
    
    # compute path to plots folder
    path_to_plots = bag_path.replace(str2, '') + "plots/"

    # create path to plots folder
    try:  # else already exists
      os.makedirs(path_to_plots)
    except:
      pass

    return path_to_plots

  def __getIdFromConfigTopic(self, topic_name):
    string_list = topic_name.split("/")[::-1] # reversed list of strings
    it = 0 # iterations

    for string in string_list:
      it += 1
      nr = ""
      for char in string:
        # if char is a digit append it to string
        if char.isdigit():
          nr += char
      
      # if a number was found
      if nr:
        return nr
      
      # if string is tooooo far away (prevent getting index of vehicle)
      # sorry for hard code
      if it > 2:
        return ""

    return ""

  def __getPlotData(self, bag, topic_name, config_type, plot_type):
    plots_data = dict()
    time_vec = []
    y_values = dict()

    # load all info for plots from the same topic (for this plot_type)
    for topic, msg, t in bag.data[topic_name]:
      # add data to time vector
      try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
      except: pass
      # except: print("Did not save time in vector")

      # for each plot that needs to be plotted according to the yaml file:
      # add data to y values
      plot_configs_list = self.configs[config_type][plot_type]["plots"]
      for plot in plot_configs_list:
        # key that indexes dictionary with data for y axis of plots
        plot_key = plot["name"]

        # initialise list if not done before
        if plot_key not in y_values.keys():
          y_values[plot_key] = []
        
        # append new value to corresponding list
        try:
          if any(angle in plot_key.lower() for angle in ["roll", 'pitch', 'yaw']):
            y_values[plot_key].append(wrapTo360(getattr(msg, plot["field"]))) # if data are angles, wrap to 360
          else:  
            y_values[plot_key].append(getattr(msg, plot["field"])) # otherwise add the value without any processing
        except: pass
        # except: print("Did not save attribute from msg")
    
    # save time vector and y_values to be plotted in a dict
    plots_data["time"] = time_vec
    plots_data["y_values"] = y_values

    return plots_data

  def __makePlotsFromPlotData(self, plots_data, path_to_plots, topic_name, config_type, plot_type, bag_filename, overall_folder):
    # loop through all plots in plots_data
    for key, value in plots_data["y_values"].items():
      # if value is empty pass
      if not value:
        break

      # create figure data
      trace_data = go.Scatter(x=plots_data["time"], 
                              y=value, 
                              mode='lines', 
                              name=key)
      layout = dict(title = topic_name, 
                    xaxis=dict(title='Time', 
                    nticks=50, 
                    tickformat='%H:%M:%S'), 
                    yaxis=dict(title=key, scaleanchor = "x", scaleratio = 1))
      fig_data = dict(data=[trace_data], layout=layout)

      # save plot in corresponding folder
      folder = path_to_plots + "/" + \
              bag_filename + "/" + \
              overall_folder + "/" + \
              config_type + "/" + \
              plot_type + self.__getIdFromConfigTopic(topic_name) + "/"
      try:  # else already exists
          os.makedirs(folder)
      except:
          pass

      py.offline.plot(fig_data, filename=folder + key + ".html", auto_open=False)

  def __makePlotsFromConfig(self, bag, config_type, path_to_plots):
    # config type is the name of the yaml file
    # plot_type is the many specified types of plots in the yaml file

    # get bag filename without ".bag"
    bag_filename = bag.filename[:bag.filename.rfind('.')]

    # for every topic in the bag
    for topic_name in bag.topics_list:
      # check through all specified plot types in the yaml file
      for plot_type in list(self.configs[config_type].keys()):
        topic_name_from_config = self.configs[config_type][plot_type]["topic"]
        if topic_name_from_config in topic_name:
          # found a topic_name that needs plotting!
          print(topic_name)
          plots_data = self.__getPlotData(bag, topic_name, config_type, plot_type)
          self.__makePlotsFromPlotData(plots_data, path_to_plots, topic_name, config_type, plot_type, bag_filename, "Overall")
                
          
  # Public Methods

  def createPlots(self):
    for bag in self.bag_list:
      # get path to plots folder
      path_to_plots = self.__getPathToPlotsFolder(bag.bag_path)

      for config_type in self.configs.keys():
        self.__makePlotsFromConfig(bag, config_type, path_to_plots)