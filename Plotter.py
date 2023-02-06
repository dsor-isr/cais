import rosbag
import os
import time
from Bag import Bag
from handyTools import *
from PlotData import PlotData
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
  def __init__(self, bag_list, configs, configs_parent_dirs):
    self.bag_list = bag_list
    self.configs = configs
    self.configs_parent_dirs = configs_parent_dirs

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

  def __makePlotFromPlotData(self, plot_data, path_to_plots, config_type, bag_filename, overall_folder):
    # check if there are any curves to plot
    if plot_data.curves is None:
      return

    # create figure data
    trace_data = []

    for curve in plot_data.curves:
      trace_data.append(go.Scatter(x=curve["x"], 
                                   y=curve["y"], 
                                   mode=curve["plot_marker"], 
                                   name=curve["label"]))

    # page title
    page_title = plot_data.title + ": \n"
    try:
      for topic_name in [curve["y_topic"] for curve in plot_data.curves]:
        page_title += topic_name + " \n"
    except:
      print("[Warning] " + config_type + "(" + plot_data.id + "): failed to create page title.")

    layout = dict(title = page_title,
                  xaxis=dict(title=plot_data.axes_labels["x"], nticks=50, tickformat='%H:%M:%S'), 
                  yaxis=dict(title=plot_data.axes_labels["y"], scaleanchor = "x", scaleratio = 1))
    fig_data = dict(data=trace_data, layout=layout)

    # topic name from the first curve in the plot
    try:
      topic_name = plot_data.curves[0]["y_topic"][0]
    except:
      topic_name = ""

    # save plot in corresponding folder
    folder = path_to_plots + "/" + \
            bag_filename + "/" + \
            overall_folder + "/" + \
            self.configs_parent_dirs[config_type] + "/" + \
            config_type + self.__getIdFromConfigTopic(topic_name) + "/"
    try:  # else already exists
      os.makedirs(folder)
    except:
      pass

    py.offline.plot(fig_data, filename=folder + plot_data.id + ".html", auto_open=False)

  def __makePlotsFromConfig(self, bag, config_type, path_to_plots):
    # get bag filename without ".bag"
    bag_filename = bag.filename[:bag.filename.rfind('.')]

    # for each specified plot in the yaml file
    try:
      for plot_key, plot_value in self.configs[config_type]["plots"].items():
        plot_data = PlotData(bag, config_type, plot_key, plot_value)
        self.__makePlotFromPlotData(plot_data, path_to_plots, config_type, bag_filename, "Overall")
    except:
      # ignores yaml files with no info
      pass
          
  # Public Methods

  def createPlots(self):
    # create plots for each bag
    for bag in self.bag_list:
      # get path to plots folder
      path_to_plots = self.__getPathToPlotsFolder(bag.bag_path)

      # for each config file
      for config_type in self.configs.keys():
        self.__makePlotsFromConfig(bag, config_type, path_to_plots)