# CAIS - Cluster of Analysis for Intelligent Systems: Reindex

## 1. Introduction

The *reindex* module of CAIS provides the ability to fix .bag files' indexation, which might be left broken after recording, due to improper closing or other issues.

**[ IMPORTANT ] This module is the SECOND part of the TRIALS WORKFLOW and should be run in order to reindex all the collected bags. At this point, all the collected data is in a folder named after the trials day and should be copied over to the servers (on whale: /mnt/nfs/developers/trials_ROSData/). It should be followed by the last part, the [*bag_analysis* module](../bag_analysis/README.md).**

## 2. How to run:

In order to know which arguments the script accepts, just run:

```shell
python reindex.py -h
```

Basically, it just accepts the path to the folder in which the bags to be reindexed are. Simply run:

```shell
python reindex.py /path/to/folder/
```

This way, `*.active` bags will be renamed, all bags will be reindexed and the original `*.orig.bag` will be erased.