
import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description='Reindex all the bags from specified vehicles')
parser.add_argument('path', type=str, nargs='?',
                    help='path to perform reindexing and cleaning of old bags')

args = parser.parse_args()

path = args.path
path = os.path.expanduser(path)

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        if "active" in name:
            new_list = name.split(".active")
            new_name = new_list[0] + new_list[1]
            subprocess.run(["mv", path + name, path + new_name])

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        subprocess.run(["rosbag","reindex", path + name])

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        if "orig" in name:
            subprocess.run(["rm","-rf", path + name])