import os     
import sys
from Bag import Bag

def getPathToTrialsData():
	# check if there is an input
	try:
		path = sys.argv[1]
	except:
		sys.exit("Please specify a path from root to trials data.")

	# check if path is valid
	if (os.path.exists(path)):
		return path
	else:
		sys.exit("Path doesn't exist!")

def main():
  # get path where trials data is
	path_trials_data = getPathToTrialsData()

	# list of bags
	bag_list = []

	print("Reading bags...")

	# search across all files in the specified path
	for root, dirs, files in os.walk(path_trials_data, topdown=False):
		for name in files:
			# check if the file is a .bag file but not a _mission.bag file
			if name.find('.bag') != -1 and name.find('_mission.bag') == -1:
				path_to_bag = os.path.join(root, name)
				# add new bag to bag list if it is inside ROSData folder
				if "ROSData/" in path_to_bag:
					bag_list.append(Bag(path_to_bag))

	# print loaded bags
	print("Loaded bags:")
	for bag in bag_list: print("\t" + bag.filename)

if __name__ == '__main__':
  main()