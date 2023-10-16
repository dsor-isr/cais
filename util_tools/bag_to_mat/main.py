import os     
import sys
import yaml
from Bag import Bag
import pandas as pd
from scipy.io import savemat

def getPathToBag():
	# check if there is an input
	try:
		path = sys.argv[1]
	except:
		sys.exit("Please specify a path the bag to convert to .mat .")

	# check if path is valid
	if (os.path.exists(path)):
		return path
	else:
		sys.exit("Path doesn't exist!")

def loadYamlFile(path_to_file):
	with open(path_to_file) as f:
		yaml_config = yaml.load(f, Loader=yaml.loader.SafeLoader)

	return yaml_config

def loadConfigurations():
	# dict with yaml info
	configs = dict()
	config_dir = "config/"

	# find all .yaml files
	for root, dirs, files in os.walk(config_dir, topdown=False):
		for name in files:
			if ".yaml" in name:
				# name without .yaml
				true_name = name[:name.rfind('.')]

				# path to the yaml file
				path_to_file = os.path.join(root, name)

				# get yaml config data
				configs = loadYamlFile(path_to_file)

	return configs

def nestedGetAttribute(obj, config_field):
	# if the config field is a list of strings, we need to nest the attributes

	obj_iter = obj
	for attr in config_field:
		field = getattr(obj_iter, attr)
		obj_iter = field

	return field

def loadDataToDict(bag, bag_dict, configs, topic_name, topic_config):
	# get different fields for the msg from the config
	list_of_fields = configs["topics"][topic_config]["fields"]
	list_of_var_names = configs["topics"][topic_config]["var_name"]

	# different number of fields and var names
	if len(list_of_fields) != len(list_of_var_names):
		return

	# SPECIAL CASE WHEN WE WANT TO SEPARATE USBL MEASUREMENTS IN MVECTOR BETWEEN
	# ALL VEHICLES THAT SEND Bearing/Elevation/Range (BER) INFORMATION
	if (configs["flags"]["separate_usbl_meas_by_sender"] is True) and ("usbl" in topic_config):
		# number of VEHICLES sending USBL measurements to MVECTOR
		n = 2

		# initialise time list FOR EVERY VEHICLE
		for i in range(n):
			bag_dict[topic_config]["t"+str(i)] = [] # for time

		# initialise fields as lists
		for field, var_name in zip(list_of_fields, list_of_var_names):
			for i in range(n):
				bag_dict[topic_config][var_name+str(i)] = []
		
		# compute the minimum time interval between BER measurements (true_delta)
		got_first_nonzero_meas = False
		true_delta = 0
		nr_iterations = 500
		for i, (topic, msg, t) in enumerate(bag.getBagTopicData(topic_name)):
			if not got_first_nonzero_meas:
				# get time instant if first measurement attribute is not 0
				if nestedGetAttribute(msg, list_of_fields[0]) != 0:
					last_time_inst = t.to_sec()
					got_first_nonzero_meas = True
			else:
				# after first measurement is got, let's compute the value of delta consecutively
				# for a certain number of iterations, and keep the smallest delta

				# get new delta if the attribute is not 0
				if nestedGetAttribute(msg, list_of_fields[0]) != 0:
					new_delta = t.to_sec() - last_time_inst
					last_time_inst = t.to_sec()

					# update delta if new_delta is smaller 
					if (true_delta == 0) or (new_delta < true_delta):
						true_delta = new_delta
			
			# after number of iterations have passed
			if i > nr_iterations:
				true_delta = int(true_delta)
				break

		# full time cycle of all n vehicles
		full_cycle = true_delta * n

		# load bag data into the dictionary
		vehicle_idx = 0
		for i, (topic, msg, t) in enumerate(bag.getBagTopicData(topic_name)):
			# update index
			if i == 0:
				last_time_inst = t.to_sec()
			# according to how much time passed, update the vehicle index
			else:
				# time passed since last measurement
				time_passed = t.to_sec() - last_time_inst

				# how many delta intervals have passed since last measurement
				deltas = time_passed/true_delta

				# not enough time has passed since last measurement <=>
				# <=> new measurement still belongs to last measurement's sender vehicle
				if deltas < true_delta/2:
					continue

				# how many deltas passed, ignoring full cycles (each full cycle is delta * n, n is number of vehicles)
				effective_deltas_passed = round(deltas % n)

				# update vehicle index
				vehicle_idx = (vehicle_idx + effective_deltas_passed) % n
				
				# update last time instant
				last_time_inst = t.to_sec()
			
			# add time
			bag_dict[topic_config]["t"+str(vehicle_idx)].append(t.to_sec())

			# add attributes to dictionary
			for field, var_name in zip(list_of_fields, list_of_var_names):
				# print(var_name+str(vehicle_idx))
				bag_dict[topic_config][var_name+str(vehicle_idx)].append(nestedGetAttribute(msg, field))

	else: # NORMAL BEHAVIOUR
		# initialise time list
		bag_dict[topic_config]["t"] = [] # for time

		# initialise fields as lists
		for field, var_name in zip(list_of_fields, list_of_var_names):
			bag_dict[topic_config][var_name] = []

		# load bag data into the dictionary
		for topic, msg, t in bag.getBagTopicData(topic_name):
			bag_dict[topic_config]["t"].append(t.to_sec())
			
			for field, var_name in zip(list_of_fields, list_of_var_names):
				bag_dict[topic_config][var_name].append(nestedGetAttribute(msg, field))

