import rosbag
import os
import time
from Bag import Bag
from Mission import Mission
from handyTools import *
from PlotData import PlotData
from HardcodedPlots import getHardcodedPlotsData
import plotly.graph_objs as go
import plotly.offline as py
from datetime import datetime
import rospy

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
    #
    # ex: bag_path = /home/ecunhado/trials_raw/20230120/vehicles/mblack/ROSData/mblack__2023-01-20-09-59-09.bag
    #     str1 = mblack/ROSData/mblack__2023-01-20-09-59-09.bag
    #     str2 = ROSData/mblack__2023-01-20-09-59-09.bag
    #     path_to_plots = /home/ecunhado/trials_raw/20230120/vehicles/mblack/plots/
    
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
    max_it = len(string_list) - 2

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
      if it >= max_it:
        return ""

    return ""

  def __getLayoutXAxis(self, plot_data, nrticks):
    # if x axis is time
    if any(curve["x_topic"] == "time" for curve in plot_data.curves):
      # return the x axis layout defining the correct labels for each tick in the plot (%H:%M:%S.%f)
      return dict(title=plot_data.axes_labels["x"], nticks=nrticks, tickformat='%H:%M:%S:%f')

    # if x axis is not time, return the usual layout without specified tick labels
    return dict(title=plot_data.axes_labels["x"], nticks=nrticks)

  def __getLayoutYAxis(self, plot_data):
    # if x axis is time
    if any(curve["x_topic"] == "time" for curve in plot_data.curves):
      return dict(title=plot_data.axes_labels["y"])
    
    # scale if the x axis is not time
    return dict(title=plot_data.axes_labels["y"], scaleanchor = "x", scaleratio = 1)

  def __makePlotFromPlotData(self, plot_data, path_to_plots, config_type, bag_filename, overall_folder):
    # check if there are any curves to plot
    if plot_data.curves is None or len(plot_data.curves) == 0:
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
                  xaxis=self.__getLayoutXAxis(plot_data, 50),
                  yaxis=self.__getLayoutYAxis(plot_data))

    fig_data = dict(data=trace_data, layout=layout)

    # topic name from the first curve in the plot
    try:
      topic_name = plot_data.curves[0]["y_topic"]
    except:
      topic_name = ""

    # save plot in corresponding folder
    folder = path_to_plots + "/" + \
            bag_filename + "/" + \
            overall_folder + "/" + \
            config_type + self.__getIdFromConfigTopic(topic_name) + "/"
    try:  # else already exists
      os.makedirs(folder)
    except:
      pass

    py.offline.plot(fig_data, filename=folder + plot_data.id + ".html", auto_open=False)

  def __makeOverallPlotsFromConfig(self, bag, config_type, path_to_plots):
    # get bag filename without ".bag"
    bag_filename = bag.filename[:bag.filename.rfind('.')]

    # for each specified plot in the yaml file
    try:
      for plot_key, plot_value in self.configs[config_type]["plots"].items():
        # flag to know if all topics corresponding to this plot configuration have been read
        flag_all_topics_read = False

        # list of already checked bags for this plot configuration
        topics_read_list = []

        # as long as not all topics have been read for this plot configuration
        while(not flag_all_topics_read):
          plot_data = PlotData(bag, config_type, plot_key, plot_value, topics_read_list)
          self.__makePlotFromPlotData(plot_data, path_to_plots, config_type, bag_filename, "Overall")

          # update flag and list of topics read
          topics_read_list = plot_data.topics_read_list
          flag_all_topics_read = plot_data.flag_all_topics_read
    except:
      # ignores yaml files with no info
      pass

  def __makeHarcodedPlots(self, bag, path_to_plots, overall_folder):
    # get bag filename without ".bag"
    bag_filename = bag.filename[:bag.filename.rfind('.')]

    # get plot data list
    plot_data_list = getHardcodedPlotsData(bag)

    # plot data from the list
    for plot_data, config_type in plot_data_list:
      self.__makePlotFromPlotData(plot_data, path_to_plots, config_type, bag_filename, overall_folder)

  def __makeMissionPlotsFromConfig(self, bag, original_bag_filename, mission_name, config_type, path_to_plots):
    # get bag filename without ".bag"
    bag_filename = original_bag_filename[:original_bag_filename.rfind('.')]

    # for each specified plot in the yaml file
    try:
      for plot_key, plot_value in self.configs[config_type]["plots"].items():
        # flag to know if all topics corresponding to this plot configuration have been read
        flag_all_topics_read = False

        # list of already checked bags for this plot configuration
        topics_read_list = []

        # as long as not all topics have been read for this plot configuration
        while(not flag_all_topics_read):
          plot_data = PlotData(bag, config_type, plot_key, plot_value, topics_read_list)
          self.__makePlotFromPlotData(plot_data, path_to_plots, mission_name, bag_filename, "Missions")

          # update flag and list of topics read
          topics_read_list = plot_data.topics_read_list
          flag_all_topics_read = plot_data.flag_all_topics_read

        print("TOPICS READ LIST: " + str(topics_read_list))
    except:
      # ignores yaml files with no info
      print("[Error] Something went wrong while loading plot data.")
      pass

  def __saveMissionBags(self, bag, missions, path_to_plots):
    # if bag has no missions, there is nothing to save
    if len(missions) == 0:
      return

    # bag filename
    bag_filename = bag.filename[:bag.filename.rfind('.')]

    # get folder to save missions' bags
    folder = path_to_plots + \
            bag_filename + "/" + \
            "Missions/"

    print("Folder to save mission bags: " + folder)

    # for each mission
    for mission in missions:
      # set mission name and folder
      mission.setMissionNameAndFolder(str(missions.index(mission)) + "_mission", folder)

      # create mission folder
      try: # else already exists
        os.makedirs(mission.mission_folder)
      except:
        pass

    # create new bags for the missions
    new_bag_list = [rosbag.Bag(folder + str(missions.index(mission)) + "_mission.bag", 'w') for mission in missions]

    # index of first mission
    mission_idx = 0
    
    # go through the bag and record the mission_bags
    for topic, msg, t in bag.bag.read_messages():
      # if time corresponds to current mission
      if missions[mission_idx].start_time <= t <= missions[mission_idx].end_time:
      # if missions[mission_idx].start_time - rospy.Duration(120) <= t <= missions[mission_idx].end_time + rospy.Duration(120):
        new_bag_list[mission_idx].write(topic, msg, t)
      # if time corresponds to after the current mission
      elif t > missions[mission_idx].end_time:
      # elif t > missions[mission_idx].end_time + rospy.Duration(120):
        new_bag_list[mission_idx].close()
        print("Created " + missions[mission_idx].mission_name + ".bag")
        
        # update index to next mission
        mission_idx += 1
        
        # if already saved bags for all missions, we can skip the rest of the bag
        if mission_idx == len(missions):
          break

    return

  def __getMissions(self, bag, start_flags, mission_flags, end_flags):
    # list of missions
    missions = []

    # get Flag data as a dictionary with "data" and "time" entries
    Flag = bag.getFlagData("/Flag")
    length = len(Flag["time"])

    print(Flag["data"])

    # go through the Flag data and find missions
    for i in range(length - 1):
      # if a starting sequence of flags is found
      if (Flag["data"][i] in start_flags) and (Flag["data"][i+1] in mission_flags):
        # from index i+1 forward, try to find the end of the mission
        for j in range(i+1, length - 1):
          # if an ending sequence of flags is found
          if (Flag["data"][j] in mission_flags) and (Flag["data"][j+1] in end_flags):
            # after having the start (i) and end (j+1) indexes
            missions.append(Mission(bag, Flag["time"][i], Flag["time"][j+1]))
            break
    
    return missions
          
  # Public Methods

  def createPlots(self):
    overall_configs_list = ["drivers"]
    # overall_configs_list = ["drivers", "missions"]
    mission_configs_list = ["missions"]

    print("\nCreating Overall plots...")
    # create plots for each bag
    for bag in self.bag_list:
      # get path to plots folder
      path_to_plots = self.__getPathToPlotsFolder(bag.bag_path)

      # for each config file
      for config_type in self.configs.keys():
        # if config file corresponds to plots for Overall folder
        if any(config_folder in config_type for config_folder in overall_configs_list):
          self.__makeOverallPlotsFromConfig(bag, config_type, path_to_plots)
      
      # plot hardcoded plots, i.e., plots not defined in the .yaml config files
      self.__makeHarcodedPlots(bag, path_to_plots, "Overall")

    print("\nCreating Mission plots...")

    # mission patterns:
    # 4 6 4 -> waypoint, PF, waypoint
    # 4 6 0 -> waypoint, PF, idle
    # 0 6 4 -> idle, PF, waypoint
    # 0 6 0 -> idle, PF, idle
    start_flags = [0, 4]
    mission_flags = [6]
    end_flags = [0, 4]

    # create plots for all missions
    for bag in self.bag_list:
      # get path to plots folder
      path_to_plots = self.__getPathToPlotsFolder(bag.bag_path)

      # create missions for this bag
      missions = self.__getMissions(bag, start_flags, mission_flags, end_flags)

      # save missions' bags in the correct directories
      self.__saveMissionBags(bag, missions, path_to_plots)

      # for each mission
      for mission in missions:
        # associate mission bags to its mission (mission.mission_bag)
        mission.setMissionBag()

        print("\tCreating plots for: " + mission.mission_name)

        # print("Mission: start: " + str(mission.start_time) + ", end: " + str(mission.end_time))
        # for each config file
        for config_type in self.configs.keys():
          # if config file corresponds to plots for Missions folder
          if any(config_folder in config_type for config_folder in mission_configs_list):
            # create mission plots
            self.__makeMissionPlotsFromConfig(mission.mission_Bag, mission.original_Bag.filename, mission.mission_name, config_type, path_to_plots)