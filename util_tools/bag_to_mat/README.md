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