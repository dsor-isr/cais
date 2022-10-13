import rosbag
import os
import time
import math
import plotly.graph_objs as go
import plotly.offline as py
from handyTools import *
from datetime import datetime

"""
Class responsable for create all plots with respect to the Missions
"""
class Missions(object):
    def __init__(self, datafolder):
        self.datafolder = datafolder
        self.missions = []
        self.flag_value_vec = []
        self.flag_time_vec = []
    
    def divideBagsPerMission(self, bag, flag_topic, pattern):
        """
        Divide the .bag into a small mission bag according the choosen pattern
        The output bag have a especific name
        """
        self.createFlagTopicVec(flag_topic)
        # self.createMissionsVec(flag_topic, pattern)
        self.createMissionsVec2(flag_topic, pattern)

        # if there is no missions in the entire bag
        if not self.missions:
            return

        # create the missions folder
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        j = 1
        outbag = rosbag.Bag(self.datafolder + "/%d_mission.bag" % j, 'w')

        for topic, msg, t in bag.read_messages():
            if t >= self.missions[j-1][0]:
                outbag.write(topic, msg, t)
            if t == self.missions[j-1][1]:
                outbag.close()
                if j < len(self.missions):
                    j+=1
                    outbag = rosbag.Bag(self.datafolder + "/%d_mission.bag" % j, 'w')
                else:
                    return

    def createFlagTopicVec(self, flag_topic):
        """
        Get messages from Flag topic
        """
        self.flag_value_vec = []
        self.flag_time_vec = []
        
        for topic, msg, t in flag_topic:
            self.flag_value_vec.append(msg.data)
            self.flag_time_vec.append(t)

    def createMissionsVec(self, flag_topic, pattern):
        """
        Find in the Flag messages the pattern for the mission, ang save the start time and end time of the mission
        """
        self.missions = []

        for i in range(0, len(self.flag_value_vec)):
            if self.flag_value_vec[i] == pattern[0] and self.flag_value_vec[i:i+len(pattern)] == pattern:
                if (i < len(self.flag_value_vec)) and (i+len(pattern) <= len(self.flag_value_vec)):
                    self.missions.append([self.flag_time_vec[i+1], self.flag_time_vec[i+len(pattern)-1]])
    
    def createMissionsVec2(self, flag_topic, pattern):
        """
        Find in the Flag messages the pattern for the mission, ang save the start time and end time of the mission
        """
        self.missions = []

        for i in range(0, len(self.flag_value_vec)):
            if self.flag_value_vec[i] == 6 and self.flag_value_vec[i+1] == 4: 
                self.missions.append([self.flag_time_vec[i], self.flag_time_vec[i+1]])
     
    def makePlots(self, bag):
        """
        Call the methods to make the analise o the mission
        """
        # read all messages from the topics
        self.readMessages(bag)

        # Plot Mission Overview: ground truth, filter and dead reckoning in UTM
        self.poseGTposeDRposeFilter()

        # Plot Filter and the Virtual Target in UTM
        self.poseFilterposeVirtual()

        # Plot Filter, Virtual Target and Ground Truth in UTM
        self.poseFilterposeVirtualposeGT()

        # Plot Along and Cross Track Error
        self.crossTrackAlongTrack()

        # Plot the Inercial Velocity of the Currents
        self.InertialCurrents()

        # Plot Sway state vs Sway Reference
        self.swayRef()
        
        # Plot Surge state vs Surge Reference
        self.surgeRef()

        # Plot Yaw state vs Yaw Reference
        self.yawRef()
        
        # Plot Yaw Rate state vs Yaw Rate Reference
        self.yawRateRef()
        
        # Plot Depth state vs Depth Reference
        self.depthRef()

        # Plot Altitude state vs Altitude Reference
        self.altitudeRef()

        # Plot Dead Reckoning x velocity vs Filter x velocity
        self.vxDRvxFilter()
        
        # Plot Dead Reckoning y velocity vs Filter y velocity
        self.vyDRvyFilter()
        
        # Plot Error in Mission Overview: ground truth, filter and dead reckoning
        self.error_poseGTposeDRposeFilter()
        
        # Plot Error between Filter and the Virtual Target
        self.error_poseFilterposeVirtual()
        
        # Plot the rms between dead reckoning and ground truth and also between Filter and Ground Truth
        self.rms_gtFilterDr()

        self.usbl_rate()

    def readMessages(self, bag):
        self.state_topic = []
        self.usbl_est_topic = []
        self.dr_topic = []
        self.gt_topic = []
        self.pathData_topic = []
        self.pathFollowingDebug_topic = []
        self.innerLoopForces_topic = []
        self.ref_sway_topic = []
        self.ref_surge_topic = []
        self.ref_yaw_topic = []
        self.ref_yaw_rate_topic = []
        self.ref_depth_topic = []
        self.ref_altitude_topic = []
        self.currents_topic = []

        if searchInTopics(bag, '/nav/filter/state'):
            vehicle_name = ''
            if searchInTopics(bag, '/nav/filter/state')[0].find('mblack0') != -1: vehicle_name = '/mblack0'
            elif searchInTopics(bag, '/nav/filter/state')[0].find('mred0') != -1: vehicle_name = '/mred0'
            elif searchInTopics(bag, '/nav/filter/state')[0].find('mvector0') != -1: vehicle_name = '/mvector0'
            self.state_topic = vehicle_name + '/nav/filter/state'

        if searchInTopics(bag, '/State_usbl_est'):
            self.usbl_est_topic = searchInTopics(bag, '/State_usbl_est')[0]
            # print("\nState_USBL: " + self.usbl_est_topic)


        if searchInTopics(bag, '/nav/filter/state_dr'):
            self.dr_topic = searchInTopics(bag, '/nav/filter/state_dr')[0]
            # print("\nState_DR: " + self.dr_topic)


        if searchInTopics(bag, '/State_gt'):
            self.gt_topic = searchInTopics(bag, '/State_gt')[0]
            # print("\nState_gt: " + self.gt_topic)

        if searchInTopics(bag, '/PathData'):
            self.pathData_topic = searchInTopics(bag, '/PathData')[0]
            # print("\nPathData: " + self.pathData_topic)

        if searchInTopics(bag, '/pfollowing/debug'):
            self.pathFollowingDebug_topic = searchInTopics(bag, '/pfollowing/debug')[0]
            # print("\nPF_debug: " + self.pathFollowingDebug_topic)

        if searchInTopics(bag, '/controls/inner_loops_forces/thrust_body_request'):
            self.innerLoopForces_topic = searchInTopics(bag, '/controls/inner_loops_forces/thrust_body_request')[0]
            # print("\ninner_Force: " + self.inner_loops_forces)

        if searchInTopics(bag, '/ref/sway'):
            self.ref_sway_topic = searchInTopics(bag, '/ref/sway')[0]
            # print("\nref_sway: " + self.ref_sway_topic)
        
        if searchInTopics(bag, '/ref/surge'):
            self.ref_surge_topic = searchInTopics(bag, '/ref/surge')[0]
            # print("\nref_surge: " + self.ref_surge_topic)
        
        if searchInTopics(bag, '/ref/yaw'):
            self.ref_yaw_topic = searchInTopics(bag, '/ref/yaw')[0]
            # print("\nref_yaw: " + self.ref_yaw_topic)
        
        if searchInTopics(bag, '/ref/yaw_rate'):
            self.ref_yaw_rate_topic = searchInTopics(bag, '/ref/yaw_rate')[0]
            # print("\nref_yaw_rate: " + self.ref_yaw_rate_topic)
        
        if searchInTopics(bag, '/ref/depth'):
            self.ref_depth_topic = searchInTopics(bag, '/ref/depth')[0]
            # print("\nref_depth: " + self.ref_depth_topic)
        
        if searchInTopics(bag, '/ref/altitude'):
            self.ref_altitude_topic = searchInTopics(bag, '/ref/altitude')[0]
            # print("\nref_altitude: " + self.ref_altitude_topic)
        
        if searchInTopics(bag, '/nav/filter/currents'):
            self.currents_topic = searchInTopics(bag, '/nav/filter/currents')[0]
            # print("\ncurrents: " + self.currents_topic)

        
        self.x_state_vec = []
        self.y_state_vec = []
        self.error_x_state_vec = []
        self.error_y_state_vec = []
        self.vx_state_vec = []
        self.vy_state_vec = []
        self.sway_state_vec = []
        self.surge_state_vec = []
        self.yaw_state_vec = []
        self.yaw_rate_state_vec = []
        self.depth_state_vec = []
        self.altitude_state_vec = []
        self.time_state_topic = []
            
       
        if self.state_topic:
            for topic, msg, t in findTopic(bag, self.state_topic):
                self.x_state_vec.append(msg.position.north)
                self.y_state_vec.append(msg.position.east)
                self.vx_state_vec.append(msg.seafloor_velocity.x)
                self.vy_state_vec.append(msg.seafloor_velocity.y)
                self.sway_state_vec.append(msg.body_velocity.y)
                self.surge_state_vec.append(msg.body_velocity.x)
                self.yaw_state_vec.append(wrapTo360(msg.orientation.z))
                self.yaw_rate_state_vec.append(msg.orientation_rate.z)
                self.depth_state_vec.append(msg.position.depth)
                self.altitude_state_vec.append(msg.global_position.altitude)
                # self.time_state_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_state_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

            for index in range(0, len(self.x_state_vec)): 
                self.error_x_state_vec.append(self.x_state_vec[index] - self.x_state_vec[0])
                self.error_y_state_vec.append(self.y_state_vec[index] - self.y_state_vec[0])

        self.x_usbl_vec = []
        self.y_usbl_vec = []
        self.time_usbl_topic = []
        self.time_sec_usbl_topic = []
       
        if self.usbl_est_topic:
            for topic, msg, t in findTopic(bag, self.usbl_est_topic):
                self.x_usbl_vec.append(msg.Y)
                self.y_usbl_vec.append(msg.X)
                self.time_sec_usbl_topic.append(t.to_sec())
                self.time_usbl_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
           
        self.x_dr_vec = []
        self.y_dr_vec = []
        self.error_x_dr_vec = []
        self.error_y_dr_vec = []
        self.vx_dr_vec = []
        self.vy_dr_vec = []
        self.time_dr_topic = []
       
        if self.dr_topic:
            for topic, msg, t in findTopic(bag, self.dr_topic):
                self.x_dr_vec.append(msg.position.north)
                self.y_dr_vec.append(msg.position.east)
                self.vx_dr_vec.append(msg.seafloor_velocity.x)
                self.vy_dr_vec.append(msg.seafloor_velocity.y)
                # self.time_dr_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_dr_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
           
            for index in range(0, len(self.x_dr_vec)): 
                self.error_x_dr_vec.append(self.x_dr_vec[index] - self.x_dr_vec[0])
                self.error_y_dr_vec.append(self.y_dr_vec[index] - self.y_dr_vec[0])

        self.x_gt_vec = []
        self.y_gt_vec = []
        self.error_x_gt_vec = []
        self.error_y_gt_vec = []
        self.time_gt_topic = []
        
        if self.gt_topic:
            for topic, msg, t in findTopic(bag, self.gt_topic):
                self.x_gt_vec.append(msg.Y)
                self.y_gt_vec.append(msg.X)
                # self.time_gt_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_gt_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
            
            for index in range(0, len(self.x_gt_vec)): 
                self.error_x_gt_vec.append(self.x_gt_vec[index] - self.x_gt_vec[0])
                self.error_y_gt_vec.append(self.y_gt_vec[index] - self.y_gt_vec[0])
        
        self.x_stateVirtual_vec = []
        self.y_stateVirtual_vec = []
        self.error_x_stateVirtual_vec = []
        self.error_y_stateVirtual_vec = []
        self.vd_vec = []
        
        if self.pathData_topic:
            for topic, msg, t in findTopic(bag, self.pathData_topic):
                self.x_stateVirtual_vec.append(msg.pd[0])
                self.y_stateVirtual_vec.append(msg.pd[1])
                self.vd_vec.append(msg.vd)
            
            for index in range(0, len(self.x_stateVirtual_vec)): 
                self.error_x_stateVirtual_vec.append(self.x_stateVirtual_vec[index] - self.x_stateVirtual_vec[0])
                self.error_y_stateVirtual_vec.append(self.y_stateVirtual_vec[index] - self.y_stateVirtual_vec[0])

        self.crossTrackError_vec = []
        self.alongTrackError_vec = []
        self.time_pathFollowingDebug_topic = []
        self.pathfollowingAlgorithm = []

        if self.pathFollowingDebug_topic:
            for topic, msg, t in findTopic(bag, self.pathFollowingDebug_topic):
                self.crossTrackError_vec.append(msg.cross_track_error)
                self.alongTrackError_vec.append(msg.along_track_error)
                self.pathfollowingAlgorithm = msg.algorithm
                # self.time_pathFollowingDebug_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_pathFollowingDebug_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.x_force_vec = []
        self.y_force_vec = []
        self.time_innerLoopForces_topic = []

        if self.innerLoopForces_topic:
            for topic, msg, t in findTopic(bag, self.innerLoopForces_topic):
                self.x_force_vec.append(msg.wrench.force.x)
                self.y_force_vec.append(msg.wrench.force.y)
                # self.time_innerLoopForces_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_innerLoopForces_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
        
        self.ref_sway_vec = []
        self.time_ref_sway_topic = []

        if self.ref_sway_topic:
            for topic, msg, t in findTopic(bag, self.ref_sway_topic):
                self.ref_sway_vec.append(msg.data)
                # self.time_ref_sway_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_sway_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
    
        self.ref_surge_vec = []
        self.time_ref_surge_topic = []

        if self.ref_surge_topic:
            for topic, msg, t in findTopic(bag, self.ref_surge_topic):
                self.ref_surge_vec.append(msg.data)
                # self.time_ref_surge_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_surge_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.ref_yaw_vec = []
        self.time_ref_yaw_topic = []

        if self.ref_yaw_topic:
            for topic, msg, t in findTopic(bag, self.ref_yaw_topic):
                self.ref_yaw_vec.append(wrapTo360(msg.data))
                # self.time_ref_yaw_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_yaw_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.ref_yaw_rate_vec = []
        self.time_ref_yaw_rate_topic = []

        if self.ref_yaw_rate_topic:
            for topic, msg, t in findTopic(bag, self.ref_yaw_rate_topic):
                self.ref_yaw_rate_vec.append(msg.data)
                # self.time_ref_yaw_rate_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_yaw_rate_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.ref_depth_vec = []
        self.time_ref_depth_topic = []

        if self.ref_depth_topic:
            for topic, msg, t in findTopic(bag, self.ref_depth_topic):
                self.ref_depth_vec.append(msg.data)
                # self.time_ref_depth_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_depth_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.ref_altitude_vec = []
        self.time_ref_altitude_topic = []

        if self.ref_altitude_vec:
            for topic, msg, t in findTopic(bag, self.ref_altitude_topic):
                self.ref_altitude_vec.append(msg.data)
                # self.time_ref_altitude_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_ref_altitude_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))

        self.vx_current_vec = []
        self.vy_current_vec = []
        self.time_current_topic = []

        if self.currents_topic:
            for topic, msg, t in findTopic(bag, self.currents_topic):
                self.vx_current_vec.append(msg.x_current)
                self.vy_current_vec.append(msg.y_current)
                # self.time_current_topic.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                self.time_current_topic.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
            
    def poseGTposeDRposeFilter(self):

        if not self.state_topic and not self.dr_topic and not self.gt_topic:
            return

        if self.state_topic and self.dr_topic and self.gt_topic and self.usbl_est_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.y_dr_vec, y=self.x_dr_vec, mode='lines', name='DR')
            gt_data = go.Scatter(x=self.y_gt_vec, y=self.x_gt_vec, mode='lines', name='GT')
            usbl_data = go.Scatter(x=self.y_usbl_vec, y=self.x_usbl_vec, mode='lines+markers', name='USBL estimation')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data, gt_data, usbl_data], layout=layout)

        elif self.state_topic and self.dr_topic and self.gt_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.y_dr_vec, y=self.x_dr_vec, mode='lines', name='DR')
            gt_data = go.Scatter(x=self.y_gt_vec, y=self.x_gt_vec, mode='lines', name='GT')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data, gt_data], layout=layout)

        elif self.state_topic and self.dr_topic and self.usbl_est_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.y_dr_vec, y=self.x_dr_vec, mode='lines', name='DR')
            usbl_data = go.Scatter(x=self.y_usbl_vec, y=self.x_usbl_vec, mode='lines+markers', name='USBL estimation')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data, usbl_data], layout=layout)

        elif self.state_topic and self.dr_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.y_dr_vec, y=self.x_dr_vec, mode='lines', name='DR')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data], layout=layout)

        elif self.state_topic and self.usbl_est_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            usbl_data = go.Scatter(x=self.y_usbl_vec, y=self.x_usbl_vec, mode='lines+markers', name='Underwater vehicle estimation by the vehicle surface using USBL')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, usbl_data], layout=layout)

        elif self.state_topic and self.gt_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            gt_data = go.Scatter(x=self.y_gt_vec, y=self.x_gt_vec, mode='lines', name='GT')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, gt_data], layout=layout)

        elif self.state_topic:
            # Plot path
            state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
            layout = dict(title = 'Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig_data, filename=self.datafolder + '/MissionOverview.html', auto_open=False)

    def error_poseGTposeDRposeFilter(self):

        if not self.state_topic and not self.dr_topic and not self.gt_topic:
            return

        if self.state_topic and self.dr_topic and self.gt_topic:
            # Plot path
            state_data = go.Scatter(x=self.error_y_state_vec, y=self.error_x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.error_y_dr_vec, y=self.error_x_dr_vec, mode='lines', name='DR')
            gt_data = go.Scatter(x=self.error_y_gt_vec, y=self.error_x_gt_vec, mode='lines', name='GT')
            layout = dict(title = 'Error in Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Error in Easting [m]'), yaxis=dict(title='Error in Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data, gt_data], layout=layout)

        elif self.state_topic and self.dr_topic:
            # Plot path
            state_data = go.Scatter(x=self.error_y_state_vec, y=self.error_x_state_vec, mode='lines', name='filter')
            dr_data = go.Scatter(x=self.error_y_dr_vec, y=self.error_x_dr_vec, mode='lines', name='DR')
            layout = dict(title = 'Error in Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Error in Easting [m]'), yaxis=dict(title='Error in Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data, dr_data], layout=layout)

        elif self.state_topic:
            # Plot path
            state_data = go.Scatter(x=self.error_y_state_vec, y=self.error_x_state_vec, mode='lines', name='filter')
            layout = dict(title = 'Error Mission Overview with ' + self.pathfollowingAlgorithm, xaxis=dict(title='Error in Easting [m]'), yaxis=dict(title='Error in Northing [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[state_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig_data, filename=self.datafolder + '/ErrorInMissionOverview.html', auto_open=False)

    def poseFilterposeVirtual(self):

        if not self.state_topic or not self.pathData_topic:
            return
        
        # Plot path
        state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
        stateVirtual_data = go.Scatter(x=self.y_stateVirtual_vec, y=self.x_stateVirtual_vec, mode='lines', name='Virtual_Target')
        layout = dict(title = 'Filter vs Virtual Target', xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, stateVirtual_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Filter_vs_Virtual.html', auto_open=False)
    
    def error_poseFilterposeVirtual(self):

        if not self.state_topic or not self.pathData_topic:
            return

        error_x_filter_vec = []
        error_y_filter_vec = []

        for index in range(0, len(self.x_state_vec)): 
            error_x_filter_vec.append(self.x_state_vec[index] - self.x_stateVirtual_vec[0])
            error_y_filter_vec.append(self.y_state_vec[index] - self.y_stateVirtual_vec[0])
        
        # Plot path
        state_data = go.Scatter(x=error_y_filter_vec, y=error_x_filter_vec, mode='lines', name='filter')
        stateVirtual_data = go.Scatter(x=self.error_y_stateVirtual_vec, y=self.error_x_stateVirtual_vec, mode='lines', name='Virtual_Target')
        layout = dict(title = 'Error between Filter and Virtual Target', xaxis=dict(title='Error in Easting [m]'), yaxis=dict(title='Error in Northing [m]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, stateVirtual_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Error_between_Filter_and_VirtualTarget.html', auto_open=False)

    def poseFilterposeVirtualposeGT(self):

        if not self.state_topic or not self.pathData_topic or not self.gt_topic:
            return

        # Plot path
        state_data = go.Scatter(x=self.y_state_vec, y=self.x_state_vec, mode='lines', name='filter')
        stateVirtual_data = go.Scatter(x=self.y_stateVirtual_vec, y=self.x_stateVirtual_vec, mode='lines', name='Virtual_Target')
        gt_data = go.Scatter(x=self.y_gt_vec, y=self.x_gt_vec, mode='lines', name='GT')
        layout = dict(title = 'Filter vs Virtual_Target vs GT', xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, stateVirtual_data, gt_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Filter_and_VirtualTarget_and_GT.html', auto_open=False)

    def crossTrackAlongTrack(self):
        
        if not self.crossTrackError_vec or not self.alongTrackError_vec:
            return

        # Plot path
        cross_data = go.Scatter(x=self.time_pathFollowingDebug_topic, y=self.crossTrackError_vec, mode='lines', name='cross_track_error')
        along_data = go.Scatter(x=self.time_pathFollowingDebug_topic, y=self.alongTrackError_vec, mode='lines', name='along_track_error')
        layout = dict(title = 'Along and Cross Track errors', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Error [m]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[cross_data, along_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Cross_and_Along_errors.html', auto_open=False)


    def InertialCurrents(self):

        if not self.vx_current_vec or not self.vy_current_vec:
            return

        # Plot path
        xcurrent_data = go.Scatter(x=self.time_current_topic, y=self.vx_current_vec, mode='lines', name='Vx Current')
        ycurrent_data = go.Scatter(x=self.time_current_topic, y=self.vy_current_vec, mode='lines', name='Vy Current')
        layout = dict(title = 'Inertial Velocity of Current', xaxis=dict(title='time', nticks=50), yaxis=dict(title='current [m/s]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[xcurrent_data, ycurrent_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Inertial_Current.html', auto_open=False)
     
    def swayRef(self):
        
        if not self.sway_state_vec or not self.ref_sway_vec:
            return

        # Plot path
        sway_state_data = go.Scatter(x=self.time_state_topic, y=self.sway_state_vec, mode='lines', name='sway from state')
        sway_ref_data = go.Scatter(x=self.time_ref_sway_topic, y=self.ref_sway_vec, mode='lines', name='ref sway')
        layout = dict(title = 'Ref sway vs real sway', xaxis=dict(title='time', nticks=50), yaxis=dict(title='sway [m/s]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[sway_state_data, sway_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Sway.html', auto_open=False)

    def surgeRef(self):
        
        if not self.surge_state_vec or not self.ref_surge_vec:
            return

        # Plot path
        surge_state_data = go.Scatter(x=self.time_state_topic, y=self.surge_state_vec, mode='lines', name='surge from state')
        surge_ref_data = go.Scatter(x=self.time_ref_surge_topic, y=self.ref_surge_vec, mode='lines', name='ref surge')
        layout = dict(title = 'Ref surge vs real surge', xaxis=dict(title='time', nticks=50), yaxis=dict(title='surge [m/s]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[surge_state_data, surge_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Surge.html', auto_open=False)

    def yawRef(self):
        
        if not self.yaw_state_vec or not self.ref_yaw_vec:
            return

        # Plot path
        yaw_state_data = go.Scatter(x=self.time_state_topic, y=self.yaw_state_vec, mode='lines', name='yaw from state')
        yaw_ref_data = go.Scatter(x=self.time_ref_yaw_topic, y=self.ref_yaw_vec, mode='lines', name='ref yaw')
        layout = dict(title = 'Ref yaw vs real yaw', xaxis=dict(title='time', nticks=50), yaxis=dict(title='yaw', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[yaw_state_data, yaw_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Yaw.html', auto_open=False)

    def yawRateRef(self):
        
        if not self.yaw_rate_state_vec or not self.ref_yaw_rate_vec:
            return

        # Plot path
        yaw_rate_state_data = go.Scatter(x=self.time_state_topic, y=self.yaw_rate_state_vec, mode='lines', name='yaw_rate from state')
        yaw_rate_ref_data = go.Scatter(x=self.time_ref_yaw_rate_topic, y=self.ref_yaw_rate_vec, mode='lines', name='ref yaw_rate')
        layout = dict(title = 'Ref yaw_rate vs real yaw_rate', xaxis=dict(title='time', nticks=50), yaxis=dict(title='yaw_rate', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[yaw_rate_state_data, yaw_rate_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Yaw_Rate.html', auto_open=False)

    def depthRef(self):
        
        if not self.depth_state_vec or not self.ref_depth_vec:
            return

        # Plot path
        depth_state_data = go.Scatter(x=self.time_state_topic, y=self.depth_state_vec, mode='lines', name='depth from state')
        depth_ref_data = go.Scatter(x=self.time_ref_depth_topic, y=self.ref_depth_vec, mode='lines', name='ref depth')
        layout = dict(title = 'Ref depth vs real depth', xaxis=dict(title='time', nticks=50), yaxis=dict(title='depth', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[depth_state_data, depth_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Depth.html', auto_open=False)

    def altitudeRef(self):
        
        if not self.altitude_state_vec or not self.ref_altitude_vec:
            return

        # Plot path
        altitude_state_data = go.Scatter(x=self.time_state_topic, y=self.altitude_state_vec, mode='lines', name='altitude from state')
        altitude_ref_data = go.Scatter(x=self.time_ref_altitude_topic, y=self.ref_altitude_vec, mode='lines', name='ref altitude')
        layout = dict(title = 'Ref altitude vs real altitude', xaxis=dict(title='time', nticks=50), yaxis=dict(title='altitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[altitude_state_data, altitude_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Altitude.html', auto_open=False)

    def vxDRvxFilter(self):
        
        if not self.vx_dr_vec or not self.vx_state_vec:
            return

        # Plot path
        vx_state_data = go.Scatter(x=self.time_state_topic, y=self.vx_state_vec, mode='lines', name='Vx in state')
        vx_dr_data = go.Scatter(x=self.time_dr_topic, y=self.vx_dr_vec, mode='lines', name='Vx in DR')
        layout = dict(title = 'Vx in state vs Vx in DR', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Vx', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[vx_state_data, vx_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/vxState_vs_VxDR.html', auto_open=False)

    def vyDRvyFilter(self):
        
        if not self.vy_dr_vec or not self.vy_state_vec:
            return

        # Plot path
        vy_state_data = go.Scatter(x=self.time_state_topic, y=self.vy_state_vec, mode='lines', name='Vy in state')
        vy_dr_data = go.Scatter(x=self.time_dr_topic, y=self.vy_dr_vec, mode='lines', name='Vy in DR')
        layout = dict(title = 'Vy in state vs Vy in DR', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Vy', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[vy_state_data, vy_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/vyState_vs_VyDR.html', auto_open=False)

    def rms_gtFilterDr(self):
        
        if not self.state_topic and not self.dr_topic and not self.gt_topic:
            return
        
        rms_state = []
        rms_dr = []
        
        if not self.x_gt_vec or not self.y_gt_vec:
            return

        if self.x_state_vec and self.y_state_vec:
            rms_state = rms(self.x_gt_vec, self.y_gt_vec, self.x_state_vec, self.y_state_vec)
        
        if self.x_dr_vec and self.y_dr_vec:
            rms_dr = rms(self.x_gt_vec, self.y_gt_vec, self.x_dr_vec, self.y_dr_vec)
        
        if rms_state and rms_dr:
            # Plot path
            rms_state_data = go.Scatter(x=self.time_state_topic, y=rms_state, mode='lines', name='rms state')
            rms_dr_data = go.Scatter(x=self.time_state_topic, y=rms_dr, mode='lines', name='rms dr')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_state_data, rms_dr_data], layout=layout)

        elif rms_state:
            # Plot path
            rms_state_data = go.Scatter(x=self.time_state_topic, y=rms_state, mode='lines', name='rms state')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_state_data], layout=layout)

        elif rms_dr:
            # Plot path
            rms_state_data = go.Scatter(x=self.time_state_topic, y=rms_state, mode='lines', name='rms state')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/RMS.html', auto_open=False)


    def usbl_rate(self):

        if not self.state_topic or not self.usbl_est_topic:
            return
        
        delta_time_usbl_vec = []
        delta_x_usbl_vec = []
        delta_y_usbl_vec = []
        delta_error = []
        for index in range(0, len(self.x_usbl_vec)): 
            delta_x_usbl_vec.append(self.x_usbl_vec[index] - self.x_usbl_vec[0])
            delta_y_usbl_vec.append(self.y_usbl_vec[index] - self.y_usbl_vec[0])
            delta_error.append(math.sqrt(delta_y_usbl_vec[index]**2 + delta_x_usbl_vec[index]**2))
            delta_time_usbl_vec.append(self.time_sec_usbl_topic[index] - self.time_sec_usbl_topic[0])

        # Plot path
        error_data = go.Scatter(x=delta_time_usbl_vec, y=delta_error, mode='markers', name='X_delta_error_USBL', showlegend=True)
        # y_usbl_data = go.Scatter(x=delta_time_usbl_vec, y=delta_y_usbl_vec, mode='markers', name='Y_delta_error_USBL', showlegend=True)
        layout = dict(title = 'Acoustics rate and |ERROR|', xaxis=dict(title='Delta Time [s]'), yaxis=dict(title='|Error| [m]'))
        fig_data = dict(data=[error_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Acoustics_rate_and_absError.html', auto_open=False)

