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
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import load_yaml as ly

import mods.slap as slap
import utils


# Working directory configuration
path = sys.argv[0].split('plot_movie.py')[0]
if sys.argv[0].split('plot_movie.py')[0] == "":
    path_files = "./files/"
    path_saves = "./saves/"
    path_configs = "./configs/"
else:
    path_files = os.path.join(sys.argv[0].split('plot_movie.py')[0], "files/")
    path_saves = os.path.join(sys.argv[0].split('plot_movie.py')[0], "saves/")
    path_configs = os.path.join(sys.argv[0].split('plot_movie.py')[0], "configs/")

# Check if directories exist and create them if not
if os.path.exists(path_files):
    pass
else:
    os.mkdir(path_files)
if os.path.exists(path_saves):
    pass
else:
    os.mkdir(path_saves)
if os.path.exists(path_configs):
    pass
else:
    os.mkdir(path_configs)

configs = ly.loadConfigurations(path_configs)

plot_data = []

# Treatment of data inside plot_data structure
# non_data = ("__header__", "__version__", "__globals__")

try:
    for f in configs["plots"]["curves"]:
        try:
            pd = {"mat_file": os.path.join(path_files, f["file"]), "data": None, "color": f["color"], "variable_keyword": None}
        except:
            print("Something went wrong while reading the .yaml parameters. Please revise")
            utils.help()
            exit(1)
        # Load .mat file
        pd["data"] = scipy.io.loadmat(pd["mat_file"])
        keywords = list(pd["data"].keys())
        # Change location of function V, can be more general than slap
        pd["variable_keyword"] = utils.search_topic(f["topic"], keywords)
        pd["data"] = pd["data"][pd["variable_keyword"]]
        # Take away outer indexation from .mat format
        while len(pd["data"]) == 1:
            try:
                pd["data"] = pd["data"][0]
            except IndexError as e:
                print(e)
                utils.help()
                exit(1)
        if configs["plots"]["image"]["mirror"]:
            aux_pd = pd["data"][1]
            pd["data"][1] = pd["data"][2]
            pd["data"][2] = aux_pd
            if "nav" in pd["variable_keyword"]:
                pd["data"][4][0] = pd["data"][4][0] + 2 * (45 - pd["data"][4][0])
            else:
                pd["data"][3][0] = pd["data"][3][0] + 2 * (45 - pd["data"][3][0])
        # This code was only usable for scalar time series
        # for i in range(len(pd["data"])):
        #     while True:
        #         try:
        #             pd["data"][i][0][0]
        #         except IndexError as e:
        #             break
        #         pd["data"][i] = pd["data"][i][0]
        plot_data.append(pd)
except FileNotFoundError as e:
    print(e)
    utils.help()
    exit(1)

# Image and Movie configurations
length_list = []
for pd in plot_data:
    length_list.append(len(pd["data"][0][0]))
max_length = max(length_list)
full_length = plot_data[0]["data"][0][0][-1] - plot_data[0]["data"][0][0][0]
try:
    duration = float(configs["plots"]["movie"]["duration"])
    factor = 1/float(configs["plots"]["movie"]["factor"])
    fps = max_length * factor / duration
    speed = float(full_length / duration)
except KeyError:
    pass

# Plot the image
legend_size = 15

fig, ax = plt.subplots(1,1)

fig.set_size_inches((14, 10))

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

for pd in plot_data:
    try:
        if configs["plots"]["mod"] == "slap":
            if "pdf" not in pd["variable_keyword"]:
                ax.plot(pd["data"][1][0], pd["data"][2][0], color=pd["color"], label="_nolegend_")
    except KeyError as e:
        ax.plot(pd["data"][1][0], pd["data"][2][0], color=pd["color"])

# Plot the samples in the image
if int(configs["plots"]["image"]["samples"]) > 0:
    samples = []
    for pd in plot_data:
        samples.append(np.linspace(pd["data"][0][0][0], pd["data"][0][0][-1], int(configs["plots"]["image"]["samples"]), True))
    for num in range(int(configs["plots"]["image"]["samples"])):
        for s, pd in enumerate(plot_data):
            # Determine the right index for timestamp
            err = 10000000000000000
            err_index = 0
            for time_stamp in pd["data"][0][0]:
                if abs(time_stamp - samples[s][num]) < err:
                    err = abs(time_stamp - samples[s][num])
                    i = err_index
                err_index += 1
            try:
                if configs["plots"]["mod"] == "slap":
                    if "pdf" in pd["variable_keyword"].lower():
                        covariance = [[pd["data"][1][i][0], pd["data"][1][i][1]], [pd["data"][2][i][0], pd["data"][2][i][1]]]
                        slap.plot_ellipse(covariance, ax, position, pd["color"])
                    else:
                        raise KeyError
                else:
                    raise KeyError
            except KeyError as e:
                if "nav" in pd["variable_keyword"] and "mvector" in pd["variable_keyword"]:
                    position = (pd["data"][1][0][i], pd["data"][2][0][i])
                    yaw = 360 - pd["data"][4][0][i]
                elif "nav" in pd["variable_keyword"]:
                    yaw = 360 - pd["data"][4][0][i]
                else:
                    yaw = 360 - pd["data"][3][0][i]
                ax.plot(pd["data"][1][0][i], pd["data"][2][0][i], color=pd["color"], marker=(3, 0, yaw), markersize=20)

