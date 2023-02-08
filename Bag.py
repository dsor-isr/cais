import rosbag

class Bag(object):

  # Constructor
  def __init__(self, bag_path):
    self.bag_path = bag_path # path to the .bag file
    self.filename = bag_path[bag_path.rfind('/')+1:] # name of the .bag file
    self.bag = None
    self.topics_list = [] # list of topics (strings)
    self.__loadBag()

  # Private Methods

  def __loadBag(self):
    # read bag
    self.bag = rosbag.Bag(self.bag_path)

    # get topics
    self.topics_list = list(self.bag.get_type_and_topic_info()[1].keys())
  
  # Public Methods

  def getBagTopicData(self, topic_name):
    return self.bag.read_messages(topics = topic_name)