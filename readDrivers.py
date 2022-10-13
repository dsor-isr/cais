import plotly.graph_objs as go
import plotly.offline as py
import os
import time
from handyTools import *
from datetime import datetime

"""
Class responsable for create all plots with respect to the drivers
"""
class Drivers(object):
    def __init__(self, datafolder):
        self.datafolder = datafolder
    
    # Call the correspondent method acording to the topic received
    def analizeDriverData(self, topic, data):
        # print("\n" + topic)
        # if the topic has the word /bat_monit/raw
        if topic.find('/bat_monit/raw') != -1:
            self.bat_monitRaw(topic, data)

        # if the topic has the word /dvl/raw
        elif topic.find('/dvl/raw') != -1:
            self.navquestPlot(topic, data)

        # discard all topics that had the word raw
        if topic.find('raw') != -1:
            return
        
        # if the topic has the word Thruster
        if topic.find('Thruster') != -1:
            self.thrusterPlot(topic, data)
        
        # if the topic has the word altimeter
        elif topic.find('altimeter') != -1:
            self.altimeterPlot(topic, data)

        # if the topic has the word bat_monit
        elif topic.find('bat_monit') != -1:
            self.batMonitPlot(topic, data)

        # if the topic has the word bluetooth
        elif topic.find('bluetooth') != -1:
            self.bluetoothPlot(topic, data)

        # if the topic has the word depth_cell
        elif topic.find('depth_cell') != -1:
            self.depthCellPlot(topic, data)

        # if the topic has the word gps
        elif topic.find('gps') != -1:
            self.gpsPlot(topic, data)

        # if the topic has the word imu
        elif topic.find('imu') != -1:
            self.imuPlot(topic, data)

        # if the topic has the word inside_pressure
        elif topic.find('inside_pressure') != -1:
            self.insidePressurePlot(topic, data)

        # if the topic has the word leaks
        elif topic.find('leaks') != -1:
            self.leaksPlot(topic, data)

        # if the topic has the word parallel_port
        elif topic.find('parallel_port') != -1:
            self.parallelPlot(topic, data)
 
    def thrusterPlot(self, topic, data):
        """
        Plots for Thrusters
        """ 
        # print("Thrusters")
        # get number of the thruster
        if topic.find('Thruster0') != -1: 
            thruster_number = '/Thruster0'
        elif topic.find('Thruster1') != -1: 
            thruster_number = '/Thruster1'
        elif topic.find('Thruster2') != -1: 
            thruster_number = '/Thruster2'
        elif topic.find('Thruster3') != -1: 
            thruster_number = '/Thruster3'
        elif topic.find('Thruster4') != -1: 
            thruster_number = '/Thruster4'
        elif topic.find('Thruster5') != -1: 
            thruster_number = '/Thruster5'

        current = [];
        errors = [];
        speed = [];
        temperature = [];
        time_vec = [];
        for topic, msg, t in data:
            try: current.append(msg.Current)
            except: pass
            try: errors.append(msg.Errors)
            except: pass
            try: speed.append(msg.Speed)
            except: pass
            try: temperature.append(msg.Temperature)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot current
        trace_data = go.Scatter(x=time_vec, y=current, mode='lines', name='current')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Current', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + thruster_number)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + thruster_number + '/Current.html', auto_open=False)

        # Plot errors
        trace_data = go.Scatter(x=time_vec, y=errors, mode='lines', name='errors')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Errors', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)
        
        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + thruster_number)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + thruster_number + '/Errors.html', auto_open=False)
    
        # Plot speed
        trace_data = go.Scatter(x=time_vec, y=speed, mode='lines', name='speed')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Speed', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + thruster_number)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + thruster_number + '/Speed.html', auto_open=False)
        
        # Plot temperature
        trace_data = go.Scatter(x=time_vec, y=temperature, mode='lines', name='temperature')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Temperature', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)
        # py.iplot(fig_data, filename='Temperature')

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + thruster_number)
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + thruster_number + '/Temperature.html',auto_open=False)

    def altimeterPlot(self, topic, data):
        """
        Plots for Altimeter
        """    
        # print("Altimeter")
        value = [];
        time_vec = [];
        for topic, msg, t in data:
            try: value.append(msg.data)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot value
        trace_data = go.Scatter(x=time_vec, y=value, mode='lines', name='altitude')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='altitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/altimeter')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/altimeter/data.html', auto_open=False)

    def batMonitPlot(self, topic, data):
        """
        Plots for BatMonit
        """    
        # print("BatMonit")
        actual_charge = [];
        charging = [];
        current = [];
        equalize = [];
        max_cell = [];
        max_temp = [];
        min_cell = [];
        min_temp = [];
        number_of_packs = [];
        time_vec = [];

        for topic, msg, t in data:
            try: actual_charge.append(msg.actual_charge)
            except: pass
            try: charging.append(msg.charging)
            except: pass
            try: current.append(msg.current)
            except: pass
            try: equalize.append(msg.equalize)
            except: pass
            try: max_cell.append(msg.max_cell)
            except: pass
            try: max_temp.append(msg.max_temp)
            except: pass
            try: min_cell.append(msg.min_cell)
            except: pass
            try: min_temp.append(msg.min_temp)
            except: pass
            try: number_of_packs.append(msg.number_of_packs)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot actual_charge
        trace_data = go.Scatter(x=time_vec, y=actual_charge, mode='lines', name='actual_charge')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='actual_charge', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/actual_charge.html', auto_open=False)

        # Plot charging
        trace_data = go.Scatter(x=time_vec, y=charging, mode='lines', name='charging')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='charging', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/charging.html', auto_open=False)

        # Plot current
        trace_data = go.Scatter(x=time_vec, y=current, mode='lines', name='current')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='current', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass
            # print('Saving current')

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/current.html', auto_open=False)

        # Plot equalize
        trace_data = go.Scatter(x=time_vec, y=equalize, mode='lines', name='equalize')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='equalize', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/equalize.html', auto_open=False)

        # Plot max_cell
        trace_data = go.Scatter(x=time_vec, y=max_cell, mode='lines', name='max_cell')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='max_cell', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/max_cell.html', auto_open=False)

        # Plot max_temp
        trace_data = go.Scatter(x=time_vec, y=max_temp, mode='lines', name='max_temp')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='max_temp', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/max_temp.html', auto_open=False)

        # Plot min_cell
        trace_data = go.Scatter(x=time_vec, y=min_cell, mode='lines', name='min_cell')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='min_cell', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/min_cell.html', auto_open=False)

        # Plot min_temp
        trace_data = go.Scatter(x=time_vec, y=min_temp, mode='lines', name='min_temp')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='min_temp', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/min_temp.html', auto_open=False)
    
        # Plot number_of_packs
        trace_data = go.Scatter(x=time_vec, y=number_of_packs, mode='lines', name='number_of_packs')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='number_of_packs', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/number_of_packs.html', auto_open=False)
    
    def bluetoothPlot(self, topic, data):
        """
        Plots for Bluetooth
        """    
        # print("Bluetooth")
        pass

    def depthCellPlot(self, topic, data):
        """
        Plots for Depth Cell
        """    
        # print("depthCell")
        pressure = [];
        temperature = [];
        time_vec = [];

        for topic, msg, t in data:
            try: pressure.append(msg.pressure)
            except: pass
            try: temperature.append(msg.temperature)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot pressure
        trace_data = go.Scatter(x=time_vec, y=pressure, mode='lines', name='pressure')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='pressure', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/depthCell')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/depthCell/pressure.html', auto_open=False)

        # Plot temperature
        trace_data = go.Scatter(x=time_vec, y=temperature, mode='lines', name='temperature')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='temperature', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/depthCell')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/depthCell/temperature.html', auto_open=False)

    def gpsPlot(self, topic, data):
        # print("gpsPlot")
        """
        Plots for GPS
        """    
        altitude = [];
        course = [];
        latitude = [];
        longitude = [];
        mode = [];
        satellites = [];
        speed_over_ground = [];
        utc_time = [];
        time_vec = [];

        for topic, msg, t in data:
            try: altitude.append(msg.altitude)
            except: pass
            try: course.append(msg.course)
            except: pass
            try: latitude.append(msg.latitude)
            except: pass
            try: longitude.append(msg.longitude)
            except: pass
            try: mode.append(msg.mode)
            except: pass
            try: satellites.append(msg.satellites)
            except: pass
            try: speed_over_ground.append(msg.speed_over_ground)
            except: pass
            try: utc_time.append(msg.utc_time)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot altitude
        trace_data = go.Scatter(x=time_vec, y=altitude, mode='lines', name='altitude')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='altitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/altitude.html', auto_open=False)

        # Plot course
        trace_data = go.Scatter(x=time_vec, y=course, mode='lines', name='course')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='course', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/course.html', auto_open=False)

        # Plot latitude
        trace_data = go.Scatter(x=time_vec, y=latitude, mode='lines', name='latitude')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='latitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/latitude.html', auto_open=False)

        # Plot longitude
        trace_data = go.Scatter(x=time_vec, y=longitude, mode='lines', name='longitude')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='longitude', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/longitude.html', auto_open=False)

        # Plot mode
        trace_data = go.Scatter(x=time_vec, y=mode, mode='lines', name='mode')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='mode', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/mode.html', auto_open=False)

        # Plot satellites
        trace_data = go.Scatter(x=time_vec, y=satellites, mode='lines', name='satellites')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='satellites', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/satellites.html', auto_open=False)

        # Plot speed_over_ground
        trace_data = go.Scatter(x=time_vec, y=speed_over_ground, mode='lines', name='speed_over_ground')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='speed_over_ground', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/speed_over_ground.html', auto_open=False)

        # Plot utc_time
        trace_data = go.Scatter(x=time_vec, y=utc_time, mode='lines', name='utc_time')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='utc_time', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/gps')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/gps/utc_time.html', auto_open=False)

    def imuPlot(self, topic, data):
        """
        Plots for IMU
        """    
        # print("IMU")
        if topic.find('data') != -1:
            Ax = [];
            Ay = [];
            Az = [];
            Gx = [];
            Gy = [];
            Gz = [];
            Mx = [];
            My = [];
            Mz = [];
            Pitch = [];
            Roll = [];
            Yaw = [];
            time_vec = [];
            time_vec_imu = [];

            for topic, msg, t in data:
                try: Ax.append(msg.Ax)
                except: pass
                try: Ay.append(msg.Ay)
                except: pass
                try: Az.append(msg.Az)
                except: pass
                try: Gx.append(msg.Gx)
                except: pass
                try: Gy.append(msg.Gy)
                except: pass
                try: Gz.append(msg.Gz)
                except: pass
                try: Mx.append(msg.Mx)
                except: pass
                try: My.append(msg.My)
                except: pass
                try: Mz.append(msg.Mz)
                except: pass
                try: Pitch.append(wrapTo360(msg.Pitch))
                except: pass
                try: Roll.append(wrapTo360(msg.Roll))
                except: pass
                try: Yaw.append(wrapTo360(msg.Yaw))
                except: pass
                # milisecond resolution
                try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                except: pass
                # seconds resolution
                try: time_vec_imu.append(time.strftime(('%H:%M:%S'), time.gmtime(t.to_sec())))
                except: pass

            # Plot Ax
            trace_data = go.Scatter(x=time_vec, y=Ax, mode='lines', name='Ax')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50, tickformat='%H:%M:%S'), yaxis=dict(title='Ax', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Ax.html', auto_open=False)

            # Plot Ay
            trace_data = go.Scatter(x=time_vec, y=Ay, mode='lines', name='Ay')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Ay', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Ay.html', auto_open=False)

            # Plot Az
            trace_data = go.Scatter(x=time_vec, y=Az, mode='lines', name='Az')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Az', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Az.html', auto_open=False)

            # Plot Gx
            trace_data = go.Scatter(x=time_vec, y=Gx, mode='lines', name='Gx')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Gx', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Gx.html', auto_open=False)

            # Plot Gy
            trace_data = go.Scatter(x=time_vec, y=Ax, mode='lines', name='Gy')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Gy', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Gy.html', auto_open=False)

            # Plot Gz
            trace_data = go.Scatter(x=time_vec, y=Gz, mode='lines', name='Gz')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Gz', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Gz.html', auto_open=False)

            # Plot Mx
            trace_data = go.Scatter(x=time_vec, y=Mx, mode='lines', name='Mx')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Mx', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Mx.html', auto_open=False)

            # Plot My
            trace_data = go.Scatter(x=time_vec, y=My, mode='lines', name='My')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='My', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/My.html', auto_open=False)

            # Plot Mz
            trace_data = go.Scatter(x=time_vec, y=Mz, mode='lines', name='Mz')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Mz', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Mz.html', auto_open=False)

            # Plot Mx vs My
            trace_data = go.Scatter(x=Mx, y=My, mode='lines', name='Mx_vs_My')
            layout = dict(title = topic, xaxis=dict(title='Mx', nticks=50), yaxis=dict(title='My', scaleanchor = "x", scaleratio = 1, nticks=50))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Mx_vs_My.html', auto_open=False)

            # Plot Pitch
            trace_data = go.Scatter(x=time_vec, y=Pitch, mode='lines', name='Pitch')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Pitch', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Pitch.html', auto_open=False)

            # Plot Roll
            trace_data = go.Scatter(x=time_vec, y=Roll, mode='lines', name='Roll')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Roll', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Roll.html', auto_open=False)

            # Plot Yaw
            trace_data = go.Scatter(x=time_vec, y=Yaw, mode='lines', name='Yaw')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Yaw', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/Yaw.html', auto_open=False)

        if topic.find('imu_pp') != -1:
            mag_abs = [];
            mag_x = [];
            mag_y = [];
            mag_z = [];
            time_vec = [];

            for topic, msg, t in data:
                try: mag_abs.append(msg.mag_abs)
                except: pass
                try: mag_x.append(msg.mag_x)
                except: pass
                try: mag_y.append(msg.mag_y)
                except: pass
                try: mag_z.append(msg.mag_z)
                except: pass
                try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                except: pass

            # Plot mag_abs
            trace_data = go.Scatter(x=time_vec, y=mag_abs, mode='lines', name='mag_abs')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='mag_abs', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/imu_pp_mag_abs.html', auto_open=False)

            # Plot mag_x
            trace_data = go.Scatter(x=time_vec, y=mag_x, mode='lines', name='mag_x')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='mag_x', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/imu_pp_mag_x.html', auto_open=False)

            # Plot mag_y
            trace_data = go.Scatter(x=time_vec, y=mag_y, mode='lines', name='mag_y')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='mag_y', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/imu_pp_mag_y.html', auto_open=False)

            # Plot mag_z
            trace_data = go.Scatter(x=time_vec, y=mag_z, mode='lines', name='mag_z')
            layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='mag_z', scaleanchor = "x", scaleratio = 1))
            fig_data = dict(data=[trace_data], layout=layout)

            # Save Plot
            try:  # else already exists
                os.makedirs(self.datafolder + '/imu')
            except:
                pass

            py.offline.plot(fig_data, filename=self.datafolder + '/imu/imu_pp_mag_z.html', auto_open=False)

    def insidePressurePlot(self, topic, data):
        """
        Plots for Inside Pressure
        """    
        # print("insidePressure")
        pressure = [];
        temperature = [];
        time_vec = [];

        for topic, msg, t in data:
            try: pressure.append(msg.pressure)
            except: pass
            try: temperature.append(msg.temperature)
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot pressure
        trace_data = go.Scatter(x=time_vec, y=pressure, mode='lines', name='pressure')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='pressure', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/insidePressure')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/insidePressure/pressure.html', auto_open=False)

        # Plot temperature
        trace_data = go.Scatter(x=time_vec, y=temperature, mode='lines', name='temperature')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='temperature', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/insidePressure')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/insidePressure/temperature.html', auto_open=False)

    def leaksPlot(self, topic, data):
        """
        Plots for Leaks
        """    
        # print("Leaks")
        pass

    def parallelPlot(self, topic, data):
        """
        Plot for parallel Plot
        """    
        # print("parallel_port")
        pass

    def navquestPlot(self, topic, data):
        """
        Plots for DVL
        """    
        # print("DVL")

        # if the topic has enable discard
        if topic.find('enable') != -1:
            return
        
        depth_estimate = [];
        error_code = [];
        good_0 = [];
        good_1 = [];
        good_2 = [];
        good_3 = [];
        pressure = [];
        rph_0 = [];
        rph_1 = [];
        rph_2 = [];
        salinity = [];
        sound_speed = [];
        temperature = [];
        v_depth_0 = [];
        v_depth_1 = [];
        v_depth_2 = [];
        v_depth_3 = [];
        velo_earth_0 = [];
        velo_earth_1 = [];
        velo_earth_2 = [];
        velo_earth_flag = [];
        velo_instrument_0 = [];
        velo_instrument_1 = [];
        velo_instrument_2 = [];
        velo_instrument_flag = [];
        velo_rad_0 = [];
        velo_rad_1 = [];
        velo_rad_2 = [];
        velo_rad_3 = [];
        water_velo_earth_0 = [];
        water_velo_earth_1 = [];
        water_velo_earth_2 = [];
        water_velo_earth_flag = [];
        water_velo_instrument_0 = [];
        water_velo_instrument_1 = [];
        water_velo_instrument_2 = [];
        water_velo_instrument_flag = [];
        wvelo_credit_0 = [];
        wvelo_credit_1 = [];
        wvelo_credit_2 = [];
        wvelo_credit_3 = [];
        wvelo_rad_0 = [];
        wvelo_rad_1 = [];
        wvelo_rad_2 = [];
        wvelo_rad_3 = [];
        time_vec = [];

        for topic, msg, t in data:
            try: depth_estimate.append(msg.depth_estimate)
            except: pass
            try: error_code.append(msg.error_code)
            except: pass
            try: good_0.append(msg.good[0])
            except: pass
            try: good_1.append(msg.good[1])
            except: pass
            try: good_2.append(msg.good[2])
            except: pass
            try: good_3.append(msg.good[3])
            except: pass
            try: pressure.append(msg.pressure)
            except: pass
            try: rph_0.append(msg.rph[0])
            except: pass
            try: rph_1.append(msg.rph[1])
            except: pass
            try: rph_2.append(msg.rph[2])
            except: pass
            try: salinity.append(msg.salinity)
            except: pass
            try: sound_speed.append(msg.sound_speed)
            except: pass
            try: temperature.append(msg.temperature)
            except: pass
            try: v_depth_0.append(msg.v_depth[0])
            except: pass
            try: v_depth_1.append(msg.v_depth[1])
            except: pass
            try: v_depth_2.append(msg.v_depth[2])
            except: pass
            try: v_depth_3.append(msg.v_depth[3])
            except: pass
            try: velo_earth_0.append(msg.velo_earth[0])
            except: pass
            try: velo_earth_1.append(msg.velo_earth[1])
            except: pass
            try: velo_earth_2.append(msg.velo_earth[2])
            except: pass
            try: velo_earth_flag.append(msg.velo_earth_flag)
            except: pass
            try: velo_instrument_0.append(msg.velo_instrument[0])
            except: pass
            try: velo_instrument_1.append(msg.velo_instrument[1])
            except: pass
            try: velo_instrument_2.append(msg.velo_instrument[2])
            except: pass
            try: velo_instrument_flag.append(msg.velo_instrument_flag)
            except: pass
            try: velo_rad_0.append(msg.velo_rad[0])
            except: pass
            try: velo_rad_1.append(msg.velo_rad[1])
            except: pass
            try: velo_rad_2.append(msg.velo_rad[2])
            except: pass
            try: velo_rad_3.append(msg.velo_rad[3])
            except: pass
            try: water_velo_earth_0.append(msg.water_velo_earth[0])
            except: pass
            try: water_velo_earth_1.append(msg.water_velo_earth[1])
            except: pass
            try: water_velo_earth_2.append(msg.water_velo_earth[2])
            except: pass
            try: water_velo_earth_flag.append(msg.water_velo_earth_flag)
            except: pass
            try: water_velo_instrument_0.append(msg.water_velo_instrument[0])
            except: pass
            try: water_velo_instrument_1.append(msg.water_velo_instrument[1])
            except: pass
            try: water_velo_instrument_2.append(msg.water_velo_instrument[2])
            except: pass
            try: water_velo_instrument_flag.append(msg.water_velo_instrument_flag)
            except: pass
            try: wvelo_credit_0.append(msg.wvelo_credit[0])
            except: pass
            try: wvelo_credit_1.append(msg.wvelo_credit[1])
            except: pass
            try: wvelo_credit_2.append(msg.wvelo_credit[2])
            except: pass
            try: wvelo_credit_3.append(msg.wvelo_credit[3])
            except: pass
            try: wvelo_rad_0.append(msg.wvelo_rad[0])
            except: pass
            try: wvelo_rad_1.append(msg.wvelo_rad[1])
            except: pass
            try: wvelo_rad_2.append(msg.wvelo_rad[2])
            except: pass
            try: wvelo_rad_3.append(msg.wvelo_rad[3])
            except: pass
            try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            except: pass

        # Plot depth_estimate
        trace_data = go.Scatter(x=time_vec, y=depth_estimate, mode='lines', name='depth_estimate')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='depth_estimate', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/depth_estimate.html', auto_open=False)

        # Plot error_code
        trace_data = go.Scatter(x=time_vec, y=error_code, mode='lines', name='error_code')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='error_code', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/error_code.html', auto_open=False)
        
        # Plot good_0
        trace_data = go.Scatter(x=time_vec, y=good_0, mode='lines', name='good_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='good_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/good_0.html', auto_open=False)

        # Plot good_1
        trace_data = go.Scatter(x=time_vec, y=good_1, mode='lines', name='good_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='good_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/good_1.html', auto_open=False)

        # Plot good_2
        trace_data = go.Scatter(x=time_vec, y=good_2, mode='lines', name='good_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='good_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/good_2.html', auto_open=False)

        # Plot good_3
        trace_data = go.Scatter(x=time_vec, y=good_3, mode='lines', name='good_3')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='good_3', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/good_3.html', auto_open=False)

        # Plot pressure
        trace_data = go.Scatter(x=time_vec, y=pressure, mode='lines', name='pressure')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='pressure', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/pressure.html', auto_open=False)

        # Plot rph_0
        trace_data = go.Scatter(x=time_vec, y=rph_0, mode='lines', name='rph_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='rph_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/rph_0.html', auto_open=False)

        # Plot rph_1
        trace_data = go.Scatter(x=time_vec, y=rph_1, mode='lines', name='rph_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='rph_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/rph_1.html', auto_open=False)

        # Plot rph_2
        trace_data = go.Scatter(x=time_vec, y=rph_2, mode='lines', name='rph_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='rph_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/rph_2.html', auto_open=False)

        # Plot salinity
        trace_data = go.Scatter(x=time_vec, y=salinity, mode='lines', name='salinity')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='salinity', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/salinity.html', auto_open=False)

        # Plot sound_speed
        trace_data = go.Scatter(x=time_vec, y=sound_speed, mode='lines', name='sound_speed')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='sound_speed', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/sound_speed.html', auto_open=False)

        # Plot temperature
        trace_data = go.Scatter(x=time_vec, y=temperature, mode='lines', name='temperature')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='temperature', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/temperature.html', auto_open=False)

        # Plot v_depth_0
        trace_data = go.Scatter(x=time_vec, y=v_depth_0, mode='lines', name='v_depth_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='v_depth_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/v_depth_0.html', auto_open=False)

        # Plot v_depth_1
        trace_data = go.Scatter(x=time_vec, y=v_depth_1, mode='lines', name='v_depth_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='v_depth_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/v_depth_1.html', auto_open=False)

        # Plot v_depth_2
        trace_data = go.Scatter(x=time_vec, y=v_depth_2, mode='lines', name='v_depth_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='v_depth_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/v_depth_2.html', auto_open=False)

        # Plot v_depth_3
        trace_data = go.Scatter(x=time_vec, y=v_depth_3, mode='lines', name='v_depth_3')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='v_depth_3', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/v_depth_3.html', auto_open=False)

        # Plot velo_earth_0
        trace_data = go.Scatter(x=time_vec, y=velo_earth_0, mode='lines', name='velo_earth_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_earth_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_earth_0.html', auto_open=False)

        # Plot velo_earth_1
        trace_data = go.Scatter(x=time_vec, y=velo_earth_1, mode='lines', name='velo_earth_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_earth_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_earth_1.html', auto_open=False)

        # Plot velo_earth_2
        trace_data = go.Scatter(x=time_vec, y=velo_earth_2, mode='lines', name='velo_earth_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_earth_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_earth_2.html', auto_open=False)

        # Plot velo_earth_flag
        trace_data = go.Scatter(x=time_vec, y=velo_earth_flag, mode='lines', name='velo_earth_flag')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_earth_flag', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass
        
        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_earth_flag.html', auto_open=False)

        # Plot velo_instrument_0
        trace_data = go.Scatter(x=time_vec, y=velo_instrument_0, mode='lines', name='velo_instrument_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_instrument_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_instrument_0.html', auto_open=False)

        # Plot velo_instrument_1
        trace_data = go.Scatter(x=time_vec, y=velo_instrument_1, mode='lines', name='velo_instrument_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_instrument_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_instrument_1.html', auto_open=False)

        # Plot velo_instrument_2
        trace_data = go.Scatter(x=time_vec, y=velo_instrument_2, mode='lines', name='velo_instrument_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_instrument_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_instrument_2.html', auto_open=False)

        # Plot velo_instrument_flag
        trace_data = go.Scatter(x=time_vec, y=velo_instrument_flag, mode='lines', name='velo_instrument_flag')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='velo_instrument_flag', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/velo_instrument_flag.html', auto_open=False)

        # Plot wvelo_credit_0
        trace_data = go.Scatter(x=time_vec, y=wvelo_credit_0, mode='lines', name='wvelo_credit_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_credit_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_credit_0.html', auto_open=False)

        # Plot wvelo_credit_1
        trace_data = go.Scatter(x=time_vec, y=wvelo_credit_1, mode='lines', name='wvelo_credit_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_credit_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_credit_1.html', auto_open=False)

        # Plot wvelo_credit_2
        trace_data = go.Scatter(x=time_vec, y=wvelo_credit_2, mode='lines', name='wvelo_credit_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_credit_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_credit_2.html', auto_open=False)

        # Plot wvelo_credit_3
        trace_data = go.Scatter(x=time_vec, y=wvelo_credit_3, mode='lines', name='wvelo_credit_3')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_credit_3', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_credit_3.html', auto_open=False)

        # Plot wvelo_rad_0
        trace_data = go.Scatter(x=time_vec, y=wvelo_rad_0, mode='lines', name='wvelo_rad_0')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_rad_0', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_rad_0.html', auto_open=False)

        # Plot wvelo_rad_1
        trace_data = go.Scatter(x=time_vec, y=wvelo_rad_1, mode='lines', name='wvelo_rad_1')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_rad_1', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_rad_1.html', auto_open=False)

        # Plot wvelo_rad_2
        trace_data = go.Scatter(x=time_vec, y=wvelo_rad_2, mode='lines', name='wvelo_rad_2')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_rad_2', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_rad_2.html', auto_open=False)

        # Plot wvelo_rad_3
        trace_data = go.Scatter(x=time_vec, y=wvelo_rad_3, mode='lines', name='wvelo_rad_3')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='wvelo_rad_3', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/navquest')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/navquest/wvelo_rad_3.html', auto_open=False)
    
    def bat_monitRaw(self, topic, data):
        """
        Plot the tension per cell for each pack
        """    
        # print("BatMonit")
        pack1_cell1 = []
        pack1_cell2 = []
        pack1_cell3 = []
        pack1_cell4 = []
        pack1_cell5 = []
        pack1_cell6 = []
        pack1_cell7 = []
        
        pack2_cell1 = []
        pack2_cell2 = []
        pack2_cell3 = []
        pack2_cell4 = []
        pack2_cell5 = []
        pack2_cell6 = []
        pack2_cell7 = []

        time_vec = []

        for topic, msg, t in data:
            raw_splited = msg.sentence.split(',')
            if len(raw_splited) > 7:
                try: time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
                except: pass
                if raw_splited[1] == '1': #Pack 1
                    try: pack1_cell1.append(int(raw_splited[3]))
                    except: pass
                    try: pack1_cell2.append(int(raw_splited[4]))
                    except: pass
                    try: pack1_cell3.append(int(raw_splited[5]))
                    except: pass
                    try: pack1_cell4.append(int(raw_splited[6]))
                    except: pass
                    try: pack1_cell5.append(int(raw_splited[7]))
                    except: pass
                    try: pack1_cell6.append(int(raw_splited[8]))
                    except: pass
                    try: pack1_cell7.append(int(raw_splited[9]))
                    except: pass
                elif raw_splited[1] == '2': #Pack 2
                    try: pack2_cell1.append(int(raw_splited[3]))
                    except: pass
                    try: pack2_cell2.append(int(raw_splited[4]))
                    except: pass
                    try: pack2_cell3.append(int(raw_splited[5]))
                    except: pass
                    try: pack2_cell4.append(int(raw_splited[6]))
                    except: pass
                    try: pack2_cell5.append(int(raw_splited[7]))
                    except: pass
                    try: pack2_cell6.append(int(raw_splited[8]))
                    except: pass
                    try: pack2_cell7.append(int(raw_splited[9]))
                    except: pass
       
        # Plot path
        pack1_cell1_data = go.Scatter(x=time_vec, y=pack1_cell1, mode='lines', name='cell1')
        pack1_cell2_data = go.Scatter(x=time_vec, y=pack1_cell2, mode='lines', name='cell2')
        pack1_cell3_data = go.Scatter(x=time_vec, y=pack1_cell3, mode='lines', name='cell3')
        pack1_cell4_data = go.Scatter(x=time_vec, y=pack1_cell4, mode='lines', name='cell4')
        pack1_cell5_data = go.Scatter(x=time_vec, y=pack1_cell5, mode='lines', name='cell5')
        pack1_cell6_data = go.Scatter(x=time_vec, y=pack1_cell6, mode='lines', name='cell6')
        pack1_cell7_data = go.Scatter(x=time_vec, y=pack1_cell7, mode='lines', name='cell7')
        layout = dict(title = 'Tension per cell in Pack 1', xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Tension [mV]'))
        fig_data = dict(data=[pack1_cell1_data, pack1_cell2_data, pack1_cell3_data, pack1_cell4_data, pack1_cell5_data, pack1_cell6_data, pack1_cell7_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/Tension_Pack1.html', auto_open=False)

        # Plot path
        pack2_cell1_data = go.Scatter(x=time_vec, y=pack2_cell1, mode='lines', name='cell1')
        pack2_cell2_data = go.Scatter(x=time_vec, y=pack2_cell2, mode='lines', name='cell2')
        pack2_cell3_data = go.Scatter(x=time_vec, y=pack2_cell3, mode='lines', name='cell3')
        pack2_cell4_data = go.Scatter(x=time_vec, y=pack2_cell4, mode='lines', name='cell4')
        pack2_cell5_data = go.Scatter(x=time_vec, y=pack2_cell5, mode='lines', name='cell5')
        pack2_cell6_data = go.Scatter(x=time_vec, y=pack2_cell6, mode='lines', name='cell6')
        pack2_cell7_data = go.Scatter(x=time_vec, y=pack2_cell7, mode='lines', name='cell7')
        layout = dict(title = 'Tension per cell in Pack 2', xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Tension [mV]'))
        fig_data = dict(data=[pack2_cell1_data, pack2_cell2_data, pack2_cell3_data, pack2_cell4_data, pack2_cell5_data, pack2_cell6_data, pack2_cell7_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/batMonit')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/batMonit/Tension_Pack2.html', auto_open=False)