ax.ticklabel_format(useOffset=False, style='plain')

# Title
ax.set_title(configs["plots"]["title"], size=legend_size)

# Labels and grid
ax.set_xlabel(configs["plots"]["xlabel"], size=legend_size*0.8)
ax.set_ylabel(configs["plots"]["ylabel"], size=legend_size*0.8)
ax.axis('equal')

try:
    xlims = (0, 0)
    xlims = (float(configs["plots"]["image"]["limits"]["xlim"][0]), float(configs["plots"]["image"]["limits"]["xlim"][1]))
    ylims = (0, 0)
    ylims = (float(configs["plots"]["image"]["limits"]["ylim"][0]), float(configs["plots"]["image"]["limits"]["ylim"][1]))
except KeyError as e:
    xlims, ylims = utils.calculate_limits(plot_data)
ax.set(xlim=xlims, ylim=ylims)
ax.grid()

# Legend
legends = []
count = 0
for pd in plot_data:
    if "pdf" not in pd["variable_keyword"]:
        legends.append(pd["variable_keyword"])
ax.legend(legends, prop={'size': legend_size})

fig.show()

fig.savefig(fname=os.path.join(path_saves, configs["plots"]["title"] + ".png"), format='png')

try:
    configs["plots"]["movie"]
except KeyError as e:
    # response = input("No movie specified, do you wish to proceed to movie making? Type \"[y]es\" to continue creating the video...\n")
    # if ("y" in response) or ("Y" in response) or (response == ""):
    #     pass
    # else:
    print("Ended program at image creation")
    exit(0)

# Make the movie
fig, ax = plt.subplots(1,1)

fig.set_size_inches((14, 10))

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()




print("The final video is x" + str(speed) + " faster and has a frame rate of " + str(fps)) # speed[0]

def make_frame(t):
    ax.cla()
    for pd in plot_data:
        # Determine the right index for timestamp
        err = 10000000000000000
        err_index = 0
        for time_stamp in pd["data"][0][0]:
            if abs(time_stamp - pd["data"][0][0][0] - t / duration * full_length) < err:
                err = abs(time_stamp - pd["data"][0][0][0] - t / duration * full_length)
                i = err_index
            err_index += 1
        # Check if there is any modification active
        try:
            if configs["plots"]["mod"] == "slap":
                if "pdf" in pd["variable_keyword"].lower():
                    covariance = [[pd["data"][1][i][0], pd["data"][1][i][1]], [pd["data"][2][i][0], pd["data"][2][i][1]]]

                    # for num, cov in enumerate(pd["data"]):
                    #     if num != 0:
                    #         covariance.append(cov[i])
                    #     print(covariance)
                    slap.plot_ellipse(covariance, ax, position, pd["color"])
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError as e:
            # Plot normal navigation
            if "nav" in pd["variable_keyword"] and "mvector" in pd["variable_keyword"]:
                position = (pd["data"][1][0][i], pd["data"][2][0][i])
                yaw = 360 - pd["data"][4][0][i]
            elif "nav" in pd["variable_keyword"]:
                yaw = 360 - pd["data"][4][0][i]
            else:
                yaw = 360 - pd["data"][3][0][i]
            ax.plot(pd["data"][1][0][:i], pd["data"][2][0][:i], color=pd["color"], label='_nolegend_')
            ax.plot(pd["data"][1][0][i], pd["data"][2][0][i], color=pd["color"], marker=(3, 0, yaw), markersize=20)
    
    ax.ticklabel_format(useOffset=False, style='plain')

    # Title
    ax.set_title(configs["plots"]["title"] + " - Video Speed: " + str(speed) + ", Frame Rate: " + str(fps), size=legend_size)

    # Labels and grid
    ax.set_xlabel(configs["plots"]["xlabel"], size=legend_size*0.8)
    ax.set_ylabel(configs["plots"]["ylabel"], size=legend_size*0.8)
    ax.axis('equal')
    ax.set(xlim=xlims, ylim=ylims)
    # ax.set_xlim(left=xlim_min)
    # ax.set_ylim([ylim_min, ylim_max])
    ax.grid()

    # Legend
    legends = []
    for pd in plot_data:
        legends.append(pd["variable_keyword"])
    ax.legend(legends, prop={'size': legend_size})

    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration=duration)
animation.write_videofile(os.path.join(path_saves, configs["plots"]["title"] + ".mp4"), fps=fps)

print("Output an image and a video. Enjoy!")