def getKeyFromValue(configs, topic_name):
	a = [key for key in configs["topics"].keys() if configs["topics"][key]["topic_name"] == topic_name]

	return a[0]

def getListOfFieldsFromTopic(bag, topic):
	# get first msg from the topic data
	for topic, msg, t in bag.getBagTopicData(topic):
		list_of_attrs = list()

		for attr in dir(msg):
			if attr[0] != "_" and attr not in ["header", "deserialize", "deserialize_numpy", "serialize", "serialize_numpy"]:
				# recursively add all nested attributes
				list_of_attrs.append([attr]) # CHANGE

		return list_of_attrs

def populateConfigsWithAllTopics(bag, configs):
	new_dict = dict()

	# for every topic in the bag, create the entries as dictionaries and populate them
	for topic in bag.topics_list:
		# replace "/" for "_" and remove the first "/"
		topic_entry = topic.replace("/", "_")[1:]

		# add entry as a dict
		new_dict[topic_entry] = dict()

		# add topic name
		new_dict[topic_entry]["topic_name"] = topic

		# get fields for the topic
		new_dict[topic_entry]["fields"] = getListOfFieldsFromTopic(bag, topic)

		# get var_names for each field
		new_dict[topic_entry]["var_name"] = [el[0] for el in new_dict[topic_entry]["fields"]]

	return new_dict

def saveMatFileFromBag(bag, configs):
	# initialise dictionary
	bag_dict = dict()

	# if we want to load all topics from the bag instead of just the ones specified in the yaml file
	if configs["flags"]["load_all_topics_from_the_bag"]:
		# delete the entry of the configurations for the topics
		del configs["topics"]

		# recreate the entry as a dictionary and populate it with all topics
		configs["topics"] = populateConfigsWithAllTopics(bag, configs)

	# get list of topics to find
	topics_to_find = dict()

	for topic in configs["topics"]:
		topics_to_find[topic] = configs["topics"][topic]["topic_name"]

	print("Topics to save:")
	for topic in topics_to_find.values():
		print("\t" + topic)
	
	print("Loading data into .mat file...")

	for topic_name in bag.topics_list:
		if topic_name in topics_to_find.values():
			# key in the yaml for each set of data for one topic
			topic_config = getKeyFromValue(configs, topic_name)

			# initialise the entry for this topic as a dictionary of its own
			bag_dict[topic_config] = dict()

			# load data to dict
			loadDataToDict(bag, bag_dict, configs, topic_name, topic_config)

	# create mat file with bag_dict
	savemat("output/" + bag.filename.replace(".bag", "") + ".mat", bag_dict)

	print("\tDone.")

def main():
	print("Loading bag...")
  # get path where bag is
	path_to_bag = getPathToBag()

	# load configurations
	configs = loadConfigurations()

  # get Bag
	bag = Bag(path_to_bag)
	print("\t" + bag.filename)

	saveMatFileFromBag(bag, configs)

if __name__ == '__main__':
	main()