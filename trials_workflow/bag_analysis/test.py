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

for root, dirs, files in os.walk("/home/ecunhado/trials_raw/2023-05-15/vehicles/mvector/ROSData", topdown=False):
  for name in files:
    # check if the file is a .bag file but not a _mission.bag file
    if name.find('.bag') != -1 and name.find('_mission.bag') == -1:
      path_to_bag = os.path.join(root, name)
      # add new bag to bag list if it is inside ROSData folder and is not a banned bag
      if "mvector__2023-05-15-08-59-19.bag" in path_to_bag:
      # if "ROSData/" in path_to_bag and "test_day/" in path_to_bag:
        bag = Bag(path_to_bag)

print("loaded")

for topic, msg, t in bag.bag.read_messages():
  print(topic)
  print(msg)