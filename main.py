import os
from handyTools import *
from software import SoftwarePlots
from farol_topics import FarolStack
from medusa_drivers import MedusaDrivers

if __name__ == '__main__':

    # NOTE: first call the script to reindex the bags
    
    pattern = [4,6,4] #padrao das missoes

    bags_folder = os.path.expanduser('~')+'/ROS_data'

    for root, dirs, files in os.walk(bags_folder, topdown=False):
        for name in files:
            if name.find('.bag') != -1 and name.find('_mission.bag') == -1:
                try:
                    bag = readBag(os.path.join(root, name))
                    vehicle_name = getNameOfVehicle(bag) #buscar nome veiculo
                    createMissionBags(bag, findTopic(bag, searchInTopics(bag, vehicle_name+'/Flag')[0]), pattern, os.path.join(root, name.split('.')[0])+'/missions')
                    medusaDrivers = MedusaDrivers(bag)
                except:
                    pass

    for root, dirs, files in os.walk(bags_folder, topdown=False):
        for name in files:
            if name.find('_mission.bag') != -1:
                print(name)
                try:
                    bag = readBag(os.path.join(root, name))
                    print('Mission bag read')
                    farolStack = FarolStack(bag)
                    print('Topics read')
                    plots = SoftwarePlots(os.path.join(root, name.split('.')[0]), farolStack) 
                    print('PLOTS MADE')
                except Exception as e:
                    print(e)
                    pass


