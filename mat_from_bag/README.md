# **This code consists in two steps:**
1. **Bag Syncing**
2. **Generation of *.mat* files**

## **1. Bag Syncing**
This step provides the ability to **cut sections** from the *input bags* according to a *reference bag*, such that the cut bags are **confined within the time interval** of the *reference bag*, making use of their gps utc time, since the internal clocks of each bag's vehicle are considered to not be synchronised a priori.

In "/bag_sync", there are three different folders:
  - "/reference_bag": where the *reference bag* can be stored
  - "/input_bags": where the *input bags* to be cut and synchronised with the *reference bag* are stored (REQUIRED)
  - "/output_bags": where the cut bags are stored after the code is ran

### **Example**
Given the *reference bag* "/bag_sync/reference_bag/mvector.bag" and the *input bags* "/bag_sync/input_bags/mblack.bag" and "/bag_sync/input_bags/mred.bag", then the command to be ran would simply be:

```shell
cd bag_sync
python sync_bags.py reference_bag/mvector.bag
```

The output result would be the cut bags in "/bag_sync/output_bags/", "mblack_cut.bag" and "mred_cut.bag".

## **2. Generation of *.mat* files** ##
This step provides the ability to generate a *.mat* file for the specified bag, according to the configuration file in "config/topics.yaml", where the topics and their chosen attributes are defined. The config file has a very simple structure, where for each wanted topic, the "topic_name", the wanted attributes and their wanted labels are defined.

### **Example**
To generate a *.mat* file for the bag "/bag_sync/output_bags/mblack_cut.bag", with the attributes "position.east" and "position.north" for the filter/state topic and the "utc_time" attribute for the gps topic, the config file should have the following:
```yaml
mblack_nav_filter_state: # this is just an ID and can be whatever you want
  topic_name: "/mblack0/nav/filter/state"
  fields: [["position", "east"], ["position", "north"]]
  var_name: ["easting", "northing"]
mblack_gps: # this is just an ID and can be whatever you want
  topic_name: "/mblack0/drivers/gps/data"
  fields: [["utc_time"]]
  var_name: ["utc_time"]
```
Then, just run:

```shell
python main.py /bag_sync/output_bags/mblack_cut.bag
```

and the output "mblack_cut.mat" file is now in the "output/" folder.