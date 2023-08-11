# CAIS - Cluster of Analysis for Intelligent Systems: Bag Analysis

## 1. Introduction

The Bag Analysis module of CAIS provides the ability to process bags, creating a series of plots making use of the bags' topics. It also divides each bag into mission bags (if missions were performed during the bag recording), which are also processed in the same way as their "parent" bags.

This is an extensible tool, i.e., any new plots can be easily added to the configuration files in the config/ folder. More information on how to configure new plots is explained below.

## 2. Trials Data Files Format

Make sure the trials data folder (where the bags to be processed are located) and its subdirectories are correctly organised. Considering the folder is ~/trials_raw/, then each vehicle bag should be located as follows:

```shell
~/trials_raw/{{day_of_trials}}/vehicles/{{vehicle_name}}/ROSData/{{bag_name}}.bag
```

For example, a bag recorded on the mvector vehicle, on 20th January 2023, should be located at:

```shell
~/trials_raw/2023-01-20/vehicles/mvector/ROSData/
```

## 3. How to run:

Create a virtual environment, source it and install the requirements (you will have to source the virtual environment every time a new terminal is opened):

```shell
python -m venv venv/.
source venv/bin/activate
pip install -r requirements.txt
```

Run the BagAnalysis python script, specifying the path where the trials data is:

```shell
python BagAnalysis.py ~/trials_raw/ #the trials data is inside the folder trials_raw, in the root folder
```

## 4. Plot Configuration:

The configurations for each plot are located at the config/ folder, which are divided into two separate folders: drivers/ and missions/. The ones specified in missions/ are only plotted for the mission bags, while the ones in drivers/ are plotted for both the original and the mission bags.

The generic structure followed in each .yaml file is as follows:

```yaml
plots:
  plot-name-1: # change to whatever fits the plot's name, it is an identifier for the plot file
    name: "Title for the plot"
    axes:
      x:
        vehicles: # leave empty to plot for all vehicles
        label: "X axis label"
        topics:
          - "topic/to/be/plotted" # don't specify the vehicle name in the beginning of the topic
        fields:
          - "attribute_with_the_data" # or list of nested attributes
      y:
        vehicles: # leave empty to plot for all vehicles
        label: "Y axis label"
        topics:
          - "topic/to/be/plotted" # don't specify the vehicle name in the beginning of the topic
        fields:
          - "attribute_with_the_data" # or list of nested attributes
    plot_markers:
      - "lines" # specify the type of marker, could be "lines", "markers" or "lines+markers"
  
  plot-name-2:
    # ...
```

### 4.1. How to specify a topic

Topics should be specified without the name of the vehicle (in order to plot for all vehicles which publish that topic), but as detailed as possible, so as to avoid plotting an unwanted topic's data.

```yaml
# EXAMPLE: /mvector0/drivers/gps/data
topics:
  - "/mvector0/drivers/gps/data" # WRONG (specifies the vehicle)
  - "/drivers/gps" # WRONG (there are multiple topics that include this string: "/#vehicle#/drivers/gps/data" and "/#vehicle#/drivers/gps/raw")
  - "drivers/gps/data" # CORRECT
```

