import os     
import sys
from Bag import Bag
from Plotter import Plotter
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
	configs_parent_dirs = dict()
	config_dir = "config/"

	# find all .yaml files
	for root, dirs, files in os.walk(config_dir, topdown=False):
		for name in files:
			if ".yaml" in name:
			# if "thruster.yaml" in name:
				# name without ".yaml"
				true_name = name[:name.rfind('.')]
				path_to_file = os.path.join(root, name)

				# add entry to the dictionary
				# this entry will be a dict of its own, with all info from
				# this specific yaml file
				configs[true_name] = loadYamlFile(path_to_file)
				
				# get parent directory
				path_from_parent = path_to_file.replace(config_dir, "")
				configs_parent_dirs[true_name] = path_from_parent.replace(name, "")[0:-1]

				print("\t" + path_from_parent)

	return configs, configs_parent_dirs

def loadYamlFile(path_to_file):
	with open(path_to_file) as f:
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
					print("\t" + name)

	# load configurations inside config/ folder
	print("\nLoading configurations...")
	configs, configs_parent_dirs = loadConfigurations()

	# create plots according to configs using loaded bags
	print("\nPlotting...")
	plt = Plotter(bag_list, configs, configs_parent_dirs)
	plt.createPlots()

if __name__ == '__main__':
  main()