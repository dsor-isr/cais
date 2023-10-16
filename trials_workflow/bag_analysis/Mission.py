import rosbag
from Bag import Bag

class Mission(object):

  # Constructor
  def __init__(self, bag, t_start, t_end):
    self.original_Bag = bag
    self.start_time = t_start
    self.end_time = t_end
    self.mission_Bag = None
    self.mission_name = None
    self.mission_folder = None

  # Private Methods

  
  
  # Public Methods

  def setMissionNameAndFolder(self, mission_name, folder):
    self.mission_name = mission_name
    self.mission_folder = folder + mission_name + "/"

  def setMissionBag(self):
    path_to_bag = self.mission_folder[:-1] + ".bag"
    self.mission_Bag = Bag(path_to_bag)