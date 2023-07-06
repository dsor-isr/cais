class Float64():
    def __init__(self):
        self.value = []
        self.time = []

class Int8():
    def __init__(self):
        self.value = []
        self.time = []

class mLatLonPos():
    def __init__(self):
        self.mode = []
        self.utc_time = []
        self.satellites = []
        self.latitude = []
        self.longitude = []
        self.altitude = []
        self.course = []
        self.speed_over_ground = []
        self.time = []

class Pressure():
    def __init__(self):
        self.pressure = []
        self.temperature = []
        self.time = []

class mBatMonit():
    def __init__(self):
        self.number_of_packs = []
        self.equalize = []
        self.charging = []
        self.current = []
        self.min_cell = []
        self.max_cell = []
        self.actual_charge = []
        self.min_temp = []
        self.max_temp = []
        self.time = []

class mExplorer():
    def __init__(self):
        self.YY = []
        self.JJJ = []
        self.HH = []
        self.MM = []
        self.SSs = []
        self.FF = []
        self.SS = []
        self.DD = []
        self.TT = []
        self.QQ = []
        self.W = []
        self.P = []
        self.M = []
        self.G = []
        self.time = []

class mIMU():
    def __init__(self):
        self.Yaw = []
        self.Pitch = []
        self.Roll = []
        self.Gx = []
        self.Gy = []
        self.Gz = []
        self.Mx = []
        self.My = []
        self.Mz = []
        self.Ax = []
        self.Ay = []
        self.Az = []
        self.time = []

class imu_pp():
    def __init__(self):
        self.mag_x = []
        self.mag_y = []
        self.mag_z = []
        self.mag_abs = []
        self.time = []

class mRaw_Thr():
    def __init__(self):
        self.data = []
        self.time = []

class mThrusterStatus():
    def __init__(self):
        self.Speed = []
        self.Current = []
        self.Temperature = []
        self.Errors = []
        self.time = []

class mBatMonitRaw():
    def __init__(self):
        self.pack1_cell1 = []
        self.pack1_cell2 = []
        self.pack1_cell3 = []
        self.pack1_cell4 = []
        self.pack1_cell5 = []
        self.pack1_cell6 = []
        self.pack1_cell7 = []
        self.pack2_cell1 = []
        self.pack2_cell2 = []
        self.pack2_cell3 = []
        self.pack2_cell4 = []
        self.pack2_cell5 = []
        self.pack2_cell6 = []
        self.pack2_cell7 = []
        self.time = []

class Bool():
    def __init__(self):
        self.value = []
        self.time = []

class navquest_dvlRes():
    def __init__(self):
        self.error_code = []
        self.good = []
        self.v_depth = []
        self.velo_rad = []
        self.wvelo_rad = []
        self.wvelo_credit = []
        self.velo_instrument = []
        self.velo_earth = []
        self.water_velo_instrument = []
        self.water_velo_earth = []
        self.velo_instrument_flag = []
        self.velo_earth_flag = []
        self.water_velo_instrument_flag = []
        self.water_velo_earth_flag = []
        self.rph = []
        self.depth_estimate = []
        self.temperature = []
        self.pressure = []
        self.salinity = []
        self.sound_speed = []
        self.time = []
