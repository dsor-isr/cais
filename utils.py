"""

Developers: whitemanatee > francisco.branco@tecnico.ulisboa.pt

Description: Utilities file for plotting overview 2D missions
             and make movie

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


def help():
    print("HELP TIPS")
    print("- The files should all be inside the working directory named \"files/\"")
    print("- If the files don't have a vehicle specified in the name, they will be attributed a random color")
    print("- There must be an existing \"saves/\" folder at the working directory")


def search_topic(topic, keywords):
    for k in keywords:
        if k.lower().find(topic.lower()) >= 0:
            return k
    return None


def calculate_limits(plot_data):
    xlim_min = 100000000000000000000000000
    xlim_max = -100000000000000000000000000
    ylim_min = 100000000000000000000000000
    ylim_max = -100000000000000000000000000
    for pd in plot_data:
        if "pdf" not in pd["variable_keyword"]:
            for i in range(len(pd["data"][1][0])):
                xlim_min = min(xlim_min, pd["data"][1][0][i])
                xlim_max = max(xlim_max, pd["data"][1][0][i])
                ylim_min = min(ylim_min, pd["data"][2][0][i])
                ylim_max = max(ylim_max, pd["data"][2][0][i])
    x_threshold = 1 * (xlim_max - xlim_min) # 0.3
    y_threshold = 1 * (ylim_max - ylim_min)
    xlim_min -= x_threshold
    xlim_max += x_threshold
    ylim_min -= y_threshold
    ylim_max += y_threshold
    return (xlim_min, xlim_max), (ylim_min, ylim_max)