There is one exception to the previous rules: whenever we deal with a set of topics that are equal apart from an integer (for example, topics for each one of the vehicle's thrusters), the specified topic should only include the full topic up to that same integer, as shown below:

```yaml
# for these topics: "/mvector0/drivers/Thruster0/Status", "/mvector0/drivers/Thruster1/Status", "/mvector0/drivers/Thruster2/Status", "/mvector0/drivers/Thruster3/Status", "/mvector0/drivers/Thruster4/Status", "/mvector0/drivers/Thruster5/Status"
# only one configuration is needed:
topics:
  - "drivers/Thruster" # will plot for Thruster0, Thruster1, etc.
```

This prevents a lot of unnecessary work: for example, if there are 4 different plots needed for each of the 6 thrusters, only 4 configurations need to be written, instead of 6 * 4 = 24 configurations.

### 4.2. Specifying fields/attributes of a topic

In the majority of cases, the topic itself does not have the data do be plotted - it has attributes (or attributes of attributes - nested attributes) which may have the wanted data. In a simple case, where "topic_X" has an atttribute "attr_Y" with the data to be plotted, then the configuration should include:

```yaml
topics:
  - "topic_X"
fields:
  - "attr_Y"
```

In a more complex situation, where "topic_Z" has an attribute "attr_A", which has an attribute "attr_B", which has an attribute "attr_C" with the data to be plotted (nested attributes), then the configuration should include:

```yaml
topics:
  - "topic_Z"
fields:
  - ["attr_A", "attr_B", "attr_C"]
```

Real examples for both cases follow:

```yaml
# config/drivers/altimeter.yaml
plots:
  altimeter:
    name: "Altimeter"
    axes:
      x: # time
      y:
        vehicles: # for all vehicles
        label: "Altimeter [m]"
        topics:
          - "drivers/altimeter/data"
        fields:
          - "data" # <-- ATTRIBUTE WITH THE DATA
    plot_markers:
      - "lines"

# config/missions/pfollowing.yaml
plots:
  overview_pf:
    name: "Overview of Path Following"
    axes:
      x:
        vehicles: # for all vehicles
        label: "Easting [m]"
        topics:
          - "/nav/filter/state"
        fields:
          - ["position", "east"] # <-- NESTED ATTRIBUTES
      y:
        vehicles: # for all vehicles
        label: "Northing [m]"
        topics:
          - "/nav/filter/state"
        fields:
          - ["position", "north"] # <-- NESTED ATTRIBUTES
    plot_markers:
      - "lines"
```

### 4.3. Time series vs. XY Plots

Most plots needed are in fact just simple time series, where the data is in the Y axis, while its correspondent timestamps are represented in the X axis. In this case, the configuration only needs to specify the y axis (the x axis is left empty), as exemplified below:

```yaml
# config/drivers/altimeter.yaml
plots:
  altimeter:
    name: "Altimeter"
    axes:
      x: # time
      y:
        vehicles: # for all vehicles
        label: "Altimeter [m]"
        topics:
          - "drivers/altimeter/data"
        fields:
          - "data"
    plot_markers:
      - "lines"
```

When the plot has non-time data in both axes, naturally both of them need to be specified, as shown below (note that both need to have the same length - normally these are from the same topic, but different field):

```yaml
# config/missions/pfollowing.yaml
plots:
  overview_pf:
    name: "Overview of Path Following"
    axes:
      x:
        vehicles: # for all vehicles
        label: "Easting [m]"
        topics:
          - "/nav/filter/state"
        fields:
          - ["position", "east"]
      y:
        vehicles: # for all vehicles
        label: "Northing [m]"
        topics:
          - "/nav/filter/state"
        fields:
          - ["position", "north"]
    plot_markers:
      - "lines"
```

### 4.4. Plotting multiple lines

Sometimes, plots need multiple lines, providing information from multiple time series. If a plot with N different lines is needed, then the *plot_markers* list and the *topics* and *fields* lists, for each axes, should have N entries. Of course, if the plot is time-based, then the x axis configuration should still be left empty. Below, a case for a plot with 3 lines is presented:

```yaml
# config/missions/pfollowing.yaml
plots:
  overview_filter_dr_usbl:
    name: "Overview of Filter/DR/USBL"
    axes:
      x:
        vehicles: # for all vehicles
        label: "Easting [m]"
        topics:
          - "/mvector0/nav/filter/state" # <-- Line 1
          - "/mvector0/State_dr" # <-- Line 2
          - "/mvector0/State_usbl_est" # <-- Line 3
        fields:
          - ["position", "east"] # <-- Line 1
          - "X" # <-- Line 2
          - "X" # <-- Line 3
      y:
        vehicles: # for all vehicles
        label: "Northing [m]"
        topics:
          - "/mvector0/nav/filter/state" # <-- Line 1
          - "/mvector0/State_dr" # <-- Line 2
          - "/mvector0/State_usbl_est" # <-- Line 3
        fields:
          - ["position", "north"] # <-- Line 1
          - "Y" # <-- Line 2
          - "Y" # <-- Line 3
    plot_markers:
      - "lines" # <-- Line 1
      - "lines" # <-- Line 2
      - "lines+markers" # <-- Line 3
```

### 4.5. Data in vectors and indexation

Occasionally, the data in an attribute is stored in a vector, from which only a specific indexed entry of it is wanted for the plot. In these cases, an additional list *indexes* is added to the configuration (only needs to be specified when vector indexation is needed). If N lines are being plotted, the list *indexes* should have size N as well; if a certain line does not need indexation, its corresponding entry in the *indexes* list should be left empty. An example follows:

```yaml
# config/missions/pfollowing.yaml
plots:
  filter_vs_virtual_target:
    name: "Filter vs. Virtual Target"
    axes:
      x:
        vehicles: # for all vehicles
        label: "Easting [m]"
        topics:
          - "/nav/filter/state"
          - "/PathData"
        fields:
          - ["position", "east"]
          - "pd"
        indexes:
          -   # <-- Line 1 does NOT need indexation
          - 1 # <-- Line 2 needs indexation
      y:
        vehicles: # for all vehicles
        label: "Northing [m]"
        topics:
          - "/nav/filter/state"
          - "/PathData"
        fields:
          - ["position", "north"]
          - "pd"
        indexes:
          -   # <-- Line 1 does NOT need indexation
          - 0 # <-- Line 2 needs indexation
    plot_markers:
      - "lines"
      - "lines"
```