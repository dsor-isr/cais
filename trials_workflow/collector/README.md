# CAIS - Cluster of Analysis for Intelligent Systems: Collector

## 1. Introduction

The *collector* module of CAIS provides the ability to extract data from the vehicles to the local pc this script is ran on, namely bags, logs and the source code, after water trials.

**[ IMPORTANT ] This module is the FIRST part of the TRIALS WORKFLOW and should be run in order to extract the data from all the vehicles deployed in the water trials. It should be followed by the [*reindex* module](../reindex/README.md) part.**

## 2. How to run:

In order to know which arguments the script accepts, just run:

```shell
python collector.py -h
```

For example, running the following command line collects the bags recorded on the date `2023-09-21` to a local folder named `Castelo_de_Bode_RAMONES` inside `~/trials_raw/`. The data is copied via ssh, using the user `ubuntu` and the IP `glider` (in this case, it is defined in `/etc/hosts` file).

```shell
python collector.py glider --date 2023-09-21 --name Castelo_de_Bode_RAMONES --user ubuntu
```

Following the next example, it is also possible to run this script once and collect bags from different IP's (`mvector`, `mred`, `mblack`).

```shell
python collector.py mvector mred mblack --date 2023-02-17 --name SLAP --user medusa
```

Moreover, the IP can also be specified directly:

```shell
python collector.py 192.168.99.99 --date 9999-99-99 --name Example --user example
```

For the sake of convenience, usual IP's such as `mred`, `mvector`, `mvector`, `delfim` and `glider` have no need for its user to be specified. For example:

```shell
python collector.py glider --date 2023-09-21 --name Castelo_de_Bode_RAMONES
```