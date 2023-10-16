# CAIS - Cluster of Analysis for Intelligent Systems: Web Application

The Cluster of Analysis for Intelligent Systems (CAIS) web application is built using [Dash](https://plotly.com/dash/), a famework designed to build applications in Python.

## How to run it

There are two ways to use it. Either with a docker image or by running it directly. 


**Run with docker**

To build the docker image, run: `docker build -t <image_name> .`
< image_name > should be replaced with the desired name for the containerized app.

To run the created image, run: `docker run -v $(pwd)/app:$(pwd)/app -w $(pwd)/app -p 8050:8050 <image_name>`
The flags used to build and run the docker image are explained in depth in the [documentation](https://docs.docker.com/engine/reference/commandline/run/). Either way, most of the times all of the above flags will be required to run CAIS. 

`-p 8040:8050` This specifies that port 8050 of the container should be connected to port 8040 of the machine it is running on. This step is essential to actual make it possible to interact with CAIS on a browser.

`-w $(pwd)/app` This specifies the working directory inside the container's own file system.

The last option `-v $(pwd)/app:$(pwd)/app` is very particular to the way the app works. Since CAIS will be reading and writing to the file system there are two ways to go about it:

1. Use the container's own file system. In this case, `-v $(pwd)/app:$(pwd)/app` isn't needed at all. What that flag does is mount the local machine's app directory (supposing that the present working directory is cais's directory) to a directory with the same name on the container's file system. However, if this flag is not passed, the plots will be needed to be built onto the container itself. See bellow on how to modify the dockerfile to accomodate that.

2. Using your own file system. Simply run with `-v $(pwd)/app:$(pwd)/app`


**Run with python**

The CAIS web app assumes it is being run from it's directory, so the first step is getting there.
`cd /path/to/cais/app`
Then simply invoke it with python
`python3 app.py`


## How to open it with a browser

It first helps to know how Dash apps are run code-wise. In a very simple way, Dash apps are run like this:
```
app = Dash(__name__)
server = app.server

(...)

app.run_server(debug=False, dev_tools_hot_reload=False, host='0.0.0.0') 
```

By default, Dash apps run on port 8050. The first relevant part is `host='0.0.0.0'` This is used if you want it to be run using your IP address, which means you would access it in your browser of choice by going to [https://https//XXX.XXX.XXX.XXX:8050](https://https//XXX.XXX.XXX.XXX:8050) where XXX.XXX.XXX.XXX is your IP address. If you omit the host argument, the app is run on the localhost [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

To figure out your IP address run `ip r` on a linux system terminal or `ipconfig /all` on Windows's command prompt.

Suppose you run `ip r`. It will return something like this:
```
default via XXX.XXX.XXX.1 dev eth0 proto kernel
XXX.XXX.XXX.XXX/K dev docker0 proto kernel scope link src XXX.XXX.XXX.1 linkdown
XXX.XXX.XXX.XXX/K' dev eth0 proto kernel scope link src YYY.YYY.YYY.YYY
```
Your IP will be *YYY.YYY.YYY.YYY*

In windows, the output will be quite larger, but the relevant bit is the IPv4 Address.

## CAIS file tree

In a very high level description, CAIS goes through the file system in a Depth-First-Search like way, albeit interactive, where at each level the user makes a decision on which directory/file to pick next. There are some additional directories that never show up, but nevertheless are there for organizational reasons. Naturally, since these directories aren't shown to the user (they're "skipped"), the underlying algorithm assumes their existence, which means that if they are removed, CAIS will stop working properly.

For this reason, if you are running CAIS outside the docker or using your own local file system, it is essential that the overall structure look something like this:
```
| cais
|    | app
|    |    | app.py
|    |    | (...)
|    |    | <other_files>
|    |    | (...)
|    |    | assets
|    |    |    | logos
|    |    |    |    | DSOR_logo_v05a.jpg
|    |    |    |    | isr_logo_red_background.png
|    |    |    |    | isr_logo_white_background.png
|    |    |    | days
|    |    |    |    | <some_date>
|    |    |    |    |    | Vehicles
|    |    |    |    |    |    | <vehicle_1>
|    |    |    |    |    |    | (...)
|    |    |    |    |    |    | <vehicle_N>
|    |    |    |    |    |    |    | plots
|    |    |    |    |    |    |    |    | Missions
|    |    |    |    |    |    |    |    |    | <number_mission>
|    |    |    |    |    |    |    |    |    |    | <plot.html>
|    |    |    |    |    |    |    |    | Overall
|    |    |    |    |    |    |    |    |    | <drivers>
|    |    |    |    |    |    |    |    |    |    | <plot.html>
```
        

## dev_tools_hot_reload

Dash has something called [Code Reloading and Hot Reload](https://dash.plotly.com/devtools). This makes Dash refresh your browser whenever a change is made to the code (Code Reloading) or a file is saved (Hot Reload). Since CAIS frequently writes to the file system and Hot Reload doesn't save the app's current state, Hot Reload is incredibly detrimental to CAIS's functionalities, so it should be generally run with `app.run_server(dev_tools_hot_reload=False)`

## Tests

CAIS already has tests to check some of it's backend's behaviour. The tests are written in Python using [Pytest](https://docs.pytest.org/en/7.3.x/). To run them all, simply run test.sh `/path/to/cais/app/test.sh`


## What plots are filtered by what drivers?

Inside the directory of each day, there is a file called `drivers.json`. This file maps each different plot to the corresponding type of driver. Plots not necessarily associated with one driver or another fall into the "mission specific" category.

These *json* files are created either when the *Update Dropdowns* button, on the profile creation menu, is clicked or every 7 days after the webapp starts running (assuming the process isn't finished or dies in the meantime). The creation of these files is implemented in `extract_plot_names.py`, where most of the domain logic, regarding finding and computing lists of all the plots and drivers, is found.