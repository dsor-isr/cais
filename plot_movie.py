"""

Developers: whitemanatee > francisco.branco@tecnico.ulisboa.pt

Description: Script that reads all .mat files from rosbags with
             N,E and yaw to plot the mission and create a movie

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


import scipy
import sys
import os
import numpy
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

def help():
    print("Command help: python plot_movie.py [TRIAL_NAME]")
    print("The files should all be inside the working directory named \"files\"")
    # print("The vehicle files must be named \"vehicle0\", \"vehicle1\", etc.")

if len(sys.argv) != 2:
    print("Invalid number of arguments: " + str(len(sys.argv) - 1))
    help()
    exit(1)

plot_data = []
color_dict = {"mred": "red", "mblack": "black", "mvector": "yellow", "delfim": "orange"}

if sys.argv[0].split('plot_movie.py')[0] == "":
    path = "./files/"
else:
    path = sys.argv[0].split('plot_movie.py')[0] + "files/"

if os.path.exists(path) and os.path.exists(path.split("files/")[0] + "save/"):
    pass
else:
    print("Either \"files/\" or \"saves\" directory does not exist in specified path")
    exit(1)

for root, dirs, files in os.walk(path):
    for f in files:
        if ".mat" in f:
            pd = {"mat_file": None, "data": None, "color": None, "variable_keyword": None}
            pd["mat_file"] = os.path.join(root, f)
            for c in color_dict.keys():
                if c in f:
                    pd["color"] = c
            plot_data.append(pd)


try:
    for pd in plot_data:
        pd["data"] = scipy.io.loadmat(pd["mat_file"])
except FileNotFoundError as e:
    print(e)
    exit(1)

non_data = ("__header__", "__version__", "__globals__")
# variable_keyword = []
for pd in plot_data:
    for keyword in non_data:
        del pd["data"][keyword]
    pd["variable_keyword"] = list(pd["data"].keys())[0]

# variable_keyword = list(plot_data[0]["data"].keys())[0]

for pd in plot_data:
    pd["data"] = pd["data"][pd["variable_keyword"]][0][0]

# Define the variables of interest
#keys = ("Time", "North", "East", "Yaw")

# if os.path.exists(path.split('files/')[0] + "saves/"):
#     pass
# else:
#     print("\"saves/\" directory does not exist in specified path")
#     exit(1)

legend_size = 15

fig, ax = plt.subplots(1,1)

fig.set_size_inches((14, 10))

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

for pd in plot_data:
    # Check if file is valid
    if len(pd["data"]) != 4:
        print("Invalid number of variables in the .mat file: " + str(len(pd["data"])))
        exit(1)
    # for key in keys:
    #     if key not in data.dtype:
    #         print("The following variable does not exist in the .mat file: " + key)
    #         exit(1)
    #ax.plot(data[2], data[1], color='blue', linestyle='--')
    if pd["color"] in color_dict.keys():
        c = color_dict[pd["color"]]
    else:
        c = "blue"
    ax.plot(pd["data"][2], pd["data"][1], color=c)

ax.ticklabel_format(useOffset=False, style='plain')

# Title
ax.set_title(sys.argv[1], size=legend_size)

# Labels and grid
ax.set_xlabel('Northing [m]', size=legend_size*0.8)
ax.set_ylabel('Easting [m]', size=legend_size*0.8)
ax.grid()
ax.axis('equal')

# Legend
legends = []
for pd in plot_data:
    legends.append(pd["color"])
ax.legend(legends, prop={'size': legend_size})

fig.show()
# file_name, ext = sys.argv[1].split('.')
fig.savefig(fname=path.split('files/')[0] + "saves/" + sys.argv[1] + ".png", format='png')

response = input("Static image created. Type \"[y]es\" to continue creating the video...\n")

if "y" or "\n" or "Y" in response:
    pass
else:
    print("Ended program at image creation")
    exit(0)


fig, ax = plt.subplots(1,1)

fig.set_size_inches((14, 10))

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

duration = 30
full_length = plot_data[0]["data"][0][-1] - plot_data[0]["data"][0][0]
factor = 1/8 # 64
fps = len(plot_data[0]["data"][0]) * factor / duration
speed = float(full_length / duration)

print("The final video is x" + str(speed) + " faster and has a frame rate of " + str(fps)) # speed[0]

def make_frame(t):
    i = int(len(plot_data[0]["data"][0]) * t / duration)
    if i >= len(plot_data[0]["data"][0]):
        i = len(plot_data[0]["data"][0]) - 1

    ax.cla()
    for pd in plot_data:
        if pd["color"] in color_dict.keys():
            c = color_dict[pd["color"]]
        else:
            c = "blue"
        ax.plot(pd["data"][2][:i], pd["data"][1][:i], color=c, label='_nolegend_')
        ax.plot(pd["data"][2][i], pd["data"][1][i], color=c, marker=(3, 0, 360 - pd["data"][3][i]), markersize=20)
    
    ax.ticklabel_format(useOffset=False, style='plain')

    # Title
    ax.set_title(sys.argv[1], size=legend_size)

    # Labels and grid
    ax.set_xlabel('Northing [m]', size=legend_size*0.8)
    ax.set_ylabel('Easting [m]', size=legend_size*0.8)
    ax.grid()
    ax.axis('equal')

    # Legend
    legends = []
    for pd in plot_data:
        legends.append(pd["color"])
    ax.legend(legends, prop={'size': legend_size})

    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration=duration)
animation.write_videofile(path.split('files/')[0] + "saves/" + sys.argv[1] + ".mp4", fps=fps)

print("Output an image and a video. Enjoy!")