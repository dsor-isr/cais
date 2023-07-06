import rosbag
import os
import time
import numpy as np
from datetime import datetime
from handyTools import *
from farol_msgs import *

"""
Class responsable for read all topics from Farol stack
"""

class FarolStack(object):
    def __init__(self, bag):
        self.__readFarolTopics(bag)
        self.getFlag()        
        self.getRefSurge()
        self.getRefSway()    
        self.getRefHeave()
        self.getRefYawRate()
        self.getRefYaw()
        self.getRefDepth()
        self.getRefAltitude()
        self.getRefPitch()
        self.getRefRoll()
        self.getRefPitchRate()
        self.getRefRollRate()
        self.getRefAltitudeSafety()
        self.getRefDepthSafety()
        self.getRPMCommand()
        self.getUsblFix()
        self.getFilterState()
        self.getFilterCurrents()
        self.getFilterStateDR()
        self.getFilterStateUSBL()
        self.getStateGT()
        self.getStateUSBL()
        self.getThrustBodyRequest()
        self.getForceBypass()
        self.getPathData()
        self.getPFvc()
        self.getPFGamma()
        self.getPFDebug()
        self.getInternalGamma()
        self.getExternalGamma()
        self.getAcommsFilterState()
        self.getAcommsUSBLFix()
        self.getAcommsGNSS()
        self.getAcommsModemRecv()
        self.getAcommsModemSend()

    def __readFarolTopics(self, bag):
        
        # init vectores to store data
        flag = []
        ref_surge = []
        ref_sway = []
        ref_heave = []
        ref_yaw_rate = []
        ref_yaw = []
        ref_depth = []
        ref_altitude = []
        ref_pitch = []
        ref_roll = []
        ref_pitch_rate = []
        ref_roll_rate = []
        ref_altitude_safety = []
        ref_depth_safety = []
        rpm_command = []
        usbl_fix = []
        filter_state = []
        filter_currents = []
        filter_state_dr = []
        filter_state_usbl = []
        State_gt = []
        State_usbl = []
        thrust_body_request = []
        force_bypass = []
        pathData = []
        pf_vc = []
        pf_gamma = []
        pf_debug = []
        internal_gamma = []
        external_gamma = []
        acomms_filter_state = []
        acomms_usbl_fix = []
        acomms_gnss = []
        acommsModemRecv = []
        acommsModemSend = []

        # Get name of the vehicle
        vehicle_name = getNameOfVehicle(bag)
        
        if searchInTopics(bag, vehicle_name + '/Flag'):
            flag = findTopic(bag, searchInTopics(bag, vehicle_name + '/Flag')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/surge'):
            ref_surge = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/surge')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/sway'):
            ref_sway = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/sway')[0])

        if searchInTopics(bag, vehicle_name + '/ref/heave'):
            ref_heave = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/heave')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/yaw_rate'):
            ref_yaw_rate = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/yaw_rate')[0])

        if searchInTopics(bag, vehicle_name + '/ref/yaw'):
            ref_yaw = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/yaw')[0])

        if searchInTopics(bag, vehicle_name + '/ref/depth'):
            ref_depth = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/depth')[0])
            
        if searchInTopics(bag, vehicle_name + '/ref/altitude'):
            ref_altitude = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/altitude')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/pitch'):
            ref_pitch = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/pitch')[0])

        if searchInTopics(bag, vehicle_name + '/ref/roll'):
            ref_roll = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/roll')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/pitch_rate'):
            ref_pitch_rate = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/pitch_rate')[0])

        if searchInTopics(bag, vehicle_name + '/ref/roll_rate'):
            ref_roll_rate = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/roll_rate')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/altitude_safety'):
            ref_altitude_safety = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/altitude_safety')[0])
        
        if searchInTopics(bag, vehicle_name + '/ref/depth_safety'):
            ref_depth_safety = findTopic(bag, searchInTopics(bag, vehicle_name + '/ref/depth_safety')[0])

        if searchInTopics(bag, vehicle_name + '/thrusters/rpm_command'):
            rpm_command = findTopic(bag, searchInTopics(bag, vehicle_name + '/thrusters/rpm_command')[0])
        
        if searchInTopics(bag, vehicle_name + '/sensors/usbl_fix'):
            usbl_fix = findTopic(bag, searchInTopics(bag, vehicle_name + '/sensors/usbl_fix')[0])
        
        if searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data'):
            inside_pressure_filter_data = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data')[0])

        if searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data_dot'):
            inside_pressure_filter_data_dot = findTopic(bag, searchInTopics(bag, vehicle_name + '/drivers/inside_pressure_filter/data_dot')[0])
        
        if searchInTopics(bag, vehicle_name + '/nav/filter/state'):
            filter_state = findTopic(bag, searchInTopics(bag, vehicle_name + '/nav/filter/state')[0])
        
        if searchInTopics(bag, vehicle_name + '/nav/filter/currents'):
           filter_currents = findTopic(bag, searchInTopics(bag, vehicle_name + '/nav/filter/currents')[0])
        
        if searchInTopics(bag, vehicle_name + '/nav/filter/state_dr'):
           filter_state_dr = findTopic(bag, searchInTopics(bag, vehicle_name + '/nav/filter/state_dr')[0])
        
        if searchInTopics(bag, vehicle_name + '/nav/filter/usbl_est'):
           filter_state_usbl = findTopic(bag, searchInTopics(bag, vehicle_name + '/nav/filter/usbl_est')[0])
        
        if searchInTopics(bag, vehicle_name + '/State_gt'):
           State_gt = findTopic(bag, searchInTopics(bag, vehicle_name + '/State_gt')[0])
        
        if searchInTopics(bag, vehicle_name + '/State_usbl_est'):
           State_usbl = findTopic(bag, searchInTopics(bag, vehicle_name + '/State_usbl_est')[0])
        
        if searchInTopics(bag, vehicle_name + '/thrust_body_request'):
           thrust_body_request = findTopic(bag, searchInTopics(bag, vehicle_name + '/thrust_body_request')[0])
        
        if searchInTopics(bag, vehicle_name + '/force_bypass'):
           force_bypass = findTopic(bag, searchInTopics(bag, vehicle_name + '/force_bypass')[0])
        
        if searchInTopics(bag, vehicle_name + '/PathData'):
           pathData = findTopic(bag, searchInTopics(bag, vehicle_name + '/PathData')[0])
        
        if searchInTopics(bag, vehicle_name + '/PF/vc'):
           pf_vc = findTopic(bag, searchInTopics(bag, vehicle_name + '/PF/vc')[0])
        
        if searchInTopics(bag, vehicle_name + '/Gamma'):
           pf_gamma = findTopic(bag, searchInTopics(bag, vehicle_name + '/Gamma')[0])
        
        if searchInTopics(bag, vehicle_name + '/pfollowing/debug'):
           pf_debug = findTopic(bag, searchInTopics(bag, vehicle_name + '/pfollowing/debug')[0])
        
        if searchInTopics(bag, vehicle_name + '/Internal/Gamma'):
           internal_gamma = findTopic(bag, searchInTopics(bag, vehicle_name + '/Internal/Gamma')[0])
        
        if searchInTopics(bag, vehicle_name + '/External/Gamma'):
           external_gamma = findTopic(bag, searchInTopics(bag, vehicle_name + '/External/Gamma')[0])
        
        if searchInTopics(bag, vehicle_name + '/acomms/nav/filter/state'):
           acomms_filter_state = findTopic(bag, searchInTopics(bag, vehicle_name + '/acomms/nav/filter/state')[0])
        
        if searchInTopics(bag, vehicle_name + '/acomms/modem/measurement/usbl_fix'):
           acomms_usbl_fix = findTopic(bag, searchInTopics(bag, vehicle_name + '/acomms/modem/measurement/usbl_fix')[0])
        
        if searchInTopics(bag, vehicle_name + '/acomms/nav/filter/gnss'):
           acomms_gnss =findTopic(bag, searchInTopics(bag, vehicle_name + '/acomms/nav/filter/gnss')[0])
        
        if searchInTopics(bag, vehicle_name + '/acomms/modem/recv'):
           acommsModemRecv = findTopic(bag, searchInTopics(bag, vehicle_name + '/acomms/modem/recv')[0])
        
        if searchInTopics(bag, vehicle_name + '/acomms/modem/send'):
           acommsModemSend = findTopic(bag, searchInTopics(bag, vehicle_name + '/acomms/modem/send')[0])
        
        # Read flag topic
        self.flag = Int8()
        if flag:
            for topic, msg, t in flag:
                self.flag.value.append(msg.data)
                self.flag.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_surge
        self.ref_surge = Int8()
        if ref_surge:
            for topic, msg, t in ref_surge:
                self.ref_surge.value.append(msg.data)
                self.ref_surge.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_sway
        self.ref_sway = Int8()
        if ref_sway:
            for topic, msg, t in ref_sway:
                self.ref_sway.value.append(msg.data)
                self.ref_sway.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_heave
        self.ref_heave = Int8()
        if ref_heave:
            for topic, msg, t in ref_heave:
                self.ref_heave.value.append(msg.data)
                self.ref_heave.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # # Read ref_yaw_rate
        self.ref_yaw_rate = Int8()
        if ref_yaw_rate:
            for topic, msg, t in ref_yaw_rate:
                self.ref_yaw_rate.value.append(msg.data)
                self.ref_yaw_rate.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read ref_yaw
        self.ref_yaw = Int8()
        if ref_yaw:
            for topic, msg, t in ref_yaw:
                self.ref_yaw.value.append(msg.data)
                self.ref_yaw.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read ref_depth
        self.ref_depth = Int8()
        if ref_depth:
            for topic, msg, t in ref_depth:
                self.ref_depth.value.append(msg.data)
                self.ref_depth.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read ref_altitude
        self.ref_altitude = Int8()
        if ref_altitude:
            for topic, msg, t in ref_altitude:
                self.ref_altitude.value.append(msg.data)
                self.ref_altitude.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read ref_pitch
        self.ref_pitch = Int8()
        if ref_pitch:
            for topic, msg, t in ref_pitch:
                self.ref_pitch.value.append(msg.data)
                self.ref_pitch.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_roll
        self.ref_roll = Int8()
        if ref_roll:
            for topic, msg, t in ref_roll:
                self.ref_roll.value.append(msg.data)
                self.ref_roll.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_pitch_rate
        self.ref_pitch_rate = Int8()
        if ref_pitch_rate:
            for topic, msg, t in ref_pitch_rate:
                self.ref_pitch_rate.value.append(msg.data)
                self.ref_pitch_rate.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_roll_rate
        self.ref_roll_rate = Int8()
        if ref_roll_rate:
            for topic, msg, t in ref_roll_rate:
                self.ref_roll_rate.value.append(msg.data)
                self.ref_roll_rate.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_altitude_safety
        self.ref_altitude_safety = Int8()
        if ref_altitude_safety:
            for topic, msg, t in ref_altitude_safety:
                self.ref_altitude_safety.value.append(msg.data)
                self.ref_altitude_safety.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read ref_depth_safety
        self.ref_depth_safety = Int8()
        if ref_depth_safety:
            for topic, msg, t in ref_roll_rate:
                self.ref_depth_safety.value.append(msg.data)
                self.ref_depth_safety.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read rpm_command
        self.rpm_command = Thruster()
        if rpm_command:
            for topic, msg, t in rpm_command:
                self.rpm_command.id.append(msg.id)
                self.rpm_command.value.append(msg.value)
                self.rpm_command.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read usbl_fix 
        self.usbl_fix = mUSBLFix()
        if usbl_fix:
            for topic, msg, t in usbl_fix:
                self.usbl_fix.bearing.append(msg.bearing)
                self.usbl_fix.bearing_raw.append(msg.bearing_raw)
                self.usbl_fix.elevation.append(msg.elevation)
                self.usbl_fix.elevation_raw.append(msg.elevation_raw)
                self.usbl_fix.range.append(msg.range)
                self.usbl_fix.relative_position.append(msg.relative_position)
                self.usbl_fix.position_covariance.append(msg.position_covariance)
                self.usbl_fix.sound_speed.append(msg.sound_speed)
                self.usbl_fix.type.append(msg.type)
                self.usbl_fix.source_id.append(msg.source_id)
                self.usbl_fix.source_frame_id.append(msg.source_frame_id)
                self.usbl_fix.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))


        # Read filter_state
        self.filter_state = NavigationStatus()
        if filter_state:
            for topic, msg, t in filter_state:
                self.filter_state.altitude.append(msg.altitude)
                self.filter_state.body_velocity_x.append(msg.body_velocity.x)
                self.filter_state.body_velocity_y.append(msg.body_velocity.y)
                self.filter_state.global_position_altitude.append(msg.global_position.altitude)
                self.filter_state.global_position_latitude.append(msg.global_position.latitude)
                self.filter_state.orientation_x.append(msg.orientation.x)
                self.filter_state.orientation_y.append(msg.orientation.y)
                self.filter_state.orientation_z.append(msg.orientation.z)
                self.filter_state.orientation_rate_x.append(msg.orientation_rate.x)
                self.filter_state.orientation_rate_y.append(msg.orientation_rate.y)
                self.filter_state.orientation_rate_z.append(msg.orientation_rate.z)
                self.filter_state.orientation_variance_x.append(msg.orientation_variance.x)
                self.filter_state.orientation_variance_y.append(msg.orientation_variance.y)
                self.filter_state.orientation_variance_z.append(msg.orientation_variance.z)
                self.filter_state.origin_altitude.append(msg.origin.altitude)
                self.filter_state.origin_latitude.append(msg.origin.latitude)
                self.filter_state.origin_longitude.append(msg.origin.longitude)
                self.filter_state.position_depth.append(msg.position.depth)
                self.filter_state.position_east.append(msg.position.east)
                self.filter_state.position_north.append(msg.position.north)
                self.filter_state.position_variance_depth.append(msg.position_variance.depth)
                self.filter_state.position_variance_east.append(msg.position_variance.east)
                self.filter_state.position_variance_north.append(msg.position_variance.north)
                self.filter_state.seafloor_velocity_x.append(msg.seafloor_velocity.x)
                self.filter_state.seafloor_velocity_y.append(msg.seafloor_velocity.y)
                self.filter_state.seafloor_velocity_z.append(msg.seafloor_velocity.z)
                self.filter_state.status.append(msg.status)
                self.filter_state.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read filter_currents
        self.filter_currents = Currents()
        if filter_currents:
            for topic, msg, t in filter_currents:
                self.filter_currents.x_current.append(msg.x_current)
                self.filter_currents.y_current.append(msg.y_current)
                self.filter_currents.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read filter_state_dr
        self.filter_state_dr = NavigationStatus()
        if filter_state_dr:
            for topic, msg, t in filter_state_dr:
                self.filter_state_dr.altitude.append(msg.altitude)
                self.filter_state_dr.body_velocity_x.append(msg.body_velocity.x)
                self.filter_state_dr.body_velocity_y.append(msg.body_velocity.y)
                self.filter_state_dr.global_position_altitude.append(msg.global_position.altitude)
                self.filter_state_dr.global_position_latitude.append(msg.global_position.latitude)
                self.filter_state_dr.orientation_x.append(msg.orientation.x)
                self.filter_state_dr.orientation_y.append(msg.orientation.y)
                self.filter_state_dr.orientation_z.append(msg.orientation.z)
                self.filter_state_dr.orientation_rate_x.append(msg.orientation_rate.x)
                self.filter_state_dr.orientation_rate_y.append(msg.orientation_rate.y)
                self.filter_state_dr.orientation_rate_z.append(msg.orientation_rate.z)
                self.filter_state_dr.orientation_variance_x.append(msg.orientation_variance.x)
                self.filter_state_dr.orientation_variance_y.append(msg.orientation_variance.y)
                self.filter_state_dr.orientation_variance_z.append(msg.orientation_variance.z)
                self.filter_state_dr.origin_altitude.append(msg.origin.altitude)
                self.filter_state_dr.origin_latitude.append(msg.origin.latitude)
                self.filter_state_dr.origin_longitude.append(msg.origin.longitude)
                self.filter_state_dr.position_depth.append(msg.position.depth)
                self.filter_state_dr.position_east.append(msg.position.east)
                self.filter_state_dr.position_north.append(msg.position.north)
                self.filter_state_dr.position_variance_depth.append(msg.position_variance.depth)
                self.filter_state_dr.position_variance_east.append(msg.position_variance.east)
                self.filter_state_dr.position_variance_north.append(msg.position_variance.north)
                self.filter_state_dr.seafloor_velocity_x.append(msg.seafloor_velocity.x)
                self.filter_state_dr.seafloor_velocity_y.append(msg.seafloor_velocity.y)
                self.filter_state_dr.seafloor_velocity_z.append(msg.seafloor_velocity.z)
                self.filter_state_dr.status.append(msg.status)
                self.filter_state_dr.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec()))) 

        # # Read filter_state_usbl
        self.filter_state_usbl = NavigationStatus()
        if filter_state_usbl:
            for topic, msg, t in filter_state_usbl:
                self.filter_state_usbl.altitude.append(msg.altitude)
                self.filter_state_usbl.body_velocity_x.append(msg.body_velocity.x)
                self.filter_state_usbl.body_velocity_y.append(msg.body_velocity.y)
                self.filter_state_usbl.global_position_altitude.append(msg.global_position.altitude)
                self.filter_state_usbl.global_position_latitude.append(msg.global_position.latitude)
                self.filter_state_usbl.orientation_x.append(msg.orientation.x)
                self.filter_state_usbl.orientation_y.append(msg.orientation.y)
                self.filter_state_usbl.orientation_z.append(msg.orientation.z)
                self.filter_state_usbl.orientation_rate_x.append(msg.orientation_rate.x)
                self.filter_state_usbl.orientation_rate_y.append(msg.orientation_rate.y)
                self.filter_state_usbl.orientation_rate_z.append(msg.orientation_rate.z)
                self.filter_state_usbl.orientation_variance_x.append(msg.orientation_variance.x)
                self.filter_state_usbl.orientation_variance_y.append(msg.orientation_variance.y)
                self.filter_state_usbl.orientation_variance_z.append(msg.orientation_variance.z)
                self.filter_state_usbl.origin_altitude.append(msg.origin.altitude)
                self.filter_state_usbl.origin_latitude.append(msg.origin.latitude)
                self.filter_state_usbl.origin_longitude.append(msg.origin.longitude)
                self.filter_state_usbl.position_depth.append(msg.position.depth)
                self.filter_state_usbl.position_east.append(msg.position.east)
                self.filter_state_usbl.position_north.append(msg.position.north)
                self.filter_state_usbl.position_variance_depth.append(msg.position_variance.depth)
                self.filter_state_usbl.position_variance_east.append(msg.position_variance.east)
                self.filter_state_usbl.position_variance_north.append(msg.position_variance.north)
                self.filter_state_usbl.seafloor_velocity_x.append(msg.seafloor_velocity.x)
                self.filter_state_usbl.seafloor_velocity_y.append(msg.seafloor_velocity.y)
                self.filter_state_usbl.seafloor_velocity_z.append(msg.seafloor_velocity.z)
                self.filter_state_usbl.status.append(msg.status)
                self.filter_state_usbl.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read State_usbl
        self.State_usbl = mState()
        if State_usbl:
            for topic, msg, t in State_usbl:
                self.State_usbl.X.append(msg.X)
                self.State_usbl.Y.append(msg.Y)
                self.State_usbl.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read State_gt
        self.State_gt = mState()
        if State_gt:
            for topic, msg, t in State_gt:
                self.State_gt.X.append(msg.X)
                self.State_gt.Y.append(msg.Y)
                self.State_gt.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read thrust_body_request
        self.thrust_body_request = BodyForceRequest()
        if thrust_body_request:
            for topic, msg, t in thrust_body_request:
                self.thrust_body_request.force_x.append(msg.wrench.force.x)
                self.thrust_body_request.force_y.append(msg.wrench.force.y)
                self.thrust_body_request.force_z.append(msg.wrench.force.z)
                self.thrust_body_request.torque_x.append(msg.wrench.torque.x)
                self.thrust_body_request.torque_y.append(msg.wrench.torque.y)
                self.thrust_body_request.torque_z.append(msg.wrench.torque.z)
                self.thrust_body_request.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read force_bypass
        self.force_bypass = BodyForceRequest()
        if force_bypass:
            for topic, msg, t in force_bypass:
                self.force_bypass.force_x.append(msg.wrench.force.x)
                self.force_bypass.force_y.append(msg.wrench.force.y)
                self.force_bypass.force_z.append(msg.wrench.force.z)
                self.force_bypass.torque_x.append(msg.wrench.torque.x)
                self.force_bypass.torque_y.append(msg.wrench.torque.y)
                self.force_bypass.torque_z.append(msg.wrench.torque.z)
                self.force_bypass.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read pathData
        self.pathData = PathData()
        if pathData:
            for topic, msg, t in pathData:
                #print(msg)
                self.pathData.curvature.append(msg.curvature)
                #print('curvature')
                self.pathData.d_pd.append(msg.d_pd)
                #print('d_pd')
                self.pathData.d_vd.append(msg.d_vd)
                #print('d_vd')
                self.pathData.dd_pd.append(msg.dd_pd)
                #print('dd_pd')
                self.pathData.derivative_norm.append(msg.derivative_norm)
                #print('derivative_norm')
                self.pathData.gamma.append(msg.gamma)
                #print('gamma')
                self.pathData.gamma_max.append(msg.gamma_max)
                #print('gamma_max')
                self.pathData.gamma_min.append(msg.gamma_min)
                #print('gamma_min')
                self.pathData.pd.append(msg.pd)
                #print('pd')
                self.pathData.tangent.append(msg.tangent)
                #print('tangent')
                self.pathData.vd.append(msg.vd)
                #print('vd')
                self.pathData.vehicle_speed.append(msg.vehicle_speed)
                #print('vshicle_speed')
                self.pathData.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
                #print('time')

                #for index in range(0,len(pathData.pd[0])):
                #    self.pathData.error_x_stateVirtual_vec.append(self.pathData.pd[0][index] - self.pathData.pd[0][0])
                #    self.pathData.error_y_stateVirtual_vec.append(self.pathData.pd[1][index] - pathData.pd[1][0])
                #print('PASSOU AQUI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')   
                
        # Read pf_vc
        self.pf_vc = Int8()
        if pf_vc:
            for topic, msg, t in pf_vc:
                self.pf_vc.value.append(msg.data)
                self.pf_vc.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read pf_gamma
        self.pf_gamma = Int8()
        if pf_gamma:
            for topic, msg, t in pf_gamma:
                self.pf_gamma.value.append(msg.data)
                self.pf_gamma.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read pf_debug
        self.pf_debug = mPFollowingDebug()
        if pf_debug:
            for topic, msg, t in pf_debug:
                self.pf_debug.algorithm = msg.algorithm
                self.pf_debug.along_track_error.append(msg.along_track_error)
                self.pf_debug.cross_track_error.append(msg.cross_track_error)
                self.pf_debug.gamma.append(msg.gamma)
                self.pf_debug.psi.append(msg.psi)
                self.pf_debug.yaw.append(msg.yaw)
                self.pf_debug.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read internal_gamma
        self.internal_gamma = CPFGamma()
        if internal_gamma:
            for topic, msg, t in internal_gamma:
                self.internal_gamma.ID.append(msg.ID)
                self.internal_gamma.gamma.append(msg.gamma)
                self.internal_gamma.vd.append(msg.vd)
                self.internal_gamma.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read internal_gamma
        self.external_gamma = CPFGamma()
        if external_gamma:
            for topic, msg, t in external_gamma:
                self.external_gamma.ID.append(msg.ID)
                self.external_gamma.gamma.append(msg.gamma)
                self.external_gamma.vd.append(msg.vd)
                self.external_gamma.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read acomms_filter_state
        self.acomms_filter_state = NavigationStatus()
        if acomms_filter_state:
            for topic, msg, t in acomms_filter_state:
                self.acomms_filter_state.altitude.append(msg.altitude)
                self.acomms_filter_state.body_velocity_x.append(msg.body_velocity.x)
                self.acomms_filter_state.body_velocity_y.append(msg.body_velocity.y)
                self.acomms_filter_state.global_position_altitude.append(msg.global_position.altitude)
                self.acomms_filter_state.global_position_latitude.append(msg.global_position.latitude)
                self.acomms_filter_state.orientation_x.append(msg.orientation.x)
                self.acomms_filter_state.orientation_y.append(msg.orientation.y)
                self.acomms_filter_state.orientation_z.append(msg.orientation.z)
                self.acomms_filter_state.orientation_rate_x.append(msg.orientation_rate.x)
                self.acomms_filter_state.orientation_rate_y.append(msg.orientation_rate.y)
                self.acomms_filter_state.orientation_rate_z.append(msg.orientation_rate.z)
                self.acomms_filter_state.orientation_variance_x.append(msg.orientation_variance.x)
                self.acomms_filter_state.orientation_variance_y.append(msg.orientation_variance.y)
                self.acomms_filter_state.orientation_variance_z.append(msg.orientation_variance.z)
                self.acomms_filter_state.origin_altitude.append(msg.origin.altitude)
                self.acomms_filter_state.origin_latitude.append(msg.origin.latitude)
                self.acomms_filter_state.origin_longitude.append(msg.origin.longitude)
                self.acomms_filter_state.position_depth.append(msg.position.depth)
                self.acomms_filter_state.position_east.append(msg.position.east)
                self.acomms_filter_state.position_north.append(msg.position.north)
                self.acomms_filter_state.position_variance_depth.append(msg.position_variance.depth)
                self.acomms_filter_state.position_variance_east.append(msg.position_variance.east)
                self.acomms_filter_state.position_variance_north.append(msg.position_variance.north)
                self.acomms_filter_state.seafloor_velocity_x.append(msg.seafloor_velocity.x)
                self.acomms_filter_state.seafloor_velocity_y.append(msg.seafloor_velocity.y)
                self.acomms_filter_state.seafloor_velocity_z.append(msg.seafloor_velocity.z)
                self.acomms_filter_state.status.append(msg.status)
                self.acomms_filter_state.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read acomms_usbl_fix 
        self.acomms_usbl_fix = mUSBLFix()
        if acomms_usbl_fix:
            for topic, msg, t in acomms_usbl_fix:
                self.acomms_usbl_fix.bearing.append(msg.bearing)
                self.acomms_usbl_fix.bearing_raw.append(msg.bearing_raw)
                self.acomms_usbl_fix.elevation.append(msg.elevation)
                self.acomms_usbl_fix.elevation_raw.append(msg.elevation_raw)
                self.acomms_usbl_fix.range.append(msg.range)
                self.acomms_usbl_fix.relative_position.append(msg.relative_position)
                self.acomms_usbl_fix.sound_speed.append(msg.sound_speed)
                self.acomms_usbl_fix.type.append(msg.type)
                self.acomms_usbl_fix.source_id.append(msg.source_id)
                self.acomms_usbl_fix.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read acomms_gnss
        self.acomms_gnss = NavigationStatus()
        if acomms_gnss:
            for topic, msg, t in acomms_gnss:
                self.acomms_gnss.altitude.append(msg.altitude)
                self.acomms_gnss.body_velocity_x.append(msg.body_velocity.x)
                self.acomms_gnss.body_velocity_y.append(msg.body_velocity.y)
                self.acomms_gnss.global_position_altitude.append(msg.global_position.altitude)
                self.acomms_gnss.global_position_latitude.append(msg.global_position.latitude)
                self.acomms_gnss.orientation_x.append(msg.orientation.x)
                self.acomms_gnss.orientation_y.append(msg.orientation.y)
                self.acomms_gnss.orientation_z.append(msg.orientation.z)
                self.acomms_gnss.orientation_rate_x.append(msg.orientation_rate.x)
                self.acomms_gnss.orientation_rate_y.append(msg.orientation_rate.y)
                self.acomms_gnss.orientation_rate_z.append(msg.orientation_rate.z)
                self.acomms_gnss.orientation_variance_x.append(msg.orientation_variance.x)
                self.acomms_gnss.orientation_variance_y.append(msg.orientation_variance.y)
                self.acomms_gnss.orientation_variance_z.append(msg.orientation_variance.z)
                self.acomms_gnss.origin_altitude.append(msg.origin.altitude)
                self.acomms_gnss.origin_latitude.append(msg.origin.latitude)
                self.acomms_gnss.origin_longitude.append(msg.origin.longitude)
                self.acomms_gnss.position_depth.append(msg.position.depth)
                self.acomms_gnss.position_east.append(msg.position.east)
                self.acomms_gnss.position_north.append(msg.position.north)
                self.acomms_gnss.position_variance_depth.append(msg.position_variance.depth)
                self.acomms_gnss.position_variance_east.append(msg.position_variance.east)
                self.acomms_gnss.position_variance_north.append(msg.position_variance.north)
                self.acomms_gnss.seafloor_velocity_x.append(msg.seafloor_velocity.x)
                self.acomms_gnss.seafloor_velocity_y.append(msg.seafloor_velocity.y)
                self.acomms_gnss.seafloor_velocity_z.append(msg.seafloor_velocity.z)
                self.acomms_gnss.status.append(msg.status)
                self.acomms_gnss.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        # Read acommsModemSend
        self.acommsModemSend = DMACPayload()
        if acommsModemSend:
            for topic, msg, t in acommsModemSend:
                self.acommsModemSend.msg_id.append(msg.msg_id)
                self.acommsModemSend.source_address.append(msg.source_address)
                self.acommsModemSend.destination_address.append(msg.destination_address)
                self.acommsModemSend.type.append(msg.type)
                self.acommsModemSend.ack.append(msg.ack)
                self.acommsModemSend.force.append(msg.force)
                self.acommsModemSend.bitrate.append(msg.bitrate)
                self.acommsModemSend.rssi.append(msg.rssi)
                self.acommsModemSend.integrity.append(msg.integrity)
                self.acommsModemSend.propagation_time.append(msg.propagation_time)
                self.acommsModemSend.duration.append(msg.duration)
                self.acommsModemSend.timestamp.append(msg.timestamp)
                self.acommsModemSend.timestamp_undefined.append(msg.timestamp_undefined)
                self.acommsModemSend.relative_velocity.append(msg.relative_velocity)
                self.acommsModemSend.payload.append(msg.payload)
                self.acommsModemSend.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        # Read acommsModemRecv
        self.acommsModemRecv = DMACPayload()
        if acommsModemRecv:
            for topic, msg, t in acommsModemRecv:
                self.acommsModemRecv.msg_id.append(msg.msg_id)
                self.acommsModemRecv.source_address.append(msg.source_address)
                self.acommsModemRecv.destination_address.append(msg.destination_address)
                self.acommsModemRecv.type.append(msg.type)
                self.acommsModemRecv.ack.append(msg.ack)
                self.acommsModemRecv.force.append(msg.force)
                self.acommsModemRecv.bitrate.append(msg.bitrate)
                self.acommsModemRecv.rssi.append(msg.rssi)
                self.acommsModemRecv.integrity.append(msg.integrity)
                self.acommsModemRecv.propagation_time.append(msg.propagation_time)
                self.acommsModemRecv.duration.append(msg.duration)
                self.acommsModemRecv.timestamp.append(msg.timestamp)
                self.acommsModemRecv.timestamp_undefined.append(msg.timestamp_undefined)
                self.acommsModemRecv.relative_velocity.append(msg.relative_velocity)
                self.acommsModemRecv.payload.append(msg.payload)
                self.acommsModemRecv.time.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

    # Getters
    def getFlag(self):
        return self.flag
        
    def getRefSurge(self):
        return self.ref_surge

    def getRefSway(self):
        return self.ref_sway
    
    def getRefHeave(self):
        return self.ref_heave

    def getRefYawRate(self):
        return self.ref_yaw_rate

    def getRefYaw(self):
        return self.ref_yaw

    def getRefDepth(self):
        return self.ref_depth

    def getRefAltitude(self):
        return self.ref_altitude

    def getRefPitch(self):
        return self.ref_pitch

    def getRefRoll(self):
        return self.ref_roll

    def getRefPitchRate(self):
        return self.ref_pitch_rate

    def getRefRollRate(self):
        return self.ref_roll_rate

    def getRefAltitudeSafety(self):
        return self.ref_altitude_safety

    def getRefDepthSafety(self):
        return self.ref_depth_safety

    def getRPMCommand(self):
        return self.rpm_command

    def getUsblFix(self):
        return self.usbl_fix
    
    def getFilterState(self):
        return self.filter_state

    def getFilterCurrents(self):
        return self.filter_currents

    def getFilterStateDR(self):
        return self.filter_state_dr

    def getFilterStateUSBL(self):
        return self.filter_state_usbl

    def getStateGT(self):
        return self.State_gt

    def getStateUSBL(self):
        return self.State_usbl

    def getThrustBodyRequest(self):
        return self.thrust_body_request

    def getForceBypass(self):
        return self.force_bypass

    def getPathData(self):
        return self.pathData

    def getPFvc(self):
        return self.pf_vc

    def getPFGamma(self):
        return self.pf_gamma

    def getPFDebug(self):
        return self.pf_debug

    def getInternalGamma(self):
        return self.internal_gamma

    def getExternalGamma(self):
        return self.external_gamma

    def getAcommsFilterState(self):
        return self.acomms_filter_state

    def getAcommsUSBLFix(self):
        return self.acomms_usbl_fix

    def getAcommsGNSS(self):
        return self.acomms_gnss

    def getAcommsModemRecv(self):
        return self.getAcommsModemRecv

    def getAcommsModemSend(self):
        return self.getAcommsModemSend


