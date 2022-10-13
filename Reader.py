import os
from readDrivers import Drivers
from readMissions import Missions
from readUSBL import DriverUSBL
from handyTools import *

"""
Class Reader responsable to find all .bag files into a specifica folder and call 
methods to make a Driver and Mission Analise
"""
class Reader(object):
    def __init__(self):
        pass
    
    # drivers analise
    def driversAnalise(self, bag, datafolder):
        plotDrivers = Drivers(datafolder + '/drivers')
        drivers_topics_list = searchInTopics(bag, 'drivers')
        for i in drivers_topics_list:
            plotDrivers.analizeDriverData(i, findTopic(bag, i))

        # for USBL -> key word is acomms
        plotUSBL = DriverUSBL(datafolder + '/drivers/USBL')
        usbl_topics_list = searchInTopics(bag, 'acomms/modem')
        if(usbl_topics_list):
            for i in usbl_topics_list:
                plotUSBL.analizeUSBLdriverData(i, findTopic(bag, i))
        
        usbl_topics_list = searchInTopics(bag, '/sensors/usbl_fix')
        if(usbl_topics_list):
            for i in usbl_topics_list:
                plotUSBL.analizeSensorsUSBLFixData(i, findTopic(bag, i))

    # make a mission analize
    def missionsAnalise(self, bag, dataFolder):
        plotMissions = Missions(dataFolder)
        plotMissions.makePlots(bag)
    
    # Divide a .bag into small mission bags, if it exists 
    def createMissionBags(self, bag, dataFolder, pattern):
        mission_bags = Missions(dataFolder + '/missions')
        mission_bags.divideBagsPerMission(bag, findTopic(bag, searchInTopics(bag, '/Flag')[0]), pattern)
        

if __name__ == '__main__':
    reader = Reader()

    # Set the pattern correspondent to the mission
    # pattern = [4,6,4]
    pattern = [6,4,0]
    # Set bags folder to process
    bags_folder = os.path.expanduser('~')+'/ROS_data'
    
    # search for any .bag that exists into a specific path, and for each one make a driver analise
    for root, dirs, files in os.walk(bags_folder, topdown=False):
        for name in files:
            # check if the file is a .bag or a _mission.bag
            if name.find('.bag') != -1 and name.find('_mission.bag') == -1:
                try: 
                    bag = readBag(os.path.join(root, name))
                    reader.driversAnalise(bag, os.path.join(root, name.split('.')[0]))
                    reader.createMissionBags(bag, os.path.join(root, name.split('.')[0]), pattern)
                except:
                    pass
    # search for any ._mission.bag that exists into a specific path, and for each one make a misson analise 
    # and a driver analise
    for root, dirs, files in os.walk(bags_folder, topdown=False):
        for name in files:
            if name.find('_mission.bag') != -1:
                try:
                    bag = readBag(os.path.join(root, name))
                    reader.driversAnalise(bag, os.path.join(root, name.split('.')[0]))
                    reader.missionsAnalise(bag, os.path.join(root, name.split('.')[0])) 
                except:
                    pass
