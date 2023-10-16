# CAIS - Cluster of Analysis for Intelligent Systems: Inter-Bag Synchronisation

The *inter_bag_sync* module of CAIS provides the ability to **cut sections** from the *input bags* according to a *reference bag*, such that the cut bags are **confined within the time interval** of the *reference bag*, making use of their gps utc time, since the internal clocks of each bag's vehicle are considered to not be synchronised a priori.

In "/bag_sync", there are three different folders:
  - "/reference_bag": where the *reference bag* can be stored
  - "/input_bags": where the *input bags* to be cut and synchronised with the *reference bag* are stored (REQUIRED)
  - "/output_bags": where the cut bags are stored after the code is ran

## **Example**
Given the *reference bag* "/bag_sync/reference_bag/mvector.bag" and the *input bags* "/bag_sync/input_bags/mblack.bag" and "/bag_sync/input_bags/mred.bag", then the command to be ran would simply be:

```shell
cd bag_sync
python sync_bags.py reference_bag/mvector.bag
```

The output result would be the cut bags in "/bag_sync/output_bags/", "mblack_cut.bag" and "mred_cut.bag".