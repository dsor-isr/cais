import rosbag

class Bag(object):

  # Constructor
  def __init__(self, bag_path):
    self.bag_path = bag_path # path to the .bag file
    self.filename = bag_path[bag_path.rfind('/')+1:] # name of the .bag file
    self.topics_list = [] # list of topics (strings)
    self.data = dict() # dictionary with data from each topic
    self.__loadBag()

  # Private Methods

  def __loadBag(self):
    # read bag
    bag = rosbag.Bag(self.bag_path)

    # get topics
    self.topics_list = list(bag.get_type_and_topic_info()[1].keys())

    # create dict with data from topics, indexed by topic name
    for topic_name in self.topics_list:
      self.data[topic_name] = bag.read_messages(topics = topic_name)

      # if "bat_monit/data" in topic_name:
      topic_data = self.data[topic_name]

      for topic, msg, t in topic_data:
        print(topic)
        print(msg)
        print(t)
        print("\n")
        break
  
  # Public Methods

