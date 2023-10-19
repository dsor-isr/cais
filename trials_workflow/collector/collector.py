
import subprocess
import os
import argparse
from datetime import date,datetime

# To run this script you need the /etc/hosts file to be configure with the name of the vehicles

# Parse arguments
parser = argparse.ArgumentParser(description='Copy all the bags from specified vehicles')
parser.add_argument('vehicles', metavar='N', type=str, nargs='+',
                    help='vehicles to collect bags from')
parser.add_argument('--date', type=str, nargs='+',
                    help='date of the bags to be collected, of the format yyyy-mm-dd')
parser.add_argument('--name', type=str, nargs='+',
                    help='name for the destination folder, has to correspond to dates')
parser.add_argument('--user', type=str, nargs='+',
                    help='users for the secure-copy, has to correspond to vehicles with IP addresses')

args = parser.parse_args()

# Define variables accordingly
vehicles = args.vehicles

try:
    dates = args.date
    print("Using specified dates: " + str(dates))
except:
    today = str(date.today()).split("-")
    dates = []
    dates.append(today[2] + today[1] + today[0])
    print("Using current date: " + str(dates))

count = 0 # Initialize # of users
known_hosts = ["mvector", "mred", "mblack", "myellow", "delfim", "glider"]
try:
    users = args.user
    for v in vehicles:
        if v not in known_hosts:
            count = count + 1
            if "." in v:
                print("\nWARNING: Probably found IP address instead of host name. Folder will be named after: " + str(v) + "\n")
            
    # Check if # of users is valid given # of unknown hosts
    if count != len(users):
        print("# of users does not match # of unknown hosts found (known_hosts = " + str(known_hosts) + "). Exiting...")
        exit()
except:
    print("Found IP addresses with no users associated. Exiting...")
    exit()

# Validate dates
# giving the date format
date_format = '%Y-%m-%d'
# using try-except blocks for handling the exceptions
try:
    for d in dates:
        # formatting the date using strptime() function
        dateObject = datetime.strptime(d, date_format)
        print("Testing time: " + str(dateObject))
# If the date validation goes wrong
except ValueError:
    # printing the appropriate text if ValueError occurs
    print("Incorrect data format, should be YYYY-MM-DD: " + d + ". Exiting...")
    exit()

try:
    name = args.name
    if len(dates) != len(name):
        print("Number of dates does not match number of names. Exiting...")
        exit()
    for i in range(len(name)):
        name[i] = dates[i] + "_" + name[i]
    print("Using specified name for destination folder: " + str(name))
except:
    name = dates
    print("Using dates as default names for destination folder: " + str(name))


# Verify directories
home_dir = os.path.expanduser("~/trials_raw/")
if os.path.exists(home_dir):
    print("Path " + home_dir + " already exists. Writing to path...")
else:
    os.mkdir(home_dir)
    print("Created path: " + home_dir)

for n in name:
    # Verify path relative to day
    path = home_dir + n + "/"
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created path: " + path)
    
    # Verify vehicles path
    path = path + "vehicles/"
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created path: " + path)

    # Verify each vehicle path
    for v in vehicles:
        v_path = path + v + "/"
        if not os.path.exists(v_path):
            os.mkdir(v_path)
            print("Created path: " + v_path)
        if not os.path.exists(v_path + "ROSData/"):
            os.mkdir(v_path + "ROSData/")
            print("Created path: " + v_path + "ROSData/")

# Keys for user inside vehicles
# v_keys = ["delfim","medusa"]

# Extract data
for v in vehicles:
    if v == "mvector" or v == "mred" or v == "mblack" or v == "myellow":
        user = "medusa"
    elif v == "delfim":
        user = "delfim"
    elif v == "glider":
        user = "ubuntu"
    else:
        user = users.pop(0)
    for d in dates:
        for n in name:
            # Copy bags
            subprocess.run(["scp","-r", user + "@" + v + ":~/ROSData/" + "*" + d + "*", home_dir + n + "/vehicles/" + v + "/ROSData/"])
            # Copy src
            subprocess.run(["scp","-r", user + "@" + v + ":~/catkin_ws_real/src/", home_dir + n + "/vehicles/" + v + "/"])
            # Copy logs
            subprocess.run(["scp","-r", user + "@" + v + ":~/catkin_ws_real/logs/", home_dir + n + "/vehicles/" + v + "/"])

print("Clearing up empty directories...")

for n in name:
    for v in vehicles:
        if len(os.listdir(home_dir + n + "/vehicles/" + v + "/ROSData/")) == 0:
            os.rmdir(home_dir + n + "/vehicles/" + v)

print("Finished process successfully")