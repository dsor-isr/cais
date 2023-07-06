class NavigationStatus():
    def __init__(self):
        self.altitude = []
        self.body_velocity_x = []
        self.body_velocity_y = []
        self.body_velocity_z = []
        self.global_position_altitude = []
        self.global_position_latitude = []
        self.global_position_longitude = []
        self.orientation_x = []
        self.orientation_y = []
        self.orientation_z = []
        self.orientation_rate_x = []
        self.orientation_rate_y = []
        self.orientation_rate_z = []
        self.orientation_variance_x = []
        self.orientation_variance_y = []
        self.orientation_variance_z = []
        self.origin_altitude = []
        self.origin_latitude = []
        self.origin_longitude = []
        self.position_depth = []
        self.position_east = []
        self.position_north = []
        self.position_variance_depth = []
        self.position_variance_east = []
        self.position_variance_north = []
        self.seafloor_velocity_x = []
        self.seafloor_velocity_y = []
        self.seafloor_velocity_z = []
        self.status = []
        self.time = []

class Int8():
    def __init__(self):
        self.value = []
        self.time = []

class Thruster():
    def __init__(self):
        self.id = []
        self.value = []
        self.time = []

class Currents():
    def __init__(self):
        self.x_current = []
        self.y_current = []
        self.time = []

class mState():
    def __init__(self):
        self.GPS_good = []
        self.IMU_good = []
        self.Depth = []
        self.X = []
        self.Y = []
        self.Z = []
        self.Vx = []
        self.Vy = []
        self.Vz = []
        self.u = []
        self.Yaw = []
        self.Pitch = []
        self.Roll = []
        self.Yaw_Rate = []
        self.Pitch_Rate = []
        self.Roll_Rate = []
        self.In_Press = []
        self.In_Press_dot = []
        self.battety_level = []
        self.altitude = []
        self.status = []
        self.time = []

class BodyForceRequest():
    def __init__(self):
        self.wrench = []
        self.force_x = []
        self.force_y = []
        self.force_z = []
        self.torque_x = []
        self.torque_y = []
        self.torque_z = []
        self.time = []

class PathData():
    def __init__(self):
        self.gamma = []
        self.pd = []
        self.d_pd = []
        self.dd_pd = []
        self.curvature = []
        self.tangent = []
        self.derivative_norm = []
        self.vd = []
        self.d_vd = []
        self.vehicle_speed = []
        self.gamma_min = []
        self.gamma_max = []
        self.time = []
        self.error_x_stateVirtual_vec = []
        self.error_y_stateVirtual_vec = []

class mPFollowingDebug():
    def __init__(self):
        self.algorithm = []
        self.cross_track_error = []
        self.along_track_error = []
        self.yaw = []
        self.psi = []
        self.gamma = []
        self.time = []

class CPFGamma():
    def __init__(self):
        self.ID = []
        self.gamma = []
        self.vd = []
        self.time = []

class mUSBLFix():
    def __init__(self):
        self.source_id = []
        self.source_name = []
        self.source_frame_id = []
        self.type = []
        self.range = []
        self.relative_position = []
        self.bearing = []
        self.elevation = []
        self.sound_speed = []
        self.bearing_raw = []
        self.elevation_raw = []
        self.position_covariance = []
        self.time = [] 
        
class DMACPayload():
    def __init__(self):
        self.msg_id = []
        self.source_address = []
        self.destination_address = []
        self.source_name = []
        self.destination_address = []
        self.type = []
        self.ack = []
        self.force = []
        self.bitrate = []
        self.rssi = []
        self.integrity = []
        self.propagation_time = []
        self.duration = []
        self.timestamp = []
        self.timestamp_undefined = []
        self.relative_velocity = []
        self.payload = []
        self.time = []
