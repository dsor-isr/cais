import rosbag
import os
import time
import numpy as np
from datetime import datetime
from handyTools import *
from medusa_drivers_msgs import *

"""
Class responsable for read all topics related to medusa drivers
"""

class MedusaDrivers(object):
    def __init__(self, bag):
        self.__readMedusaDriversTopics(bag)

    def __readMedusaDriversTopics(self, bag):
        
        # init vectores to store data
        altimeterData = []
        gpsData = []
        batMonitData = []
        batMonitRaw = []
        inPressureData = []
        thrusterTest = []
        thrusterWash = []
        thrusterStop = []
        batMonitEqualize = []
        depthCellData = []
        imuData = []
        imupp = []
        inPressureFilter = []
        inPressureFilterDot = []
        parallelPortData = []
        dvlEnable = []
        dvlRaw = []
        thruster0Status = []
        thruster1Status = []
        thruster2Status = []
        thruster3Status = []
        thruster4Status = []
        thruster5Status = []

        # Get name of the vehicle
        vehicle_name = getNameOfVehicle(bag)
       
        if searchInTopics(bag, vehicle_name + '/drivers/altimeter/data'):
            altimeterData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/altimeter/data'))

        if searchInTopics(bag, vehicle_name + '/drivers/gps/data'):
            gpsData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/gps/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/bat_monit/data'):
            batMonitData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/bat_monit/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/bat_monit/raw'):
            batMonitRaw = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/bat_monit/raw')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/bat_monit/equalize'):
            batMonitEqualize = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/bat_monit/equalize')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/inside_pressure/data'):
            inPressureData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/inside_pressure/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/Thruster_Test'):
            thrusterTest = findTopic(bag, searchInTopics(bag, vehicle_name + '/Thruster_Test')[0])

        if searchInTopics(bag, vehicle_name + '/Thruster_Wash'):
            thrusterWash = findTopic(bag, searchInTopics(bag, vehicle_name + '/Thuster_Wash')[0])
        
        if searchInTopics(bag, vehicle_name + '/Thruster_Stop'):
            thrusterStop = findTopic(bag, searchInTopics(bag, vehicle_name + '/Thuster_Stop')[0])
 
        if searchInTopics(bag, vehicle_name + '/drivers/depth_cell/data'):
            depthCellData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/depth_cell/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/imu/data'):
            imuData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/imu/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/imu/imu_pp'):
            imupp = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/imu/imu_pp')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data'):
            inPressureFilter = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data_dot'):
            inPressureFilterDot = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data_dot')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/parallel_port/data'):
            parallelPortData = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/parallel_port/data')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/dvl/enable'):
            dvlEnable = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/dvl/enable')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/dvl/raw'):
            dvlRaw = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/dvl/raw')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/thruster0/Status'):
            thruster0Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster0/Status')[0])

        if searchInTopics(bag, vehicle_name + '/drivers/thruster1/Status'):
            thruster1Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster1/Status')[0])

        if searchInTopics(bag, vehicle_name + '/drivers/thruster2/Status'):
            thruster2Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster2/Status')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/thruster3/Status'):
            thruster3Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster3/Status')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/thruster4/Status'):
            thruster4Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster4/Status')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/thruster5/Status'):
            thruster5Status = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/thuster5/Status')[0])
        


        # Read altimeterData
        self.altimeterData = Float64()
        if altimeterData:
            for topic, msg, t in altimeterData:
                self.altimeterData.value.append(msg.data)
                self.altimeterData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # ReadgpsData 
        self.gpsData = mLatLonPos()
        if gpsData:
            for topic, msg, t in gpsData:
                self.gpsData.mode.append(msg.mode)
                self.gpsData.utc_time.append(msg.utc_time)
                self.gpsData.satellites.append(msg.satellites)
                self.gpsData.latitude.append(msg.latitude)
                self.gpsData.longitude.append(msg.longitude)
                self.gpsData.altitude.append(msg.altitude)
                self.gpsData.course.append(msg.course)
                self.gpsData.speed_over_ground.append(msg.speed_over_ground)
                self.gpsData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # ReadbatMonitData 
        self.batMonitData = mBatMonit()
        if batMonitData:
            for topic, msg, t in batMonitData:
                self.batMonitData.actual_charge.append(msg.actual_charge)
                self.batMonitData.charging.append(msg.charging)
                self.batMonitData.current.append(msg.current)
                self.batMonitData.equalize.append(msg.equalize)
                self.batMonitData.max_cell.append(msg.max_cell)
                self.batMonitData.max_temp.append(msg.max_temp)
                self.batMonitData.min_cell.append(msg.min_cell)
                self.batMonitData.min_temp.append(msg.min_temp)
                self.batMonitData.number_of_packs.append(msg.number_of_packs)
                self.batMonitData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read batMonitRaw 
        self.batMonitRaw = mBatMonitRaw()
        if batMonitRaw:
            for topic, msg, t in batMonitRaw:
                raw_splited = msg.sentence.split(',')
                if len(raw_splited) > 7:
                    try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                    except: pass
                    if raw_splited[1] == '1': #Pack 1
                        try: self.batMonitRaw.pack1_cell1.append(int(raw_splited[3]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell2.append(int(raw_splited[4]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell3.append(int(raw_splited[5]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell4.append(int(raw_splited[6]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell5.append(int(raw_splited[7]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell6.append(int(raw_splited[8]))
                        except: pass
                        try: self.batMonitRaw.pack1_cell7.append(int(raw_splited[9]))
                        except: pass
                    elif raw_splited[1] == '2': #Pack 2
                        try: self.batMonitRaw.pack2_cell1.append(int(raw_splited[3]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell2.append(int(raw_splited[4]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell3.append(int(raw_splited[5]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell4.append(int(raw_splited[6]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell5.append(int(raw_splited[7]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell6.append(int(raw_splited[8]))
                        except: pass
                        try: self.batMonitRaw.pack2_cell7.append(int(raw_splited[9]))
                        except: pass

        # Read batMonitEqualize 
        self.batMonitEqualize = Bool()
        if batMonitEqualize:
            for topic, msg, t in batMonitEqualize:
                self.batMonitEqualize.value.append(msg.data)
                self.batMonitEqualize.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
            
        # Read inPressureData 
        self.inPressureData = Pressure()
        if inPressureData:
            for topic, msg, t in inPressureData:
                self.inPressureData.pressure.append(msg.pressure)
                self.inPressureData.temperature.append(msg.temperature)
                self.inPressureData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thrusterTest 
        self.thrusterTest = Int8()
        if thrusterTest: 
            for topic, msg, t in thrusterTest:
                self.thrusterTest.value.append(msg.value)
                self.thrusterTest.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thrusterWash
        self.thrusterWash = Int8()
        if thrusterWash: 
            for topic, msg, t in thrusterWash:
                self.thrusterWash.value.append(msg.value)
                self.thrusterWash.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thrusterStop
        self.thrusterStop = Int8()
        if thrusterStop: 
            for topic, msg, t in thrusterStop:
                self.thrusterStop.value.append(msg.value)
                self.thrusterStop.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read depthCellData
        self.depthCellData = Pressure()
        if depthCellData:
            for topic, msg, t in depthCellData:
                self.depthCellData.pressure.append(msg.pressure)
                self.depthCellData.temperature.append(msg.temperature)
                self.depthCellData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read imuData
        self.imuData = mIMU()
        if imuData:
            for topic, msg, t in imuData:
                self.imuData.Yaw.append(msg.Yaw)
                self.imuData.Pitch.append(msg.Pitch)
                self.imuData.Roll.append(msg.Roll)
                self.imuData.Gx.append(msg.Gx)
                self.imuData.Gy.append(msg.Gy)
                self.imuData.Gz.append(msg.Gz)
                self.imuData.Mx.append(msg.Mx)
                self.imuData.My.append(msg.My)
                self.imuData.Mz.append(msg.Mz)
                self.imuData.Ax.append(msg.Ax)
                self.imuData.Ay.append(msg.Ay)
                self.imuData.Az.append(msg.Az)
                self.imuData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read imupp
        self.imupp = mIMU()
        if imupp:
            for topic, msg, t in imuData:
                self.imupp.mag_x.append(msg.mag_x)
                self.imupp.mag_y.append(msg.mag_y)
                self.imupp.mag_z.append(msg.mag_z)
                self.imupp.mag_abs.append(msg.mag_abs)
                self.iimupp.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read inPressureFilter
        self.inPressureFilter = Float64()
        if inPressureFilter:
            for topic, msg, t in inPressureFilter:
                self.inPressureFilter.value.append(msg.data)
                self.inPressureFilter.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read inPressureFilterDot
        self.inPressureFilterDot = Float64()
        if inPressureFilterDot:
            for topic, msg, t in inPressureFilter:
                self.inPressureFilterDot.value.append(msg.data)
                self.inPressureFilterDot.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read parallelPortData
        self.parallelPortData = Int8()
        if parallelPortData: 
            for topic, msg, t in parallelPortData:
                self.parallelPortData.value.append(msg.data)
                self.parallelPortData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read dvlEnable
        self.dvlEnable = Bool()
        if dvlEnable:
            for topic, msg, t in dvlEnable:
                self.dvlEnable.value.append(msg.data)
                self.batMonitEqualize.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read dvlRaw
        self.dvlRaw = navquest_dvlRes()
        if dvlRaw:
            for topic, msg, t in dvlRaw:
                self.dvlRaw.error_code.append(msg.error_code)
                self.dvlRaw.good.append(msg.good)
                self.dvlRaw.v_depth.append(msg.v_depth)
                self.dvlRaw.velo_rad.append(msg.velo_rad)
                self.dvlRaw.wvelo_rad.append(msg.wvelo_rad)
                self.dvlRaw.wvelo_credit.append(msg.wvelo_credit)
                self.dvlRaw.water_velo_instrument.append(msg.water_velo_instrument)
                self.dvlRaw.water_velo_earth.append(msg.water_velo_earth)
                self.dvlRaw.velo_instrument_flag.append(msg.velo_instrument_flag)
                self.dvlRaw.velo_earth_flag.append(msg.velo_earth_flag)
                self.dvlRaw.water_velo_instrument_flag.append(msg.water_velo_instrument_flag)
                self.dvlRaw.water_velo_earth_flag.append(msg.water_velo_earth_flag)
                self.dvlRaw.velo_instrument_flag.append(msg.velo_instrument_flag)
                self.dvlRaw.rph.append(msg.rph)
                self.dvlRaw.depth_estimate.append(msg.depth_estimate)
                self.dvlRaw.temperature.append(msg.temperature)
                self.dvlRaw.pressure.append(msg.pressure)
                self.dvlRaw.salinity.append(msg.salinity)
                self.dvlRaw.sound_speed.append(msg.sound_speed)
                self.dvlRaw.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thruster0Status
        self.thruster0Status = mThrusterStatus()
        if thruster0Status:
            for topic, msg, t in thruster0Status:
                self.thruster0Status.Current.append(msg.Current)
                self.thruster0Status.Temperature.append(msg.Temperature)
                self.thruster0Status.Errors.append(msg.Errors)
                self.thruster0Status.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thruster1Status
        self.thruster1Status = mThrusterStatus()
        if thruster1Status:
            for topic, msg, t in thruster1Status:
                self.thruster1Status.Current.append(msg.Current)
                self.thruster1Status.Temperature.append(msg.Temperature)
                self.thruster1Status.Errors.append(msg.Errors)
                self.thruster1Status.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thruster2Status
        self.thruster2Status = mThrusterStatus()
        if thruster2Status:
            for topic, msg, t in thruster0Status:
                self.thruster2Status.Current.append(msg.Current)
                self.thruster2Status.Temperature.append(msg.Temperature)
                self.thruster2Status.Errors.append(msg.Errors)
                self.thruster2Status.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thruster3Status
        self.thruster3Status = mThrusterStatus()
        if thruster3Status:
            for topic, msg, t in thruster3Status:
                self.thruster3Status.Current.append(msg.Current)
                self.thruster3Status.Temperature.append(msg.Temperature)
                self.thruster3Status.Errors.append(msg.Errors)
                self.thruster3Status.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thruster4Status
        self.thruster4Status = mThrusterStatus()
        if thruster4Status:
            for topic, msg, t in thruster4Status:
                self.thruster4Status.Current.append(msg.Current)
                self.thruster4Status.Temperature.append(msg.Temperature)
                self.thruster4Status.Errors.append(msg.Errors)
                self.thruster4Status.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

    # Getters
    def getAltimeterData(self):
        return self.altimeterData
    
    def getGPSData(self):
        return self.gpsData
   
    def getBatMonitData(self):
        return self.batMonitData
   
    def getBatMonitRaw(self):
        return self.batMonitRaw
    
    def getInPressureData(self):
        return self.inPressureData
    
    def getThrusterTest(self):
        return self.thrusterTest
    
    def getThrusterWash(self):
        return self.thrusterWash
    
    def getThrusterStop(self):
        return self.thrusterStop
    
    def getBatMonitEqalize(self):
        return self.batMonitEqualize
    
    def getDepthCellData(self):
        return self.depthCellData
    
    def getIMUData(self):
        return self.imuData
    
    def getIMUpp(self):
        return self.imupp
    
    def getInPressureFilter(self):
        return self.inPressureFilter
    
    def getInPressureFilterDot(self):
        return self.inPressureFilterDot
    
    def getParallelPortData(self):
        return self.parallelPortData
    
    def getDVLEnable(self):
        return self.dvlEnable
    
    def getDVLRaw(self):
        return self.dvlRaw
    
    def getThruster0Status(self):
        return self.thruster0Status
    
    def getThruster1Status(self):
        return self.thruster1Status
    
    def getThruster2Status(self):
        return self.thruster2Status
    
    def getThruster3Status(self):
        return self.thruster3Status
    
    def getThruster4Status(self):
        return self.thruster4Status
    
    def getThruster5Status(self):
        return self.thruster5Status
    























