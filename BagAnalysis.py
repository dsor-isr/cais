import os     
import sys
from Bag import Bag
from BagPlot import Plotter
import yaml

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
	
def loadConfigurations():
	# dict with yaml info
	configs = dict()
	config_dir = "config/"

	# find all .yaml files
	for root, dirs, files in os.walk(config_dir, topdown=False):
		for name in files:
			if ".yaml" in name:
				# name without ".yaml"
				true_name = name[:name.rfind('.')]

				# add entry to the dictionary
				# this entry will be a dict of its own, with all info from
				# this specific yaml file
				configs[true_name] = loadYamlFile(name, config_dir)

	return configs

def loadYamlFile(filename, config_dir):
	with open(config_dir + filename) as f:
		yaml_config = yaml.load(f, Loader=yaml.loader.SafeLoader)

	return yaml_config

def main():
	# list of bags
	bag_list = []

  # get path where trials data is
	path_trials_data = getPathToTrialsData()

	# search across all files in the specified path
	print("Loading bags...")
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

	# load configurations inside config/ folder
	print("\nLoading configurations...")
	configs = loadConfigurations()

	# print loaded configs
	print("Loaded configs:")
	for key in configs.keys(): print("\t" + key + ".yaml")

	# create plots according to configs using loaded bags
	print("\nPlotting...")
	plt = Plotter(bag_list, configs)
	plt.createPlots()

if __name__ == '__main__':
  main()