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

  def getFlagData(self, flag_topic):
    # Flag topic data
    Flag = dict()
    Flag["time"] = []
    Flag["data"] = []

    # find topic name correspondent to the Flag topic
    for topic_name in self.topics_list:
      # if topic name is the Flag topic
      if flag_topic in topic_name:
        # extract time and message from the topic data
        for topic, msg, t in self.getBagTopicData(topic_name):
          Flag["time"].append(t)
          Flag["data"].append(msg.data)
        
        return Flag

    return Flag

  def getBagTopicData(self, topic_name):
    return self.bag.read_messages(topics = topic_name)
