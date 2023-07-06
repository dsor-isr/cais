import os
import plotly.graph_objs as go
import plotly.offline as py
from farol_topics import FarolStack
from datetime import datetime
from handyTools import rms
import math

class SoftwarePlots():
    def __init__(self, datafolder, farolStack):
        self.datafolder = datafolder
        self.farolStack = farolStack
        
        self.plotMissionOverview()
        self.error_poseGTposeDRposeFilter()
        self.plotFilterposeVirtual()
        self.error_plotFilterposeVirtual()
        self.plotFilterposeVirtualposeGT()
        self.crossTrackAlongTrack()
        self.InertialCurrents()
        self.swayRef()
        self.surgeRef()
        self.yawRef()
        self.yawRateRef()
        self.depthRef()
        self.altitudeRef()
        self.vxDRvxFilter()
        self.vyDRvyFilter()
        self.rms_gtFilterDr()
        self.usbl_rate()

    def plotMissionOverview(self):
        
        filterState = self.farolStack.getFilterState()
        filterStateDR = self.farolStack.getFilterStateDR()
        StateGT = self.farolStack.getStateGT()
        StateUSBL = self.farolStack.getStateUSBL()
        
        if not filterState and not filterStateDR and not StateGT:
            return
        
        elif filterState and filterStateDR and StateUSBL and StateGT:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            usbl_data = go.Scatter(x=StateUSBL.X, y=StateUSBL.Y, mode='lines', name='USBL estimation')
            gt_data = go.Scatter(x=StateGT.X, y=StateGT.Y, mode='lines', name='GT')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data, usbl_data, gt_data], layout=layout)
            
        elif filterState and filterStateDR and StateUSBL:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            usbl_data = go.Scatter(x=StateUSBL.X, y=StateUSBL.Y, mode='lines', name='USBL')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data, usbl_data], layout=layout)
       
        elif filterState and filterStateDR and StateGT:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            gt_data = go.Scatter(x=StateGT.Y, y=StateGT.X, mode='lines', name='GT')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data, gt_data], layout=layout) 

        elif filterState and filterStateDR:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data], layout=layout)

        elif filterState and StateGT:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            gt_data = go.Scatter(x=StateGT.Y, y=StateGT.X, mode='lines', name='GT')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, gt_data], layout=layout)
        
        elif filterState and StateUSBL:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            usbl_data = go.Scatter(x=StateUSBL.X, y=StateUSBL.Y, mode='lines+markers', name='Underwater vehicle estimation by the vehicle surface using USBL')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, usbl_data], layout=layout)
        
        elif filterState:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            layout = dict(title = 'Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Easting'), yaxis=dict(title='Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/MissionOverview.html', auto_open=False)

    def error_poseGTposeDRposeFilter(self):
        
        filterState = self.farolStack.getFilterState()
        filterStateDR = self.farolStack.getFilterStateDR()
        StateGT = self.farolStack.getStateGT()
        StateUSBL = self.farolStack.getStateUSBL()
        
        if not filterState and not filterStateDR and not StateGT:
            return
       
        elif filterState and filterStateDR and StateGT:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            gt_data = go.Scatter(x=StateGT.Y, y=StateGT.X, mode='lines', name='GT')
            layout = dict(title = 'Error in Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Error in Easting'), yaxis=dict(title='Error in Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data, gt_data], layout=layout) 

        elif filterState and filterStateDR:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            dr_data = go.Scatter(x=filterStateDR.position_east, y=filterStateDR.position_north, mode='lines', name='DR')
            layout = dict(title = 'Error in Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Error in Easting'), yaxis=dict(title='Error in Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, dr_data], layout=layout)
        
        elif filterState:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            layout = dict(title = 'Error in Mission Overview with ' + self.farolStack.getPFDebug().algorithm, xaxis=dict(title='Error in Easting'), yaxis=dict(title='Error in Northing', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/ErrorInMissionOverview.html', auto_open=False)

    def plotFilterposeVirtual(self):
        
        filterState = self.farolStack.getFilterState()
        pathData = self.farolStack.getPathData()
        
        if not filterState or not pathData:
            return
        
        else:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            path_data = go.Scatter(x=pathData.pd[1], y=pathData.pd[0], mode='lines', name='Virtual_Target')
            layout = dict(title = 'Filter vs Virtual Target', xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, path_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/Filter_vs_Virtual.html', auto_open=False)

    def error_plotFilterposeVirtual(self):
        
        filterState = self.farolStack.getFilterState()
        pathData = self.farolStack.getPathData()
        
        if not filterState or not pathData:
            return
        
        else:
            error_x_filter_vec=[]
            error_y_filter_vec=[]

            for index in range(0,len(filterState.position_north)):
                error_x_filter_vec.append(filterState.position_north[index] - pathData.pd[0][0])
                error_y_filter_vec.append(filterState.position_east[index] - pathData.pd[1][0])

            state_data = go.Scatter(x=error_y_filter_vec, y=error_x_filter_vec, mode='lines', name='filter')
            path_data = go.Scatter(x=pathData.error_y_stateVirtual_vec, y=pathData.error_x_stateVirtual_vec, mode='lines', name='Virtual_Target')
            layout = dict(title = 'Error between Filter and Virtual Target', xaxis=dict(title='Error in Easting [m]'), yaxis=dict(title='Error in Northing [m]', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, path_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/Error_between_Filter_and_Virtual.html', auto_open=False)

    def plotFilterposeVirtualposeGT(self):
        
        filterState = self.farolStack.getFilterState()
        pathData = self.farolStack.getPathData()
        StateGT = self.farolStack.getStateGT()
        
        if not filterState or not pathData or not StateGT:
            return
        
        else:
            state_data = go.Scatter(x=filterState.position_east, y=filterState.position_north, mode='lines', name='filter')
            path_data = go.Scatter(x=pathData.pd[1], y=pathData.pd[0], mode='lines', name='Virtual_Target')
            gt_data = go.Scatter(x=StateGT.X, y=StateGT.Y, mode='lines', name='GT')
            layout = dict(title = 'Filter vs Virtual_Target vs GT ', xaxis=dict(title='Easting [m]'), yaxis=dict(title='Northing [m]', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[state_data, path_data, gt_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/Filter_and_VirtualTarget_and_GT.html', auto_open=False)

    def crossTrackAlongTrack(self):
        
        PFdebug = self.farolStack.getPFDebug()
        
        if not PFdebug.cross_track_error or not PFdebug.along_track_error:
            return
        
        else:
            cross_data = go.Scatter(x=PFdebug.time, y=PFdebug.cross_track_error, mode='lines', name='cross_track_error')
            along_data = go.Scatter(x=PFdebug.time, y=PFdebug.along_track_error, mode='lines', name='along_track_error')
            layout = dict(title = 'Along and Cross Track errors', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Error [m]', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[cross_data, along_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/Cross_and_Along_errors.html', auto_open=False)

    def InertialCurrents(self):
        
        FCurrents = self.farolStack.getFilterCurrents()
        
        if not FCurrents.x_current or not FCurrents.y_current:
            return
        
        else:
            x_current_data = go.Scatter(x=FCurrents.time, y=FCurrents.x_current, mode='lines', name='Vx current')
            y_current_data = go.Scatter(x=FCurrents.time, y=FCurrents.y_current, mode='lines', name='Vy current')
            layout = dict(title = 'Inertial Velocity of Current', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Current [m/s]', scaleanchor = 'x', scaleratio = 1))
            fig = dict(data=[x_current_data, y_current_data], layout=layout)

        try:
            os.makedirs(self.datafolder)
        except:
            pass
        
        py.offline.plot(fig, filename=self.datafolder + '/Intertial_Current.html', auto_open=False)  

    def swayRef(self):

        filterState = self.farolStack.getFilterState()
        RSway = self.farolStack.getRefSway()
        #print(filterState.body_velocity_y)
        #print(RSway.value)
        
        if not filterState.body_velocity_y or not RSway.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.body_velocity_y, mode='lines', name='sway from state')
        sway_ref_data = go.Scatter(x=RSway.time, y=RSway.value, mode='lines', name='ref sway')
        layout = dict(title = 'Ref sway vs real sway', xaxis=dict(title='time', nticks=50), yaxis=dict(title='sway [m/s]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, sway_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Sway.html', auto_open=False)

    def surgeRef(self):

        filterState = self.farolStack.getFilterState()
        RSurge = self.farolStack.getRefSurge()
        
        if not filterState.body_velocity_x  or not RSurge.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.body_velocity_x, mode='lines', name='surge from state')
        surge_ref_data = go.Scatter(x=RSurge.time, y=RSurge.value, mode='lines', name='ref surge')
        layout = dict(title = 'Ref surge vs Real surge', xaxis=dict(title='time', nticks=50), yaxis=dict(title='surge [m/s]', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, surge_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Surge.html', auto_open=False)
  
    def yawRef(self):

        filterState = self.farolStack.getFilterState()
        RYaw = self.farolStack.getRefYaw()
        
        if not filterState.orientation_z or not RYaw.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.orientation_z, mode='lines', name='yaw from state')
        yaw_ref_data = go.Scatter(x=RYaw.time, y=RYaw.value, mode='lines', name='ref yaw')
        layout = dict(title = 'Ref yaw vs real yaw', xaxis=dict(title='time', nticks=50), yaxis=dict(title='yaw', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, yaw_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Yaw.html', auto_open=False)

    def yawRateRef(self):

        filterState = self.farolStack.getFilterState()
        RYawRate = self.farolStack.getRefYawRate()
        #print(filterState.orientation_rate_z)
        #print(RYawRate.value)
        
        if not filterState.orientation_rate_z or not RYawRate.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.orientation_rate_z, mode='lines', name='yaw_rate from state')
        yaw_rate_ref_data = go.Scatter(x=RYawRate.time, y=RYawRate.value, mode='lines', name='ref yaw_rate')
        layout = dict(title = 'Ref yaw_rate vs real yaw_rate', xaxis=dict(title='time', nticks=50), yaxis=dict(title='yaw_rate', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, yaw_rate_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Yaw_Rate.html', auto_open=False)

    def depthRef(self):

        filterState = self.farolStack.getFilterState()
        RDepth = self.farolStack.getRefDepth()
        
        if not filterState.position_depth or not RDepth.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.position_depth, mode='lines', name='depth from state')
        depth_ref_data = go.Scatter(x=RDepth.time, y=RDepth.value, mode='lines', name='ref depth')
        layout = dict(title = 'Ref depth vs real depth', xaxis=dict(title='time', nticks=50), yaxis=dict(title='depth', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, depth_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Depth.html', auto_open=False)

    def altitudeRef(self):
        
        filterState = self.farolStack.getFilterState()
        RAltitude = self.farolStack.getRefAltitude()
        #print(filterState.global_position_altitude)
        #print(RAltitude.value)

        if not filterState.global_position_altitude or not RAltitude.value:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.global_position_altitude, mode='lines', name='altitude from state')
        altitude_ref_data = go.Scatter(x=RAltitude.time, y=RAltitude.value, mode='lines', name='ref altitude')
        layout = dict(title = 'Ref altitude vs real altitude', xaxis=dict(title='time', nticks=50), yaxis=dict(title='altitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, altitude_ref_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Ref_Altitude.html', auto_open=False)

    def vxDRvxFilter(self):

        DR = self.farolStack.getFilterStateDR()
        filterState = self.farolStack.getFilterState()
        
        if not DR.seafloor_velocity_x or not filterState.seafloor_velocity_x:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.seafloor_velocity_x, mode='lines', name='Vx in state')
        vx_dr_data = go.Scatter(x=DR.time, y=DR.seafloor_velocity_x, mode='lines', name='Vx in DR')
        layout = dict(title = 'Vx in state vs Vx in DR', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Vx', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, vx_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/vxState_vs_VxDR.html', auto_open=False)

    def vyDRvyFilter(self):

        DR = self.farolStack.getFilterStateDR()
        filterState = self.farolStack.getFilterState()
        
        if not DR.seafloor_velocity_y or not filterState.seafloor_velocity_y:
            return

        # Plot path
        state_data = go.Scatter(x=filterState.time, y=filterState.seafloor_velocity_y, mode='lines', name='Vy in state')
        vy_dr_data = go.Scatter(x=DR.time, y=DR.seafloor_velocity_y, mode='lines', name='Vy in DR')
        layout = dict(title = 'Vy in state vs Vy in DR', xaxis=dict(title='time', nticks=50), yaxis=dict(title='Vy', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[state_data, vy_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/vyState_vs_VyDR.html', auto_open=False)

    def rms_gtFilterDr(self):
        
        filterState = self.farolStack.getFilterState()
        DR = self.farolStack.getFilterStateDR()
        GT = self.farolStack.getStateGT()

        if not filterState and not DR and not GT:
            return
        
        rms_state = []
        rms_dr = []
        
        if not GT.X or not GT.Y:
            return

        if filterState.position_north and filterState.position_east:
            rms_state = rms(GT.X, GT.Y, filterState.position_north, filterState.position_east)
        
        if DR.position_north and DR.position_east:
            rms_dr = rms(GT.X, GT.Y, DR.position_north, DR.position_east)
        
        if rms_state and rms_dr:
            # Plot path
            rms_state_data = go.Scatter(x=filterState.time, y=rms_state, mode='lines', name='rms state')
            rms_dr_data = go.Scatter(x=filterState.time, y=rms_dr, mode='lines', name='rms dr')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_state_data, rms_dr_data], layout=layout)

        elif rms_state:
            # Plot path
            rms_state_data = go.Scatter(x=filterState.time, y=rms_state, mode='lines', name='rms state')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_state_data], layout=layout)

        elif rms_dr:
            # Plot path
            rms_state_data = go.Scatter(x=filterState.time, y=rms_state, mode='lines', name='rms state')
            layout = dict(title = 'RMS', xaxis=dict(title='time', nticks=50), yaxis=dict(title='error [m]', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[rms_dr_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/RMS.html', auto_open=False)

    def usbl_rate(self):

        filterState = self.farolStack.getFilterState()
        StateUSBL = self.farolStack.getStateUSBL()

        #print(StateUSBL.Y)
        #print(StateUSBL.X)
        #print(StateUSBL.time[0])
    
        if not filterState or not StateUSBL:
            return
        
        delta_time_usbl_vec = []
        delta_x_usbl_vec = []
        delta_y_usbl_vec = []
        delta_error = []

        for index in range(0, len(StateUSBL.X)): 
            delta_x_usbl_vec.append(StateUSBL.Y[index] - StateUSBL.Y[0])
            delta_y_usbl_vec.append(StateUSBL.X[index] - StateUSBL.X[0])
            #print(delta_y_usbl_vec)
            #print(delta_x_usbl_vec)
            delta_error.append(math.sqrt(delta_y_usbl_vec[index]**2 + delta_x_usbl_vec[index]**2))
            t1 = datetime.strptime(StateUSBL.time[index], '%H:%M:%S')
            t2 = datetime.strptime(StateUSBL.time[0], '%H:%M:%S')
            delta=t1-t2
            delta_time_usbl_vec.append(delta.total_seconds())

        #print(delta_time_usbl_vec)

        # Plot path
        error_data = go.Scatter(x=delta_time_usbl_vec, y=delta_error, mode='markers', name='X_delta_error_USBL', showlegend=True)
        #y_usbl_data = go.Scatter(x=delta_time_usbl_vec, y=delta_y_usbl_vec, mode='markers', name='Y_delta_error_USBL', showlegend=True)
        layout = dict(title = 'Acoustics rate and |ERROR|', xaxis=dict(title='Delta Time [s]'), yaxis=dict(title='|Error| [m]'))
        fig_data = dict(data=[error_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/Acoustics_rate_and_absError.html', auto_open=False)