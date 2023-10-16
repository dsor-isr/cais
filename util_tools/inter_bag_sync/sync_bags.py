import os     
import sys
import yaml
import pandas as pd
import rosbag
from scipy.io import savemat

# sys.path.insert(0,"..")
from Bag import Bag

def getPathToBag():
	# check if there is an input
	try:
		path = sys.argv[1]
	except:
		sys.exit("Please specify a path from root to bag to serve as sync for other bags.")

	# check if path is valid
	if (os.path.exists(path)):
		return path
	else:
		sys.exit("Path doesn't exist!")

def loadInputBags():
	print("Loading input bags...")

	input_bags = []

	# get bags to synchronise from input folder
	input_dir = "input_bags/"

	# find all .bag files
	for root, dirs, files in os.walk(input_dir, topdown=False):
		for name in files:
			if ".bag" in name:
				# path to bag
				path_to_bag = os.path.join(root, name)

				input_bags.append(Bag(path_to_bag))
				print("\t" + input_bags[-1].filename)

	return input_bags

def foundDesiredTopic(topic_name, config_topic):
	# if the topic to be plotted (config) is not in the current topic being checked
	if config_topic.lower() not in topic_name.lower():
		return False

	# since at this point config_topic is in the topic_name, let's know what's before and after
	try:
		before, after = topic_name.lower().split(config_topic.lower())
	except:
		# if failed, let it consider the topic has been found
		return True
	
	# check if there is anything other than the vehicle name before the config topic 
	# (== occurences of "/*" is 0 or 1, * being a wildcard for any character)
	nr_of_slashes = 0 # number of '/' with characters after
	for i, c in enumerate(before):
		try:
			if (c == '/') and (i+1 < len(before)):
				nr_of_slashes += 1
		except:
			pass
	
	if nr_of_slashes > 1:
		return False

	# check if there is anything after the config_topic
	if len(after) != 0:
		if (after[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
			return False

	return True

def getTimeInstants(bag, gps_time_instant):
	t_gps, t_state = None, None

	# if we want the time instants for the reference bag
	if gps_time_instant is None:
		# for every topic existent in the bag
		for topic_name in bag.topics_list:
			# if found gps topic
			if foundDesiredTopic(topic_name, "drivers/gps/data"):
				# extract message from the topic data
				for topic, msg, t in bag.getBagTopicData(topic_name):
					t_gps = msg.utc_time
					break
			
			# if found state topic
			if foundDesiredTopic(topic_name, "nav/filter/state"):
				# extract message from the topic data
				for topic, msg, t in bag.getBagTopicData(topic_name):
					t_state = t.to_sec()
					break
	# if we want the time instances corresponding to the reference bag
	else:
		# for every topic existent in the bag
		for topic_name in bag.topics_list:
			# if found gps topic
			if foundDesiredTopic(topic_name, "drivers/gps/data"):
				# extract message from the topic data
				for topic, msg, t in bag.getBagTopicData(topic_name):
					# when it find a time instant after the gps_time_instant from the reference bag
					if (msg.utc_time > gps_time_instant):
						t_state = t.to_sec()
						t_gps = msg.utc_time
						break

	# return values found
	return t_state, t_gps

def getTimeDifference(reference_bag, input_bags):
	time_diffs = []

	# get first datapoint from reference bag
	t_state_ref, t_gps_ref = getTimeInstants(reference_bag, None)

	# for each bag get correspondent time
	for input_bag in input_bags:
		# get time instants for current bag
		t_state, t_gps = getTimeInstants(input_bag, t_gps_ref)

		# compute difference between ref bag and current bag
		time_diffs.append(t_state_ref - t_state)

	return time_diffs

def getMinMaxTimeInState(bag):
  # for every topic existent in the bag
	for topic_name in bag.topics_list:
		# if found gps topic
		if foundDesiredTopic(topic_name, "drivers/gps/data"):
			# extract message from the topic data
			for i, (topic, msg, t) in enumerate(bag.getBagTopicData(topic_name)):
				# get first time instant
				if i == 0:
					t_init = t.to_sec()

				# get last time instant
				t_end = t.to_sec()
			
	print(str(t_init) + " " + str(t_end))
	
	return t_init, t_end

def writeOutputBags(ref_t_min, ref_t_max, input_bags, time_diffs):
	print("Creating output bags (synchronised with reference bag)...")

	# create new bags for the missions
	new_bag_list = [rosbag.Bag("output_bags/" + input_bag.filename.replace(".bag", "") + "_cut.bag", 'w') for input_bag in input_bags]
	
	# flag to know if the bag is still opened
	bag_is_open = False

	for input_bag, new_bag, time_diff in zip(input_bags, new_bag_list, time_diffs):
		# go through the bag and record the mission_bags
		for topic, msg, t in input_bag.bag.read_messages():
			# if time corresponds to during the interval of the reference bag
			if ref_t_min <= t.to_sec() + time_diff <= ref_t_max:

				if not bag_is_open:
					print("Input bag: " + input_bag.filename)
					print(str(ref_t_min) + " -> " + str(ref_t_max))
					print("Time: " + str(t.to_sec() + time_diff))

				new_bag.write(topic, msg, t)
				bag_is_open = True
			# if time corresponds to after the interval of the reference bag
			elif t.to_sec() + time_diff > ref_t_max:
				print("End time: " + str(t.to_sec() + time_diff))
				new_bag.close()
				bag_is_open = False
				print("Created " + input_bag.filename.replace(".bag", "") + "_cut.bag")
				break
		
		# if it reached the end of the bag without finding a time instant after the time interval, close the bag
		if bag_is_open:
			print("End time: " + str(t.to_sec() + time_diff))
			new_bag.close()
			bag_is_open = False
			print("Created " + input_bag.filename.replace(".bag", "") + "_cut.bag")

def main():
	print("Loading bag...")
  # get path where bag is
	path_to_bag = getPathToBag()

  # get Bag
	reference_bag = Bag(path_to_bag)
	print("\t" + reference_bag.filename)

	# get min, max time instants of the reference bag
	ref_t_min, ref_t_max = getMinMaxTimeInState(reference_bag)

	# load input bags to synchronise
	input_bags = loadInputBags()

	# get time difference between reference bag and input bags
	time_diffs = getTimeDifference(reference_bag, input_bags)

	# write output bags
	writeOutputBags(ref_t_min, ref_t_max, input_bags, time_diffs)

if __name__ == '__main__':
	main()