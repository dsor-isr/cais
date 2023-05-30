"""

Developers: whitemanatee > francisco.branco@tecnico.ulisboa.pt
            ecunhado > eduardo.m.a.cunha@tecnico.ulisboa.pt

Description: Yaml loading functions (developed by Eduardo Cunha)

===========================================================
|               _.-----.._                 __________     |
|             -'    .     ``:--.          (o(' ^ ') o)    |
|           .'.         '  '    \,                        |
|          /       .    `  .  (* \                        |
|         : .  `.  :  ,)  .::../  k                       |
|        ) ..aaa8Y88aP/ <d888aaL_::)                      |
|      .'a888Y8888888b\  )  `^88: "                       |
|    .'.a8888)  ""     `'    d88                          |
|   (a888888/                "`                           |
|   `Y888PP'                                              |
===========================================================
Protect the manatees!
"""

import yaml
import os

def loadConfigurations(path):
	# dict with yaml info
	configs = dict()
	# config_dir = os.path.join(path, "config/")

	# find all .yaml files
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if ".yaml" in name:
				# path to the yaml file
				path_to_file = os.path.join(root, name)

				# get yaml config data
				configs = loadYamlFile(path_to_file)
	return configs

def loadYamlFile(path_to_file):
	with open(path_to_file) as f:
		yaml_config = yaml.load(f, Loader=yaml.loader.SafeLoader)
	return yaml_config