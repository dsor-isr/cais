import plotly.graph_objs as go
import plotly.offline as py
import os
import time
from handyTools import *
from datetime import datetime

"""
Class responsable for create all plots with respect to the USBL
"""
class DriverUSBL(object):
    def __init__(self, datafolder):
        self.datafolder = datafolder
    
    # Call the correspondent method acording to the topic received
    def analizeUSBLdriverData(self, topic, data):
        # if the topic has the word measurement/usbl_fix
        if topic.find('measurement/usbl_fix') != -1:
            self.measurement_usbl_fix(topic, data)
        
        # if the topic has the word recv
        elif topic.find('recv') != -1:
            self.recv(topic, data)

        # if the topic has the word send
        elif topic.find('send') != -1:
            self.send(topic, data)

    def analizeSensorsUSBLFixData(self, topic, data):
        
        bearing = []
        bearing_raw = []
        elevation = []
        elevation_raw = []
        range_ = []
        source_id = []
        time_vec = [];
        time_sec_vec = [];

        counter_of_good_bearing = 0  # good here is when we recive a value different of zero
        counter_of_good_elevation = 0
        counter_of_good_range = 0

        for topic, msg, t in data:
            bearing.append(msg.bearing)
            bearing_raw.append(msg.bearing_raw)
            elevation.append(msg.elevation)
            elevation_raw.append(msg.elevation_raw)
            range_.append(msg.range)
            source_id.append(msg.source_id)
            time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])
            time_sec_vec.append(t.to_sec())

            # To Know the percentagem of data that are usefull, to available the quality of the accustic chanel
            if msg.bearing_raw != 0.0: counter_of_good_bearing = counter_of_good_bearing +1
            if msg.elevation_raw != 0.0: counter_of_good_elevation = counter_of_good_elevation +1
            if msg.range != 0.0: counter_of_good_range = counter_of_good_range +1

        # calculate percentage
        per_of_bearing = round((counter_of_good_bearing/len(bearing))*100, 1)
        per_of_elevation = round((counter_of_good_bearing/len(elevation))*100, 1)
        per_of_range = round((counter_of_good_range/len(range_))*100, 1)

        delta_time_vec = []
        for index in range(0, len(time_sec_vec)): 
            delta_time_vec.append(time_sec_vec[index] - time_sec_vec[0])

        # plot bearing and bearing_raw
        bearing_data = go.Scatter(x=delta_time_vec, y=bearing, mode='markers', name='bearing')
        bearing_raw_data = go.Scatter(x=delta_time_vec, y=bearing_raw, mode='markers', name='bearing_raw')
        layout = dict(title='Bearing vs Bearing_Raw: ' + str(per_of_bearing) + '% of values not zero (' + str(counter_of_good_bearing) + ' values)', xaxis=dict(title='Delta Time [s]', nticks=50), yaxis=dict(title='angles [rad]'))
        fig_data = dict(data=[bearing_data, bearing_raw_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/sensors_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/sensors_usbl_fix/bearing_vs_bearing_raw.html', auto_open=False)

        # plot elevation and elevation_raw
        elevation_data = go.Scatter(x=delta_time_vec, y=elevation, mode='markers', name='elevation')
        elevation_raw_data = go.Scatter(x=delta_time_vec, y=elevation_raw, mode='markers', name='elevation_raw')
        layout = dict(title='Elevation vs Elevation_Raw: ' + str(per_of_elevation) + '% of values not zero (' + str(counter_of_good_elevation) + ' values)', xaxis=dict(title='Delta Time [s]', nticks=50), yaxis=dict(title='angles [rad]'))
        fig_data = dict(data=[elevation_data, elevation_raw_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/sensors_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/sensors_usbl_fix/elevation_vs_elevation_raw.html', auto_open=False)

        # plot range
        range_data = go.Scatter(x=delta_time_vec, y=range_, mode='markers', name='range', showlegend=True)
        layout = dict(title='Range vs Range_Raw: ' + str(per_of_range) + '% of values not zero (' + str(counter_of_good_range) + ' values)', xaxis=dict(title='Delta Time [s]', nticks=50), yaxis=dict(title='Range [m]'))
        fig_data = dict(data=[range_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/sensors_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/sensors_usbl_fix/range.html', auto_open=False)

        # plot source_id
        source_id_data = go.Scatter(x=delta_time_vec, y=source_id, mode='lines', name='source_id', showlegend=True)
        layout = dict(title=topic, xaxis=dict(title='Delta Time [s]', nticks=50), yaxis=dict(title='source_id'))
        fig_data = dict(data=[source_id_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/sensors_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/sensors_usbl_fix/source_id.html', auto_open=False)

        # plot range bearing and elevation 
        range_data = go.Scatter(x=delta_time_vec, y=range_, mode='markers', name='range', showlegend=True)
        bearing_data = go.Scatter(x=delta_time_vec, y=bearing, mode='markers', name='bearing', showlegend=True)
        elevation_data = go.Scatter(x=delta_time_vec, y=elevation, mode='markers', name='elevation', showlegend=True)
        layout = dict(title=topic, xaxis=dict(title='Delta Time [s]', nticks=50), yaxis=dict(title='Values'))
        fig_data = dict(data=[range_data, bearing_data, elevation_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/sensors_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/sensors_usbl_fix/range_vs_bering_vs_elevation.html', auto_open=False)

    def measurement_usbl_fix(self, topic, data):
    
        source_id = [];
        type_id = [];
        range_ = [];
        bearing = [];
        elevation = [];
        sound_speed = [];
        bearing_raw = [];
        elevation_raw = [];
        time_vec = [];
        
        for topic, msg, t in data:
            source_id.append(msg.source_id)
            type_id.append(msg.type)
            range_.append(msg.range)
            bearing.append(msg.bearing)
            elevation.append(msg.elevation)
            sound_speed.append(msg.sound_speed)
            bearing_raw.append(msg.bearing_raw)
            elevation_raw.append(msg.elevation_raw)
            time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])

        # Plot source_id
        trace_data = go.Scatter(x=time_vec, y=source_id, mode='lines', name='source_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Source_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/source_id.html', auto_open=False)

        # Plot type_id
        trace_data = go.Scatter(x=time_vec, y=type_id, mode='lines', name='type_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Type_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/type_id.html', auto_open=False)

        # Plot range_
        trace_data = go.Scatter(x=time_vec, y=range_, mode='lines', name='range')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Range', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Range.html', auto_open=False)

        # Plot bearing
        trace_data = go.Scatter(x=time_vec, y=bearing, mode='lines', name='bearing')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Bearing', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Bearing.html', auto_open=False)

        # Plot elevation
        trace_data = go.Scatter(x=time_vec, y=elevation, mode='lines', name='elevation')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Elevation', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Elevation.html', auto_open=False)

        # Plot sound_speed
        trace_data = go.Scatter(x=time_vec, y=sound_speed, mode='lines', name='sound_speed')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Sound_speed', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Sound_speed.html', auto_open=False)

        # Plot bearing_raw
        trace_data = go.Scatter(x=time_vec, y=bearing_raw, mode='markers', name='bearing_raw')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Bearing_Raw', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Bearing_Raw.html', auto_open=False)

        # Plot elevation_raw
        trace_data = go.Scatter(x=time_vec, y=elevation_raw, mode='markers', name='elevation_raw')
        layout = dict(title = topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='Elevation_Raw', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/measurement_usbl_fix')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/measurement_usbl_fix/Elevation_Raw.html', auto_open=False)


    def send(self, topic, data):
    
        msg_id = [];
        source_address = [];
        destination_address = [];
        type_id = [];
        bitrate = [];
        rssi = [];
        integrity = [];
        propagation_time = [];
        duration = [];
        relative_velocity = [];
        time_vec = [];
        
        for topic, msg, t in data:
            msg_id.append(msg.msg_id)
            source_address.append(msg.source_address)
            destination_address.append(msg.destination_address)
            type_id.append(msg.type)
            bitrate.append(msg.bitrate)
            rssi.append(msg.rssi)
            integrity.append(msg.integrity)
            propagation_time.append(msg.propagation_time)
            duration.append(msg.duration)
            relative_velocity.append(msg.relative_velocity)
            time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])

        # Plot msg_id
        trace_data = go.Scatter(x=time_vec, y=msg_id, mode='lines', name='msg_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='msg_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/msg_id.html', auto_open=False)

        # Plot source_address
        trace_data = go.Scatter(x=time_vec, y=source_address, mode='lines', name='source_address')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='source_address', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/source_address.html', auto_open=False)

        # Plot destination_address
        trace_data = go.Scatter(x=time_vec, y=destination_address, mode='lines', name='destination_address')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='destination_address', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/destination_address.html', auto_open=False)

        # Plot type_id
        trace_data = go.Scatter(x=time_vec, y=type_id, mode='lines', name='type_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='type_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/type_id.html', auto_open=False)

        # Plot bitrate
        trace_data = go.Scatter(x=time_vec, y=bitrate, mode='lines', name='bitrate')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='bitrate', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/bitrate.html', auto_open=False)

        # Plot rssi
        trace_data = go.Scatter(x=time_vec, y=rssi, mode='lines', name='rssi')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='rssi', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/rssi.html', auto_open=False)

        # Plot integrity
        trace_data = go.Scatter(x=time_vec, y=integrity, mode='lines', name='integrity')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='integrity', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/integrity.html', auto_open=False)

        # Plot propagation_time
        trace_data = go.Scatter(x=time_vec, y=propagation_time, mode='lines', name='propagation_time')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='propagation_time', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/propagation_time.html', auto_open=False)

        # Plot duration
        trace_data = go.Scatter(x=time_vec, y=duration, mode='lines', name='duration')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='duration', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/duration.html', auto_open=False)

        # Plot relative_velocity
        trace_data = go.Scatter(x=time_vec, y=relative_velocity, mode='lines', name='relative_velocity')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='relative_velocity', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/send')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/send/relative_velocity.html', auto_open=False)

    def recv(self, topic, data):
    
        msg_id = [];
        source_address = [];
        destination_address = [];
        type_id = [];
        bitrate = [];
        rssi = [];
        integrity = [];
        propagation_time = [];
        duration = [];
        relative_velocity = [];
        time_vec = [];
        
        for topic, msg, t in data:
            msg_id.append(msg.msg_id)
            source_address.append(msg.source_address)
            destination_address.append(msg.destination_address)
            type_id.append(msg.type)
            bitrate.append(msg.bitrate)
            rssi.append(msg.rssi)
            integrity.append(msg.integrity)
            propagation_time.append(msg.propagation_time)
            duration.append(msg.duration)
            relative_velocity.append(msg.relative_velocity)
            time_vec.append(datetime.fromtimestamp(t.to_sec()).strftime('%H:%M:%S.%f')[:-3])

        # Plot msg_id
        trace_data = go.Scatter(x=time_vec, y=msg_id, mode='lines', name='msg_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='msg_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/msg_id.html', auto_open=False)

        # Plot source_address
        trace_data = go.Scatter(x=time_vec, y=source_address, mode='lines', name='source_address')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='source_address', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/source_address.html', auto_open=False)

        # Plot destination_address
        trace_data = go.Scatter(x=time_vec, y=destination_address, mode='lines', name='destination_address')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='destination_address', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/destination_address.html', auto_open=False)

        # Plot type_id
        trace_data = go.Scatter(x=time_vec, y=type_id, mode='lines', name='type_id')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='type_id', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/type_id.html', auto_open=False)

        # Plot bitrate
        trace_data = go.Scatter(x=time_vec, y=bitrate, mode='lines', name='bitrate')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='bitrate', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/bitrate.html', auto_open=False)

        # Plot rssi
        trace_data = go.Scatter(x=time_vec, y=rssi, mode='lines', name='rssi')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='rssi', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/rssi.html', auto_open=False)

        # Plot integrity
        trace_data = go.Scatter(x=time_vec, y=integrity, mode='lines', name='integrity')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='integrity', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/integrity.html', auto_open=False)

        # Plot propagation_time
        trace_data = go.Scatter(x=time_vec, y=propagation_time, mode='lines', name='propagation_time')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='propagation_time', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/propagation_time.html', auto_open=False)

        # Plot duration
        trace_data = go.Scatter(x=time_vec, y=duration, mode='lines', name='duration')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='duration', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/duration.html', auto_open=False)

        # Plot relative_velocity
        trace_data = go.Scatter(x=time_vec, y=relative_velocity, mode='lines', name='relative_velocity')
        layout = dict(title=topic, xaxis=dict(title='Time', nticks=50), yaxis=dict(title='relative_velocity', scaleanchor = "x", scaleratio = 1))
        fig_data = dict(data=[trace_data], layout=layout)

        # Save Plot
        try:  # else already exists
            os.makedirs(self.datafolder + '/recv')
        except:
            pass

        py.offline.plot(fig_data, filename=self.datafolder + '/recv/relative_velocity.html', auto_open=False)
