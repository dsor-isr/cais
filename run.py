"""

Developers: whitemanatee > francisco.branco@tecnico.ulisboa.pt

Description: Script that reads a .mat file from rosbags with
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
import numpy
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid number of arguments: " + str(len(sys.argv) - 1))
        exit(1)
    try:
        mat = scipy.io.loadmat(sys.argv[1])
    except FileNotFoundError as e:
        print(e)
        exit(1)
    
    non_data = ("__header__", "__version__", "__globals__")
    for keyword in non_data:
        del mat[keyword]
    keyword = list(mat.keys())[0]
    data = mat[keyword][0][0]

    # Define the variables of interest
    #keys = ("Time", "North", "East", "Yaw")

    
    
    # Check if file is valid
    if len(data) != 4:
        print("Invalid number of variables in the .mat file: " + str(len(data)))
        exit(1)
    # for key in keys:
    #     if key not in data.dtype:
    #         print("The following variable does not exist in the .mat file: " + key)
    #         exit(1)


    legend_size = 15

    fig, ax = plt.subplots(1,1)

    fig.set_size_inches((14, 10))

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    #ax.plot(data[2], data[1], color='blue', linestyle='--')
    ax.plot(data[2], data[1], color='orange')
    ax.ticklabel_format(useOffset=False, style='plain')

    # Title
    ax.set_title('Delfim Multi-Azimuth Mission', size=legend_size)

    # Labels and grid
    ax.set_xlabel('Northing [m]', size=legend_size*0.8)
    ax.set_ylabel('Easting [m]', size=legend_size*0.8)
    ax.grid()
    ax.axis('equal')

    # Legend
    #ax.legend(['Path','Position'], prop={'size': legend_size})

    fig.show()
    file_name, ext = sys.argv[1].split('.')
    
    fig.savefig(fname=file_name + ".png", format='png')

    input("Press Enter to continue...")

    duration = 60
    full_length = data[0][-1] - data[0][0]
    factor = 1/64 # 64
    fps = len(data[0]) * factor / duration
    speed = full_length / duration

    print("The final video is x" + str(speed[0]) + " faster")

    def make_frame(t):
        i = int(len(data[0]) * t / duration)
        if i >= len(data[0]):
            i = len(data[0]) - 1

        ax.cla()

        ax.plot(data[2][:i], data[1][:i], color='orange')
        ax.plot(data[2][i], data[1][i], color='orange', marker=(3, 0, 360 - data[3][i]), markersize=20)
        ax.ticklabel_format(useOffset=False, style='plain')

        # Title
        ax.set_title('Delfim Multi-Azimuth Mission', size=legend_size)

        # Labels and grid
        ax.set_xlabel('Northing [m]', size=legend_size*0.8)
        ax.set_ylabel('Easting [m]', size=legend_size*0.8)
        ax.grid()
        ax.axis('equal')

        # Legend
        #ax.legend(['Path','Position'], prop={'size': legend_size})

        return mplfig_to_npimage(fig)

    animation = VideoClip(make_frame, duration=duration)
    animation.write_videofile(file_name + ".mp4", fps=fps)

    print("Output an image and a video. Enjoy!")