import json
import os
import re
import portalocker

class Profile:
    """
    A class to represent a profile. A profile is a set of filters that can be applied to a list of strings.

    Attributes
    ----------
    name : str
        name of the profile
    usbl : bool
        boolean flag to determine if the profile cares about USBL
    altimeter : bool
        boolean flag to determine if the profile cares about altimeter
    depthCell : bool
        boolean flag to determine if the profile cares about depthCell
    gps : bool
        boolean flag to determine if the profile cares about gps
    imu : bool
        boolean flag to determine if the profile cares about imu
    insidePressure : bool
        boolean flag to determine if the profile cares about insidePressure
    batMonit : bool
        boolean flag to determine if the profile cares about batMonit
    

    Methods
    -------
    __validateConstructorAttributes(name, usbl, altimeter):
        Private method. Validates the attributes of the constructor
    setName(name):
        Sets the name of the profile
    getName():
        Returns the name of the profile
    setUsbl(usbl):
        Sets the usbl flag for the profile. If true, it will show USBL related plots.
    getUsbl():
        Returns the USBL status of the profile
    setAltimeter(altimeter):
        Sets the altimeter flag for the profile. If true, it will show altimeter related plots.
    getAltimeter():
        Returns the altimeter status of the profile
    deserializeClass(jsonData):
        Deserializes a JSON data into a Profile object
    deserializeFile(filePath):
        Deserializes a JSON file into a Profile object
    serializeClass():
        Serializes the Profile object into a JSON file
    serializeProfiles(profiles):
        Serializes a list or tuple of Profile objects into a JSON string
    """

    # TODO - Add more fields
    # TODO - Create default profiles
    # TODO - Delete Profiles from CAIS
    #           - Find way to ask if user is sure
    #           - Find way to ask for a password for deletion (store encrypted version of password?)
    # TODO - Add Profiles to CAIS
    # TODO - Update Profiles in CAIS

    ########################################
    ######     JSON Enconder Class    ######
    ########################################

    class ProfileEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__


    ########################################
    ######     public instance        ######
    ######          methods           ######
    ########################################

    def __init__(self, name, usbl=True, altimeter=True, depthCell=True,
                  gps=True, imu=True, insidePressure=True, batMonit=True,
                  thrusters=True, controlSurge=True,
                  overviewFilterDrUsbl=True, filterVsVirtualTarget=True,
                  overviewPf=True, crossTrackAlongTrack=True, Ax=True,
                  Ay=True, Az=True, current=True, errors=True, Gx=True,
                  Gy=True, Gz=True, Mx=True, My=True, Mz=True, speed=True,
                  temperature=True, actual_charge=True, altitude=True,
                  charging=True, equalize=True, latitude=True,
                  longitude=True, magAbs=True, magX=True, magY=True,
                  magZ=True, maxCell=True, maxTemp=True, measurementUSBLFixBearing=True,
                  measurementUSBLFixBearingRaw=True, measurementUSBLFixElevation=True,
                  measurementUSBLFixElevationRaw=True, measurementUSBLFixRange=True,
                  measurementUSBLFixSoundSpeed=True, measurementUSBLFixSourceID=True,
                  measurementUSBLFixTypeID=True, minCell=True, minTemp=True,
                  pitch=True, roll=True, voltage=True, yaw=True, pressure=True,
                  mode=True, numberPacks=True, recvBitRate=True, recvBitDestinationAddress=True,
                  recvDuration=True, recvIntegrity=True, recvMsgID=True,
                  recvPropagationTime=True, recvRelativeVelocity=True,
                  recvRSSI=True, recvSourceAddress=True, satellites=True,
                  sendBitRate=True, sendBitDestinationAddress=True,
                  sendDuration=True, sendIntegrity=True, sendMsgID=True,
                  sendPropagationTime=True, sendRelativeVelocity=True,
                  sendRSSI=True, sendSourceAddress=True, sendTypeID=True,
                  sensorsUSBLFixBearingVsBearingRaw=True,
                  sensorsUSBLFixElevationVsElevationRaw=True,
                  sensorsUSBLFixRange=True,
                  sensorsUSBLFixRangeVsBearingVsElevation=True,
                  sensorsUSBLFixSourceID=True, speedOverGround=True,
                  utcTime=True):
        """
        Creates a Profile object
        
        Parameters
        ----------
            name: str
                The name of the profile
            usbl: bool
                The USBL status of the profile. If true, it will show USBL related plots.
                (optional, default=True)
            altimeter: bool
                The altimeter status of the profile. If true, it will show altimeter related plots.
                (optional, default=True)
            depthCell: bool
                The depthCell status of the profile. If true, it will show depthCell related plots.
                (optional, default=True)
            gps: bool
                The gps status of the profile. If true, it will show gps related plots.
                (optional, default=True)
            imu: bool
                The imu status of the profile. If true, it will show imu related plots.
                (optional, default=True)
            insidePressure: bool
                The insidePressure status of the profile. If true, it will show insidePressure related plots.
                (optional, default=True)
            batMonit: bool
                The batMonit status of the profile. If true, it will show batMonit related plots.
                (optional, default=True)
        """
        try:
            self.__validateConstructorAttributes(name, usbl, altimeter,
                                                 depthCell, gps, imu,
                                                 insidePressure, batMonit, thrusters, 
                                                 controlSurge, overviewFilterDrUsbl, filterVsVirtualTarget,
                                                 overviewPf, crossTrackAlongTrack, Ax,
                                                 Ay, Az, current, errors, Gx,
                                                 Gy, Gz, Mx, My, Mz, speed,
                                                 temperature, actual_charge, altitude,
                                                 charging, equalize, latitude,
                                                 longitude, magAbs, magX, magY,
                                                 magZ, maxCell, maxTemp, measurementUSBLFixBearing,
                                                 measurementUSBLFixBearingRaw, measurementUSBLFixElevation,
                                                 measurementUSBLFixElevationRaw, measurementUSBLFixRange,
                                                 measurementUSBLFixSoundSpeed, measurementUSBLFixSourceID,
                                                 measurementUSBLFixTypeID, minCell, minTemp,
                                                 pitch, roll, voltage, yaw, pressure,
                                                 mode, numberPacks, recvBitRate, recvBitDestinationAddress,
                                                 recvDuration, recvIntegrity, recvMsgID,
                                                 recvPropagationTime, recvRelativeVelocity, recvRSSI,
                                                 recvSourceAddress, satellites, sendBitRate, sendBitDestinationAddress,
                                                 sendDuration, sendIntegrity, sendMsgID,
                                                 sendPropagationTime, sendRelativeVelocity, sendRSSI,
                                                 sendSourceAddress, sendTypeID, sensorsUSBLFixBearingVsBearingRaw,
                                                 sensorsUSBLFixElevationVsElevationRaw, sensorsUSBLFixRange,
                                                 sensorsUSBLFixRangeVsBearingVsElevation, sensorsUSBLFixSourceID,
                                                 speedOverGround, utcTime)
        except ValueError as valueError:
            raise valueError
        except TypeError as typeError:
            raise typeError
        
        self.setName(name)
        self.setUsbl(usbl)
        self.setAltimeter(altimeter)
        self.setBatMonit(batMonit)
        self.setInsidePressure(insidePressure)
        self.setImu(imu)
        self.setGps(gps)
        self.setDepthCell(depthCell)
        self.setThrusters(thrusters)
        self.setControlSurge(controlSurge)
        self.setFilterVsVirtualTarget(filterVsVirtualTarget)
        self.setCrossTrackAlongTrack(crossTrackAlongTrack)
        self.setAx(Ax)
        self.setAy(Ay)
        self.setAz(Az)
        self.setCurrent(current)
        self.setErrors(errors)
        self.setGx(Gx)
        self.setGy(Gy)
        self.setGz(Gz)
        self.setSpeed(speed)
        self.setTemperature(temperature)
        self.setActual_charge(actual_charge)
        self.setOverviewPf(overviewPf)
        self.setOverviewFilterDrUsbl(overviewFilterDrUsbl)
        self.setCharging(charging)
        self.setEqualize(equalize)
        self.setMx(Mx)
        self.setMy(My)
        self.setMz(Mz)
        self.setMagAbs(magAbs)
        self.setVoltage(voltage)
        self.setAltitude(altitude)
        self.setLatitude(latitude)
        self.setLongitude(longitude)
        self.setMagX(magX)
        self.setMagY(magY)
        self.setMagZ(magZ)
        self.setMaxCell(maxCell)
        self.setMaxTemp(maxTemp)
        self.setMeasurementUSBLFixBearing(measurementUSBLFixBearing)
        self.setMeasurementUSBLFixBearingRaw(measurementUSBLFixBearingRaw)
        self.setMeasurementUSBLFixElevation(measurementUSBLFixElevation)
        self.setMeasurementUSBLFixElevationRaw(measurementUSBLFixElevationRaw)
        self.setMeasurementUSBLFixRange(measurementUSBLFixRange)
        self.setMeasurementUSBLFixSoundSpeed(measurementUSBLFixSoundSpeed)
        self.setMeasurementUSBLFixSourceID(measurementUSBLFixSourceID)
        self.setMeasurementUSBLFixTypeID(measurementUSBLFixTypeID)
        self.setMinCell(minCell)
        self.setMinTemp(minTemp)
        self.setPitch(pitch)
        self.setRoll(roll)
        self.setYaw(yaw)
        self.setPressure(pressure)
        self.setMode(mode)
        self.setNumberPacks(numberPacks)
        self.setRecvBitRate(recvBitRate)
        self.setRecvBitDestinationAddress(recvBitDestinationAddress)
        self.setRecvDuration(recvDuration)
        self.setRecvIntegrity(recvIntegrity)
        self.setRecvMsgID(recvMsgID)
        self.setRecvPropagationTime(recvPropagationTime)
        self.setRecvRelativeVelocity(recvRelativeVelocity)
        self.setRecvRSSI(recvRSSI)
        self.setRecvSourceAddress(recvSourceAddress)
        self.setSatellites(satellites)
        self.setSendBitRate(sendBitRate)
        self.setSendBitDestinationAddress(sendBitDestinationAddress)
        self.setSendDuration(sendDuration)
        self.setSendIntegrity(sendIntegrity)
        self.setSendMsgID(sendMsgID)
        self.setSendPropagationTime(sendPropagationTime)
        self.setSendRelativeVelocity(sendRelativeVelocity)
        self.setSendRSSI(sendRSSI)
        self.setSendSourceAddress(sendSourceAddress)
        self.setSendTypeID(sendTypeID)
        self.setSensorsUSBLFixBearingVsBearingRaw(sensorsUSBLFixBearingVsBearingRaw)
        self.setSensorsUSBLFixElevationVsElevationRaw(sensorsUSBLFixElevationVsElevationRaw)
        self.setSensorsUSBLFixRange(sensorsUSBLFixRange)
        self.setSensorsUSBLFixRangeVsBearingVsElevation(sensorsUSBLFixRangeVsBearingVsElevation)
        self.setSensorsUSBLFixSourceID(sensorsUSBLFixSourceID)
        self.setSpeedOverGround(speedOverGround)
        self.setUtcTime(utcTime)


    ########################################
    ######     private methods        ######
    ########################################

    @classmethod
    def __validateConstructorAttributes(self, name, usbl, altimeter, depthCell, gps, imu, 
                                        insidePressure, batMonit, thrusters,
                                        controlSurge, overviewFilterDrUsbl, filterVsVirtualTarget,
                                        overviewPf, crossTrackAlongTrack, Ax, Ay, Az, current,
                                        errors, Gx, Gy, Gz, Mx, My, Mz, speed, temperature,
                                        actual_charge, altitude, charging, equalize, latitude,
                                        longitude, magAbs, magX, magY, magZ, maxCell, maxTemp,
                                        measurementUSBLFixBearing, measurementUSBLFixBearingRaw,
                                        measurementUSBLFixElevation, measurementUSBLFixElevationRaw,
                                        measurementUSBLFixRange, measurementUSBLFixSoundSpeed,
                                        measurementUSBLFixSourceID, measurementUSBLFixTypeID,
                                        minCell, minTemp, pitch, roll, voltage, yaw, pressure,
                                        mode, numberPacks, recvBitRate, recvBitDestinationAddress,
                                        recvDuration, recvIntegrity, recvMsgID, recvPropagationTime,
                                        recvRelativeVelocity, recvRSSI, recvSourceAddress, satellites,
                                        sendBitRate, sendBitDestinationAddress, sendDuration,
                                        sendIntegrity, sendMsgID, sendPropagationTime,
                                        sendRelativeVelocity, sendRSSI, sendSourceAddress, sendTypeID,
                                        sensorsUSBLFixBearingVsBearingRaw, sensorsUSBLFixElevationVsElevationRaw,
                                        sensorsUSBLFixRange, sensorsUSBLFixRangeVsBearingVsElevation,
                                        sensorsUSBLFixSourceID, speedOverGround, utcTime):
        """Validates the attributes of the constructor"""
        if (type(name) != str):
            raise TypeError("Name must be a string")
        elif (name == None or name == ""):
            raise ValueError("Name can't be None/Null or empty")
        if (type(usbl) != bool):
            raise TypeError("USBL must be a boolean")
        if (type(altimeter) != bool):
            raise TypeError("Altimeter must be a boolean")
        if (type(depthCell) != bool):
            raise TypeError("DepthCell must be a boolean")
        if (type(gps) != bool):
            raise TypeError("GPS must be a boolean")
        if (type(imu) != bool):
            raise TypeError("IMU must be a boolean")
        if (type(insidePressure) != bool):
            raise TypeError("InsidePressure must be a boolean")
        if (type(batMonit) != bool):
            raise TypeError("BatMonit must be a boolean")
        if (type(thrusters) != bool):
            raise TypeError("Thrusters must be a boolean")
        if (type(controlSurge) != bool):
            raise TypeError("ControlSurge must be a boolean")
        if (type(overviewFilterDrUsbl) != bool):
            raise TypeError("OverviewFilterDrUsbl must be a boolean")
        if (type(filterVsVirtualTarget) != bool):
            raise TypeError("FilterVsVirtualTarget must be a boolean")
        if (type(overviewPf) != bool):
            raise TypeError("OverviewPf must be a boolean")
        if (type(crossTrackAlongTrack) != bool):
            raise TypeError("CrossTrackAlongTrack must be a boolean")
        if (type(Ax) != bool):
            raise TypeError("Ax must be a boolean")
        if (type(Ay) != bool):
            raise TypeError("Ay must be a boolean")
        if (type(Az) != bool):
            raise TypeError("Az must be a boolean")
        if (type(current) != bool):
            raise TypeError("Current must be a boolean")
        if (type(errors) != bool):
            raise TypeError("Errors must be a boolean")
        if (type(Gx) != bool):
            raise TypeError("Gx must be a boolean")
        if (type(Gy) != bool):
            raise TypeError("Gy must be a boolean")
        if (type(Gz) != bool):
            raise TypeError("Gz must be a boolean")
        if (type(Mx) != bool):
            raise TypeError("Mx must be a boolean")
        if (type(My) != bool):
            raise TypeError("My must be a boolean")
        if (type(Mz) != bool):
            raise TypeError("Mz must be a boolean")
        if (type(speed) != bool):
            raise TypeError("Speed must be a boolean")
        if (type(temperature) != bool):
            raise TypeError("Temperature must be a boolean")
        if (type(actual_charge) != bool):
            raise TypeError("Actual_charge must be a boolean")
        if (type(altitude) != bool):
            raise TypeError("Altitude must be a boolean")
        if (type(charging) != bool):
            raise TypeError("Charging must be a boolean")
        if (type(equalize) != bool):
            raise TypeError("Equalize must be a boolean")
        if (type(latitude) != bool):
            raise TypeError("Latitude must be a boolean")
        if (type(longitude) != bool):
            raise TypeError("Longitude must be a boolean")
        if (type(magAbs) != bool):
            raise TypeError("MagAbs must be a boolean")
        if (type(magX) != bool):
            raise TypeError("MagX must be a boolean")
        if (type(magY) != bool):
            raise TypeError("MagY must be a boolean")
        if (type(magZ) != bool):
            raise TypeError("MagZ must be a boolean")
        if (type(maxCell) != bool):
            raise TypeError("MaxCell must be a boolean")
        if (type(maxTemp) != bool):
            raise TypeError("MaxTemp must be a boolean")
        if (type(measurementUSBLFixBearing) != bool):
            raise TypeError("MeasurementUSBLFixBearing must be a boolean")
        if (type(measurementUSBLFixBearingRaw) != bool):
            raise TypeError("MeasurementUSBLFixBearingRaw must be a boolean")
        if (type(measurementUSBLFixElevation) != bool):
            raise TypeError("MeasurementUSBLFixElevation must be a boolean")
        if (type(measurementUSBLFixElevationRaw) != bool):
            raise TypeError("MeasurementUSBLFixElevationRaw must be a boolean")
        if (type(measurementUSBLFixRange) != bool):
            raise TypeError("MeasurementUSBLFixRange must be a boolean")
        if (type(measurementUSBLFixSourceID) != bool):
            raise TypeError("MeasurementUSBLFixSourceID must be a boolean")
        if (type(minCell) != bool):
            raise TypeError("MinCell must be a boolean")
        if (type(minTemp) != bool):
            raise TypeError("MinTemp must be a boolean")

    ########################################
    ######     normal  methods        ######
    ########################################

    def setControlSurge(self, controlSurge):
        """Sets the controlSurge flag for the profile. If true, it will show controlSurge related plots.
        
        Parameters
        ----------
            controlSurge: bool
                The controlSurge status of the profile. If true, it will show controlSurge related plots."""
        if (type(controlSurge) != bool):
            raise TypeError("controlSurge must be a boolean")

        self.controlSurge = controlSurge

    
    def getControlSurge(self):
        """Returns the controlSurge flag for the profile. If true, it will show controlSurge related plots.
        
        Returns
        -------
            bool
                The controlSurge status of the profile. If true, it will show controlSurge related plots."""
        return self.controlSurge
    

    def setCrossTrackAlongTrack(self, crossTrackAlongTrack):
        """Sets the crossTrackAlongTrack flag for the profile. If true, it will show crossTrackAlongTrack related plots.
        
        Parameters
        ----------
            crossTrackAlongTrack: bool
                The crossTrackAlongTrack status of the profile. If true, it will show crossTrackAlongTrack related plots."""
        if (type(crossTrackAlongTrack) != bool):
            raise TypeError("crossTrackAlongTrack must be a boolean")

        self.crossTrackAlongTrack = crossTrackAlongTrack


    def getCrossTrackAlongTrack(self):
        """Returns the crossTrackAlongTrack flag for the profile. If true, it will show crossTrackAlongTrack related plots.
        
        Returns
        -------
            bool
                The crossTrackAlongTrack status of the profile. If true, it will show crossTrackAlongTrack related plots."""
        return self.crossTrackAlongTrack
    

    def setFilterVsVirtualTarget(self, filterVsVirtualTarget):
        """Sets the filterVsVirtualTarget flag for the profile. If true, it will show filterVsVirtualTarget related plots.
        
        Parameters
        ----------
            filterVsVirtualTarget: bool
                The filterVsVirtualTarget status of the profile. If true, it will show filterVsVirtualTarget related plots."""
        if (type(filterVsVirtualTarget) != bool):
            raise TypeError("filterVsVirtualTarget must be a boolean")

        self.filterVsVirtualTarget = filterVsVirtualTarget


    def getFilterVsVirtualTarget(self):
        """Returns the filterVsVirtualTarget flag for the profile. If true, it will show filterVsVirtualTarget related plots.
        
        Returns
        -------
            bool
                The filterVsVirtualTarget status of the profile. If true, it will show filterVsVirtualTarget related plots."""
        return self.filterVsVirtualTarget
    
    def setGy(self, Gy):
        """Sets the Gy flag for the profile. If true, it will show Gy related plots.
        
        Parameters
        ----------
            Gy: bool
                The Gy status of the profile. If true, it will show Gy related plots."""
        if (type(Gy) != bool):
            raise TypeError("Gy must be a boolean")

        self.Gy = Gy

    
    def getGy(self):
        """Returns the Gy flag for the profile. If true, it will show Gy related plots.
        
        Returns
        -------
            bool
                The Gy status of the profile. If true, it will show Gy related plots."""
        return self.Gy
    

    def setGz(self, Gz):
        """Sets the Gz flag for the profile. If true, it will show Gz related plots.
        
        Parameters
        ----------
            Gz: bool
                The Gz status of the profile. If true, it will show Gz related plots."""
        if (type(Gz) != bool):
            raise TypeError("Gz must be a boolean")

        self.Gz = Gz

    
    def getGz(self):
        """Returns the Gz flag for the profile. If true, it will show Gz related plots.
        
        Returns
        -------
            bool
                The Gz status of the profile. If true, it will show Gz related plots."""
        return self.Gz
    

    def setMagX(self, magX):
        """Sets the magX flag for the profile. If true, it will show magX related plots.
        
        Parameters
        ----------
            magX: bool
                The magX status of the profile. If true, it will show magX related plots."""
        if (type(magX) != bool):
            raise TypeError("MagX must be a boolean")

        self.magX = magX

    
    def getMagX(self):
        """Returns the magX flag for the profile. If true, it will show magX related plots.
        
        Returns
        -------
            bool
                The magX status of the profile. If true, it will show magX related plots."""
        return self.magX
    

    def setMagY(self, magY):
        """Sets the magY flag for the profile. If true, it will show magY related plots.
        
        Parameters
        ----------
            magY: bool
                The magY status of the profile. If true, it will show magY related plots."""
        if (type(magY) != bool):
            raise TypeError("MagY must be a boolean")

        self.magY = magY

    
    def getMagY(self):
        """Returns the magY flag for the profile. If true, it will show magY related plots.
        
        Returns
        -------
            bool
                The magY status of the profile. If true, it will show magY related plots."""
        return self.magY
    

    def setMagZ(self, magZ):
        """Sets the magZ flag for the profile. If true, it will show magZ related plots.
        
        Parameters
        ----------
            magZ: bool
                The magZ status of the profile. If true, it will show magZ related plots."""
        if (type(magZ) != bool):
            raise TypeError("MagZ must be a boolean")

        self.magZ = magZ


    def getMagZ(self):
        """Returns the magZ flag for the profile. If true, it will show magZ related plots.
        
        Returns
        -------
            bool
                The magZ status of the profile. If true, it will show magZ related plots."""
        return self.magZ
    

    def setPitch(self, pitch):
        """Sets the pitch flag for the profile. If true, it will show pitch related plots.
        
        Parameters
        ----------
            pitch: bool
                The pitch status of the profile. If true, it will show pitch related plots."""
        if (type(pitch) != bool):
            raise TypeError("Pitch must be a boolean")

        self.pitch = pitch


    def getPitch(self):
        """Returns the pitch flag for the profile. If true, it will show pitch related plots.
        
        Returns
        -------
            bool
                The pitch status of the profile. If true, it will show pitch related plots."""
        return self.pitch
    

    def setRoll(self, roll):
        """Sets the roll flag for the profile. If true, it will show roll related plots.
        
        Parameters
        ----------
            roll: bool
                The roll status of the profile. If true, it will show roll related plots."""
        if (type(roll) != bool):
            raise TypeError("Roll must be a boolean")

        self.roll = roll

    
    def getRoll(self):
        """Returns the roll flag for the profile. If true, it will show roll related plots.
        
        Returns
        -------
            bool
                The roll status of the profile. If true, it will show roll related plots."""
        return self.roll
    

    def setYaw(self, yaw):
        """Sets the yaw flag for the profile. If true, it will show yaw related plots.
        
        Parameters
        ----------
            yaw: bool
                The yaw status of the profile. If true, it will show yaw related plots."""
        if (type(yaw) != bool):
            raise TypeError("Yaw must be a boolean")

        self.yaw = yaw

    
    def getYaw(self):
        """Returns the yaw flag for the profile. If true, it will show yaw related plots.
        
        Returns
        -------
            bool
                The yaw status of the profile. If true, it will show yaw related plots."""
        return self.yaw
    

    def setDepth(self, depth):
        """Sets the depth flag for the profile. If true, it will show depth related plots.
        
        Parameters
        ----------
            depth: bool
                The depth status of the profile. If true, it will show depth related plots."""
        if (type(depth) != bool):
            raise TypeError("Depth must be a boolean")

        self.depth = depth


    def getDepth(self):
        """Returns the depth flag for the profile. If true, it will show depth related plots.
        
        Returns
        -------
            bool
                The depth status of the profile. If true, it will show depth related plots."""
        return self.depth
    

    def setTemperature(self, temperature):
        """Sets the temperature flag for the profile. If true, it will show temperature related plots.
        
        Parameters
        ----------
            temperature: bool
                The temperature status of the profile. If true, it will show temperature related plots."""
        if (type(temperature) != bool):
            raise TypeError("Temperature must be a boolean")

        self.temperature = temperature


    def getTemperature(self):
        """Returns the temperature flag for the profile. If true, it will show temperature related plots.
        
        Returns
        -------
            bool
                The temperature status of the profile. If true, it will show temperature related plots."""
        return self.temperature
    

    def setPressure(self, pressure):
        """Sets the pressure flag for the profile. If true, it will show pressure related plots.
        
        Parameters
        ----------
            pressure: bool
                The pressure status of the profile. If true, it will show pressure related plots."""
        if (type(pressure) != bool):
            raise TypeError("Pressure must be a boolean")

        self.pressure = pressure


    def getPressure(self):
        """Returns the pressure flag for the profile. If true, it will show pressure related plots.
        
        Returns
        -------
            bool
                The pressure status of the profile. If true, it will show pressure related plots."""
        return self.pressure
    

    def setAltitude(self, altitude):
        """Sets the altitude flag for the profile. If true, it will show altitude related plots.
        
        Parameters
        ----------
            altitude: bool
                The altitude status of the profile. If true, it will show altitude related plots."""
        if (type(altitude) != bool):
            raise TypeError("Altitude must be a boolean")

        self.altitude = altitude


    def getAltitude(self):
        """Returns the altitude flag for the profile. If true, it will show altitude related plots.
        
        Returns
        -------
            bool
                The altitude status of the profile. If true, it will show altitude related plots."""
        return self.altitude
    

    def setLatitude(self, latitude):
        """Sets the latitude flag for the profile. If true, it will show latitude related plots.
        
        Parameters
        ----------
            latitude: bool
                The latitude status of the profile. If true, it will show latitude related plots."""
        if (type(latitude) != bool):
            raise TypeError("Latitude must be a boolean")

        self.latitude = latitude


    def getLatitude(self):
        """Returns the latitude flag for the profile. If true, it will show latitude related plots.
        
        Returns
        -------
            bool
                The latitude status of the profile. If true, it will show latitude related plots."""
        return self.latitude
    

    def setLongitude(self, longitude):
        """Sets the longitude flag for the profile. If true, it will show longitude related plots.
        
        Parameters
        ----------
            longitude: bool
                The longitude status of the profile. If true, it will show longitude related plots."""
        if (type(longitude) != bool):
            raise TypeError("Longitude must be a boolean")

        self.longitude = longitude


    def getLongitude(self):
        """Returns the longitude flag for the profile. If true, it will show longitude related plots.
        
        Returns
        -------
            bool
                The longitude status of the profile. If true, it will show longitude related plots."""
        return self.longitude
    

    def setSpeed(self, speed):
        """Sets the speed flag for the profile. If true, it will show speed related plots.
        
        Parameters
        ----------
            speed: bool
                The speed status of the profile. If true, it will show speed related plots."""
        if (type(speed) != bool):
            raise TypeError("Speed must be a boolean")

        self.speed = speed


    def getSpeed(self):
        """Returns the speed flag for the profile. If true, it will show speed related plots.
        
        Returns
        -------
            bool
                The speed status of the profile. If true, it will show speed related plots."""
        return self.speed
    

    def setCourse(self, course):
        """Sets the course flag for the profile. If true, it will show course related plots.
        
        Parameters
        ----------
            course: bool
                The course status of the profile. If true, it will show course related plots."""
        if (type(course) != bool):
            raise TypeError("Course must be a boolean")

        self.course = course


    def getCourse(self):
        """Returns the course flag for the profile. If true, it will show course related plots.
        
        Returns
        -------
            bool
                The course status of the profile. If true, it will show course related plots."""
        return self.course
    

    def setPitch(self, pitch):
        """Sets the pitch flag for the profile. If true, it will show pitch related plots.
        
        Parameters
        ----------
            pitch: bool
                The pitch status of the profile. If true, it will show pitch related plots."""
        if (type(pitch) != bool):
            raise TypeError("Pitch must be a boolean")

        self.pitch = pitch


    def getPitch(self):
        """Returns the pitch flag for the profile. If true, it will show pitch related plots.
        
        Returns
        -------
            bool
                The pitch status of the profile. If true, it will show pitch related plots."""
        return self.pitch
    

    def setRoll(self, roll):
        """Sets the roll flag for the profile. If true, it will show roll related plots.
        
        Parameters
        ----------
            roll: bool
                The roll status of the profile. If true, it will show roll related plots."""
        if (type(roll) != bool):
            raise TypeError("Roll must be a boolean")

        self.roll = roll


    def setAx(self, Ax):
        """Sets the Ax flag for the profile. If true, it will show Ax related plots.
        
        Parameters
        ----------
            Ax: bool
                The Ax status of the profile. If true, it will show Ax related plots."""
        if (type(Ax) != bool):
            raise TypeError("Ax must be a boolean")

        self.Ax = Ax

    
    def getAx(self):
        """Returns the Ax flag for the profile. If true, it will show Ax related plots.
        
        Returns
        -------
            bool
                The Ax status of the profile. If true, it will show Ax related plots."""
        return self.Ax
    

    def setAy(self, Ay):
        """Sets the Ay flag for the profile. If true, it will show Ay related plots.
        
        Parameters
        ----------
            Ay: bool
                The Ay status of the profile. If true, it will show Ay related plots."""
        if (type(Ay) != bool):
            raise TypeError("Ay must be a boolean")

        self.Ay = Ay

    
    def getAy(self):
        """Returns the Ay flag for the profile. If true, it will show Ay related plots.
        
        Returns
        -------
            bool
                The Ay status of the profile. If true, it will show Ay related plots."""
        return self.Ay
    

    def setAz(self, Az):
        """Sets the Az flag for the profile. If true, it will show Az related plots.
        
        Parameters
        ----------
            Az: bool
                The Az status of the profile. If true, it will show Az related plots."""
        if (type(Az) != bool):
            raise TypeError("Az must be a boolean")

        self.Az = Az


    def getAz(self):
        """Returns the Az flag for the profile. If true, it will show Az related plots.
        
        Returns
        -------
            bool
                The Az status of the profile. If true, it will show Az related plots."""
        return self.Az
    

    def setCurrent(self, current):
        """Sets the current flag for the profile. If true, it will show current related plots.
        
        Parameters
        ----------
            current: bool
                The current status of the profile. If true, it will show current related plots."""
        if (type(current) != bool):
            raise TypeError("Current must be a boolean")

        self.current = current

    
    def getCurrent(self):
        """Returns the current flag for the profile. If true, it will show current related plots.
        
        Returns
        -------
            bool
                The current status of the profile. If true, it will show current related plots."""
        return self.current
    

    def setErrors(self, errors):
        """Sets the errors flag for the profile. If true, it will show errors related plots.
        
        Parameters
        ----------
            errors: bool
                The errors status of the profile. If true, it will show errors related plots."""
        if (type(errors) != bool):
            raise TypeError("Errors must be a boolean")

        self.errors = errors


    def getErrors(self):
        """Returns the errors flag for the profile. If true, it will show errors related plots.
        
        Returns
        -------
            bool
                The errors status of the profile. If true, it will show errors related plots."""
        return self.errors
    

    def setGx(self, Gx):
        """Sets the Gx flag for the profile. If true, it will show Gx related plots.
        
        Parameters
        ----------
            Gx: bool
                The Gx status of the profile. If true, it will show Gx related plots."""
        if (type(Gx) != bool):
            raise TypeError("Gx must be a boolean")

        self.Gx = Gx


    def getGx(self):
        """Returns the Gx flag for the profile. If true, it will show Gx related plots.
        
        Returns
        -------
            bool
                The Gx status of the profile. If true, it will show Gx related plots."""
        return self.Gx
    

    def setGy(self, Gy):
        """Sets the Gy flag for the profile. If true, it will show Gy related plots.
        
        Parameters
        ----------
            Gy: bool
                The Gy status of the profile. If true, it will show Gy related plots."""
        if (type(Gy) != bool):
            raise TypeError("Gy must be a boolean")

        self.Gy = Gy


    def getRoll(self):
        """Returns the roll flag for the profile. If true, it will show roll related plots.
        
        Returns
        -------
            bool
                The roll status of the profile. If true, it will show roll related plots."""
        return self.roll


    def setName(self, name):
        """Sets the name of the profile
        
        Parameters
        ----------
            name: str
                The name of the profile"""
        if (type(name) != str):
            raise TypeError("Name must be a string")
        elif (name == None or name == ""):
            raise ValueError("Name can't be None/Null or empty")

        self.name = name


    def getName(self):
        """Returns the name of the profile
        
        Returns
        -------
            str
                The name of the profile"""
        return self.name
    

    def setThrusters(self, thrusters):
        """Sets the thrusters flag for the profile. If true, it will show thrusters related plots.
        
        Parameters
        ----------
            thrusters: bool
                The thrusters status of the profile. If true, it will show thrusters related plots."""
        if (type(thrusters) != bool):
            raise TypeError("thrusters must be a boolean")

        self.thrusters = thrusters


    def getThrusters(self):
        """Returns the thrusters status of the profile
        
        Returns
        -------
            bool
                The thrusters status of the profile"""
        return self.thrusters


    def setBatMonit(self, batMonit):
        """Sets the batMonit flag for the profile. If true, it will show batMonit related plots.
        
        Parameters
        ----------
            batMonit: bool
                The batMonit status of the profile. If true, it will show batMonit related plots."""
        if (type(batMonit) != bool):
            raise TypeError("batMonit must be a boolean")

        self.batMonit = batMonit


    def getBatMonit(self):
        """Returns the batMonit status of the profile
        
        Returns
        -------
            bool
                The batMonit status of the profile"""
        return self.batMonit
    

    def setInsidePressure(self, insidePressure):
        """Sets the insidePressure flag for the profile. If true, it will show insidePressure related plots.
        
        Parameters
        ----------
            insidePressure: bool
                The insidePressure status of the profile. If true, it will show insidePressure related plots."""
        if (type(insidePressure) != bool):
            raise TypeError("insidePressure must be a boolean")

        self.insidePressure = insidePressure


    def getInsidePressure(self):
        """Returns the insidePressure status of the profile
        
        Returns
        -------
            bool
                The insidePressure status of the profile"""
        return self.insidePressure
    

    def setImu(self, imu):
        """Sets the imu flag for the profile. If true, it will show imu related plots.
        
        Parameters
        ----------
            imu: bool
                The imu status of the profile. If true, it will show imu related plots."""
        if (type(imu) != bool):
            raise TypeError("imu must be a boolean")

        self.imu = imu


    def getImu(self):
        """Returns the imu status of the profile
        
        Returns
        -------
            bool
                The imu status of the profile"""
        return self.imu
    

    def setGps(self, gps):
        """Sets the gps flag for the profile. If true, it will show gps related plots.
        
        Parameters
        ----------
            gps: bool
                The gps status of the profile. If true, it will show gps related plots."""
        if (type(gps) != bool):
            raise TypeError("gps must be a boolean")

        self.gps = gps


    def getGps(self):
        """Returns the gps status of the profile
        
        Returns
        -------
            bool
                The gps status of the profile"""
        return self.gps
    

    def setDepthCell(self, depthCell):
        """Sets the depthCell flag for the profile. If true, it will show depthCell related plots.
        
        Parameters
        ----------
            depthCell: bool
                The depthCell status of the profile. If true, it will show depthCell related plots."""
        if (type(depthCell) != bool):
            raise TypeError("depthCell must be a boolean")

        self.depthCell = depthCell


    def getDepthCell(self):
        """Returns the depthCell status of the profile
        
        Returns
        -------
            bool
                The depthCell status of the profile"""
        return self.depthCell
     
    
    def setUsbl(self, usbl):
        """Sets the usbl flag for the profile. If true, it will show USBL related plots.
        
        Parameters
        ----------
            usbl: bool
                The USBL status of the profile. If true, it will show USBL related plots."""
        if (type(usbl) != bool):
            raise TypeError("USBL must be a boolean")

        self.usbl = usbl

    
    def getUsbl(self):
        """Returns the USBL status of the profile
        
        Returns
        -------
            bool
                The USBL status of the profile"""
        return self.usbl

    
    def setAltimeter(self, altimeter):
        """Sets the altimeter flag for the profile. If true, it will show altimeter related plots.
        
        Parameters
        ----------
            altimeter: bool
                The altimeter status of the profile. If true, it will show altimeter related plots."""
        if (type(altimeter) != bool):
            raise TypeError("Altimeter must be a boolean")

        self.altimeter = altimeter


    def getAltimeter(self):
        """Returns the altimeter status of the profile
        
        Returns
        -------
            bool
                The altimeter status of the profile"""
        return self.altimeter
    

    def setMaxCell(self, maxCell):
        """Sets the maxCell flag for the profile. If true, it will show maxCell related plots.
        
        Parameters
        ----------
            maxCell: bool
                The maxCell status of the profile. If true, it will show maxCell related plots."""
        if (type(maxCell) != bool):
            raise TypeError("maxCell must be a boolean")

        self.maxCell = maxCell

    
    def getMaxCell(self):
        """Returns the maxCell status of the profile
        
        Returns
        -------
            bool
                The maxCell status of the profile"""
        return self.maxCell
    

    def setMaxTemp(self, maxTemp):
        """Sets the maxTemp flag for the profile. If true, it will show maxTemp related plots.
        
        Parameters
        ----------
            maxTemp: bool
                The maxTemp status of the profile. If true, it will show maxTemp related plots."""
        if (type(maxTemp) != bool):
            raise TypeError("maxTemp must be a boolean")

        self.maxTemp = maxTemp


    def getMaxTemp(self):
        """Returns the maxTemp status of the profile
        
        Returns
        -------
            bool
                The maxTemp status of the profile"""
        return self.maxTemp
    

    def setMeasurementUSBLFixBearing(self, measurementUSBLFixBearing):
        """Sets the measurementUSBLFixBearing flag for the profile. If true, it will show measurementUSBLFixBearing related plots.
        
        Parameters
        ----------
            measurementUSBLFixBearing: bool
                The measurementUSBLFixBearing status of the profile. If true, it will show measurementUSBLFixBearing related plots."""
        if (type(measurementUSBLFixBearing) != bool):
            raise TypeError("measurementUSBLFixBearing must be a boolean")

        self.measurementUSBLFixBearing = measurementUSBLFixBearing


    def getMeasurementUSBLFixBearing(self):
        """Returns the measurementUSBLFixBearing status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixBearing status of the profile"""
        return self.measurementUSBLFixBearing
    

    def setMeasurementUSBLFixBearingRaw(self, measurementUSBLFixBearingRaw):
        """Sets the measurementUSBLFixBearingRaw flag for the profile. If true, it will show measurementUSBLFixBearingRaw related plots.
        
        Parameters
        ----------
            measurementUSBLFixBearingRaw: bool
                The measurementUSBLFixBearingRaw status of the profile. If true, it will show measurementUSBLFixBearingRaw related plots."""
        if (type(measurementUSBLFixBearingRaw) != bool):
            raise TypeError("measurementUSBLFixBearingRaw must be a boolean")

        self.measurementUSBLFixBearingRaw = measurementUSBLFixBearingRaw


    def getMeasurementUSBLFixBearingRaw(self):
        """Returns the measurementUSBLFixBearingRaw status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixBearingRaw status of the profile"""
        return self.measurementUSBLFixBearingRaw
    

    def setMeasurementUSBLFixElevation(self, measurementUSBLFixElevation):
        """Sets the measurementUSBLFixElevation flag for the profile. If true, it will show measurementUSBLFixElevation related plots.
        
        Parameters
        ----------
            measurementUSBLFixElevation: bool
                The measurementUSBLFixElevation status of the profile. If true, it will show measurementUSBLFixElevation related plots."""
        if (type(measurementUSBLFixElevation) != bool):
            raise TypeError("measurementUSBLFixElevation must be a boolean")

        self.measurementUSBLFixElevation = measurementUSBLFixElevation


    def getMeasurementUSBLFixElevation(self):
        """Returns the measurementUSBLFixElevation status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixElevation status of the profile"""
        return self.measurementUSBLFixElevation
    

    def setMeasurementUSBLFixElevationRaw(self, measurementUSBLFixElevationRaw):
        """Sets the measurementUSBLFixElevationRaw flag for the profile. If true, it will show measurementUSBLFixElevationRaw related plots.
        
        Parameters
        ----------
            measurementUSBLFixElevationRaw: bool
                The measurementUSBLFixElevationRaw status of the profile. If true, it will show measurementUSBLFixElevationRaw related plots."""
        if (type(measurementUSBLFixElevationRaw) != bool):
            raise TypeError("measurementUSBLFixElevationRaw must be a boolean")

        self.measurementUSBLFixElevationRaw = measurementUSBLFixElevationRaw


    def getMeasurementUSBLFixElevationRaw(self):
        """Returns the measurementUSBLFixElevationRaw status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixElevationRaw status of the profile"""
        return self.measurementUSBLFixElevationRaw
    

    def setMeasurementUSBLFixRange(self, measurementUSBLFixRange):
        """Sets the measurementUSBLFixRange flag for the profile. If true, it will show measurementUSBLFixRange related plots.
        
        Parameters
        ----------
            measurementUSBLFixRange: bool
                The measurementUSBLFixRange status of the profile. If true, it will show measurementUSBLFixRange related plots."""
        if (type(measurementUSBLFixRange) != bool):
            raise TypeError("measurementUSBLFixRange must be a boolean")

        self.measurementUSBLFixRange = measurementUSBLFixRange


    def getMeasurementUSBLFixRange(self):
        """Returns the measurementUSBLFixRange status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixRange status of the profile"""
        return self.measurementUSBLFixRange
    

    def setMeasurementUSBLFixSoundSpeed(self, measurementUSBLFixSoundSpeed):
        """Sets the measurementUSBLFixSoundSpeed flag for the profile. If true, it will show measurementUSBLFixSoundSpeed related plots.
        
        Parameters
        ----------
            measurementUSBLFixSoundSpeed: bool
                The measurementUSBLFixSoundSpeed status of the profile. If true, it will show measurementUSBLFixSoundSpeed related plots."""
        if (type(measurementUSBLFixSoundSpeed) != bool):
            raise TypeError("measurementUSBLFixSoundSpeed must be a boolean")

        self.measurementUSBLFixSoundSpeed = measurementUSBLFixSoundSpeed

    
    def getMeasurementUSBLFixSoundSpeed(self):
        """Returns the measurementUSBLFixSoundSpeed status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixSoundSpeed status of the profile"""
        return self.measurementUSBLFixSoundSpeed
    

    def setMeasurementUSBLFixSourceID(self, measurementUSBLFixSourceID):
        """Sets the measurementUSBLFixSourceID flag for the profile. If true, it will show measurementUSBLFixSourceID related plots.
        
        Parameters
        ----------
            measurementUSBLFixSourceID: bool
                The measurementUSBLFixSourceID status of the profile. If true, it will show measurementUSBLFixSourceID related plots."""
        if (type(measurementUSBLFixSourceID) != bool):
            raise TypeError("measurementUSBLFixSourceID must be a boolean")

        self.measurementUSBLFixSourceID = measurementUSBLFixSourceID


    def getMeasurementUSBLFixSourceID(self):
        """Returns the measurementUSBLFixSourceID status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixSourceID status of the profile"""
        return self.measurementUSBLFixSourceID
    

    def setMeasurementUSBLFixTypeID(self, measurementUSBLFixTypeID):
        """Sets the measurementUSBLFixTypeID flag for the profile. If true, it will show measurementUSBLFixTypeID related plots.
        
        Parameters
        ----------
            measurementUSBLFixTypeID: bool
                The measurementUSBLFixTypeID status of the profile. If true, it will show measurementUSBLFixTypeID related plots."""
        if (type(measurementUSBLFixTypeID) != bool):
            raise TypeError("measurementUSBLFixTypeID must be a boolean")

        self.measurementUSBLFixTypeID = measurementUSBLFixTypeID


    def getMeasurementUSBLFixTypeID(self):
        """Returns the measurementUSBLFixTypeID status of the profile
        
        Returns
        -------
            bool
                The measurementUSBLFixTypeID status of the profile"""
        return self.measurementUSBLFixTypeID
    

    def setMinCell(self, minCell):
        """Sets the minCell flag for the profile. If true, it will show minCell related plots.
        
        Parameters
        ----------
            minCell: bool
                The minCell status of the profile. If true, it will show minCell related plots."""
        if (type(minCell) != bool):
            raise TypeError("minCell must be a boolean")

        self.minCell = minCell


    def getMinCell(self):
        """Returns the minCell status of the profile
        
        Returns
        -------
            bool
                The minCell status of the profile"""
        return self.minCell
    

    def setMinTemp(self, minTemp):
        """Sets the minTemp flag for the profile. If true, it will show minTemp related plots.
        
        Parameters
        ----------
            minTemp: bool
                The minTemp status of the profile. If true, it will show minTemp related plots."""
        if (type(minTemp) != bool):
            raise TypeError("minTemp must be a boolean")

        self.minTemp = minTemp


    def getMinTemp(self):
        """Returns the minTemp status of the profile
        
        Returns
        -------
            bool
                The minTemp status of the profile"""
        return self.minTemp
    

    def setMode(self, mode):
        """Sets the mode flag for the profile. If true, it will show mode related plots.
        
        Parameters
        ----------
            mode: bool
                The mode status of the profile. If true, it will show mode related plots."""
        if (type(mode) != bool):
            raise TypeError("mode must be a boolean")

        self.mode = mode


    def getMode(self):
        """Returns the mode status of the profile
        
        Returns
        -------
            bool
                The mode status of the profile"""
        return self.mode
    

    def setNumberPacks(self, numberPacks):
        """Sets the numberPacks flag for the profile. If true, it will show numberPacks related plots.
        
        Parameters
        ----------
            numberPacks: bool
                The numberPacks status of the profile. If true, it will show numberPacks related plots."""
        if (type(numberPacks) != bool):
            raise TypeError("numberPacks must be a boolean")

        self.numberPacks = numberPacks


    def getNumberPacks(self):
        """Returns the numberPacks status of the profile
        
        Returns
        -------
            bool
                The numberPacks status of the profile"""
        return self.numberPacks
    

    def setRecvBitRate(self, recvBitRate):
        """Sets the recvBitRate flag for the profile. If true, it will show recvBitRate related plots.
        
        Parameters
        ----------
            recvBitRate: bool
                The recvBitRate status of the profile. If true, it will show recvBitRate related plots."""
        if (type(recvBitRate) != bool):
            raise TypeError("recvBitRate must be a boolean")

        self.recvBitRate = recvBitRate


    def getRecvBitRate(self):
        """Returns the recvBitRate status of the profile
        
        Returns
        -------
            bool
                The recvBitRate status of the profile"""
        return self.recvBitRate
    

    def setRecvBitDestinationAddress(self, recvBitDestinationAddress):
        """Sets the recvBitDestinationAddress flag for the profile. If true, it will show recvBitDestinationAddress related plots.
        
        Parameters
        ----------
            recvBitDestinationAddress: bool
                The recvBitDestinationAddress status of the profile. If true, it will show recvBitDestinationAddress related plots."""
        if (type(recvBitDestinationAddress) != bool):
            raise TypeError("recvBitDestinationAddress must be a boolean")

        self.recvBitDestinationAddress = recvBitDestinationAddress


    def getRecvBitDestinationAddress(self):
        """Returns the recvBitDestinationAddress status of the profile
        
        Returns
        -------
            bool
                The recvBitDestinationAddress status of the profile"""
        return self.recvBitDestinationAddress
    

    def setRecvDuration(self, recvDuration):
        """Sets the recvDuration flag for the profile. If true, it will show recvDuration related plots.
        
        Parameters
        ----------
            recvDuration: bool
                The recvDuration status of the profile. If true, it will show recvDuration related plots."""
        if (type(recvDuration) != bool):
            raise TypeError("recvDuration must be a boolean")

        self.recvDuration = recvDuration


    def getRecvDuration(self):
        """Returns the recvDuration status of the profile
        
        Returns
        -------
            bool
                The recvDuration status of the profile"""
        return self.recvDuration
    

    def setRecvIntegrity(self, recvIntegrity):
        """Sets the recvIntegrity flag for the profile. If true, it will show recvIntegrity related plots.
        
        Parameters
        ----------
            recvIntegrity: bool
                The recvIntegrity status of the profile. If true, it will show recvIntegrity related plots."""
        if (type(recvIntegrity) != bool):
            raise TypeError("recvIntegrity must be a boolean")

        self.recvIntegrity = recvIntegrity


    def getRecvIntegrity(self):
        """Returns the recvIntegrity status of the profile
        
        Returns
        -------
            bool
                The recvIntegrity status of the profile"""
        return self.recvIntegrity
    

    def setRecvMsgID(self, recvMsgID):
        """Sets the recvMsgID flag for the profile. If true, it will show recvMsgID related plots.
        
        Parameters
        ----------
            recvMsgID: bool
                The recvMsgID status of the profile. If true, it will show recvMsgID related plots."""
        if (type(recvMsgID) != bool):
            raise TypeError("recvMsgID must be a boolean")

        self.recvMsgID = recvMsgID


    def getRecvMsgID(self):
        """Returns the recvMsgID status of the profile
        
        Returns
        -------
            bool
                The recvMsgID status of the profile"""
        return self.recvMsgID
    

    def setRecvPropagationTime(self, recvPropagationTime):
        """Sets the recvPropagationTime flag for the profile. If true, it will show recvPropagationTime related plots.
        
        Parameters
        ----------
            recvPropagationTime: bool
                The recvPropagationTime status of the profile. If true, it will show recvPropagationTime related plots."""
        if (type(recvPropagationTime) != bool):
            raise TypeError("recvPropagationTime must be a boolean")

        self.recvPropagationTime = recvPropagationTime


    def getRecvPropagationTime(self):
        """Returns the recvPropagationTime status of the profile
        
        Returns
        -------
            bool
                The recvPropagationTime status of the profile"""
        return self.recvPropagationTime
    

    def setRecvRelativeVelocity(self, recvRelativeVelocity):
        """Sets the recvRelativeVelocity flag for the profile. If true, it will show recvRelativeVelocity related plots.
        
        Parameters
        ----------
            recvRelativeVelocity: bool
                The recvRelativeVelocity status of the profile. If true, it will show recvRelativeVelocity related plots."""
        if (type(recvRelativeVelocity) != bool):
            raise TypeError("recvRelativeVelocity must be a boolean")

        self.recvRelativeVelocity = recvRelativeVelocity


    def getRecvRelativeVelocity(self):
        """Returns the recvRelativeVelocity status of the profile
        
        Returns
        -------
            bool
                The recvRelativeVelocity status of the profile"""
        return self.recvRelativeVelocity
    

    def setRecvRSSI(self, recvRSSI):
        """Sets the recvRSSI flag for the profile. If true, it will show recvRSSI related plots.
        
        Parameters
        ----------
            recvRSSI: bool
                The recvRSSI status of the profile. If true, it will show recvRSSI related plots."""
        if (type(recvRSSI) != bool):
            raise TypeError("recvRSSI must be a boolean")

        self.recvRSSI = recvRSSI

    
    def getRecvRSSI(self):
        """Returns the recvRSSI status of the profile
        
        Returns
        -------
            bool
                The recvRSSI status of the profile"""
        return self.recvRSSI
    

    def setRecvSourceAddress(self, recvSourceAddress):
        """Sets the recvSourceAddress flag for the profile. If true, it will show recvSourceAddress related plots.
        
        Parameters
        ----------
            recvSourceAddress: bool
                The recvSourceAddress status of the profile. If true, it will show recvSourceAddress related plots."""
        if (type(recvSourceAddress) != bool):
            raise TypeError("recvSourceAddress must be a boolean")

        self.recvSourceAddress = recvSourceAddress


    def getRecvSourceAddress(self):
        """Returns the recvSourceAddress status of the profile
        
        Returns
        -------
            bool
                The recvSourceAddress status of the profile"""
        return self.recvSourceAddress
    

    def setSatellites(self, satellites):
        """Sets the satellites flag for the profile. If true, it will show satellites related plots.
        
        Parameters
        ----------
            satellites: bool
                The satellites status of the profile. If true, it will show satellites related plots."""
        if (type(satellites) != bool):
            raise TypeError("satellites must be a boolean")

        self.satellites = satellites


    def getSatellites(self):
        """Returns the satellites status of the profile
        
        Returns
        -------
            bool
                The satellites status of the profile"""
        return self.satellites
    

    def setSendBitRate(self, sendBitRate):
        """Sets the sendBitRate flag for the profile. If true, it will show sendBitRate related plots.
        
        Parameters
        ----------
            sendBitRate: bool
                The sendBitRate status of the profile. If true, it will show sendBitRate related plots."""
        if (type(sendBitRate) != bool):
            raise TypeError("sendBitRate must be a boolean")

        self.sendBitRate = sendBitRate


    def getSendBitRate(self):
        """Returns the sendBitRate status of the profile
        
        Returns
        -------
            bool
                The sendBitRate status of the profile"""
        return self.sendBitRate
    

    def setSendBitDestinationAddress(self, sendBitDestinationAddress):
        """Sets the sendBitDestinationAddress flag for the profile. If true, it will show sendBitDestinationAddress related plots.
        
        Parameters
        ----------
            sendBitDestinationAddress: bool
                The sendBitDestinationAddress status of the profile. If true, it will show sendBitDestinationAddress related plots."""
        if (type(sendBitDestinationAddress) != bool):
            raise TypeError("sendBitDestinationAddress must be a boolean")

        self.sendBitDestinationAddress = sendBitDestinationAddress


    def getSendBitDestinationAddress(self):
        """Returns the sendBitDestinationAddress status of the profile
        
        Returns
        -------
            bool
                The sendBitDestinationAddress status of the profile"""
        return self.sendBitDestinationAddress
    

    def setSendDuration(self, sendDuration):
        """Sets the sendDuration flag for the profile. If true, it will show sendDuration related plots.
        
        Parameters
        ----------
            sendDuration: bool
                The sendDuration status of the profile. If true, it will show sendDuration related plots."""
        if (type(sendDuration) != bool):
            raise TypeError("sendDuration must be a boolean")

        self.sendDuration = sendDuration


    def getSendDuration(self):
        """Returns the sendDuration status of the profile
        
        Returns
        -------
            bool
                The sendDuration status of the profile"""
        return self.sendDuration
    

    def setSendIntegrity(self, sendIntegrity):
        """Sets the sendIntegrity flag for the profile. If true, it will show sendIntegrity related plots.
        
        Parameters
        ----------
            sendIntegrity: bool
                The sendIntegrity status of the profile. If true, it will show sendIntegrity related plots."""
        if (type(sendIntegrity) != bool):
            raise TypeError("sendIntegrity must be a boolean")

        self.sendIntegrity = sendIntegrity


    def getSendIntegrity(self):
        """Returns the sendIntegrity status of the profile
        
        Returns
        -------
            bool
                The sendIntegrity status of the profile"""
        return self.sendIntegrity
    

    def setSendMsgID(self, sendMsgID):
        """Sets the sendMsgID flag for the profile. If true, it will show sendMsgID related plots.
        
        Parameters
        ----------
            sendMsgID: bool
                The sendMsgID status of the profile. If true, it will show sendMsgID related plots."""
        if (type(sendMsgID) != bool):
            raise TypeError("sendMsgID must be a boolean")

        self.sendMsgID = sendMsgID


    def getSendMsgID(self):
        """Returns the sendMsgID status of the profile
        
        Returns
        -------
            bool
                The sendMsgID status of the profile"""
        return self.sendMsgID
    

    def setSendPropagationTime(self, sendPropagationTime):
        """Sets the sendPropagationTime flag for the profile. If true, it will show sendPropagationTime related plots.
        
        Parameters
        ----------
            sendPropagationTime: bool
                The sendPropagationTime status of the profile. If true, it will show sendPropagationTime related plots."""
        if (type(sendPropagationTime) != bool):
            raise TypeError("sendPropagationTime must be a boolean")

        self.sendPropagationTime = sendPropagationTime


    def getSendPropagationTime(self):
        """Returns the sendPropagationTime status of the profile
        
        Returns
        -------
            bool
                The sendPropagationTime status of the profile"""
        return self.sendPropagationTime
    

    def setSendRelativeVelocity(self, sendRelativeVelocity):
        """Sets the sendRelativeVelocity flag for the profile. If true, it will show sendRelativeVelocity related plots.
        
        Parameters
        ----------
            sendRelativeVelocity: bool
                The sendRelativeVelocity status of the profile. If true, it will show sendRelativeVelocity related plots."""
        if (type(sendRelativeVelocity) != bool):
            raise TypeError("sendRelativeVelocity must be a boolean")

        self.sendRelativeVelocity = sendRelativeVelocity


    def getSendRelativeVelocity(self):
        """Returns the sendRelativeVelocity status of the profile
        
        Returns
        -------
            bool
                The sendRelativeVelocity status of the profile"""
        return self.sendRelativeVelocity
    

    def setSendRSSI(self, sendRSSI):
        """Sets the sendRSSI flag for the profile. If true, it will show sendRSSI related plots.
        
        Parameters
        ----------
            sendRSSI: bool
                The sendRSSI status of the profile. If true, it will show sendRSSI related plots."""
        if (type(sendRSSI) != bool):
            raise TypeError("sendRSSI must be a boolean")

        self.sendRSSI = sendRSSI


    def getSendRSSI(self):
        """Returns the sendRSSI status of the profile
        
        Returns
        -------
            bool
                The sendRSSI status of the profile"""
        return self.sendRSSI
    

    def setSendSourceAddress(self, sendSourceAddress):
        """Sets the sendSourceAddress flag for the profile. If true, it will show sendSourceAddress related plots.
        
        Parameters
        ----------
            sendSourceAddress: bool
                The sendSourceAddress status of the profile. If true, it will show sendSourceAddress related plots."""
        if (type(sendSourceAddress) != bool):
            raise TypeError("sendSourceAddress must be a boolean")

        self.sendSourceAddress = sendSourceAddress


    def getSendSourceAddress(self):
        """Returns the sendSourceAddress status of the profile
        
        Returns
        -------
            bool
                The sendSourceAddress status of the profile"""
        return self.sendSourceAddress
    

    def setSendTypeID(self, sendTypeID):
        """Sets the sendTypeID flag for the profile. If true, it will show sendTypeID related plots.
        
        Parameters
        ----------
            sendTypeID: bool
                The sendTypeID status of the profile. If true, it will show sendTypeID related plots."""
        if (type(sendTypeID) != bool):
            raise TypeError("sendTypeID must be a boolean")

        self.sendTypeID = sendTypeID

    
    def getSendTypeID(self):
        """Returns the sendTypeID status of the profile
        
        Returns
        -------
            bool
                The sendTypeID status of the profile"""
        return self.sendTypeID
    

    def setSensorsUSBLFixBearingVsBearingRaw(self, sensorsUSBLFixBearingVsBearingRaw):
        """Sets the sensorsUSBLFixBearingVsBearingRaw flag for the profile. If true, it will show sensorsUSBLFixBearingVsBearingRaw related plots.
        
        Parameters
        ----------
            sensorsUSBLFixBearingVsBearingRaw: bool
                The sensorsUSBLFixBearingVsBearingRaw status of the profile. If true, it will show sensorsUSBLFixBearingVsBearingRaw related plots."""
        if (type(sensorsUSBLFixBearingVsBearingRaw) != bool):
            raise TypeError("sensorsUSBLFixBearingVsBearingRaw must be a boolean")

        self.sensorsUSBLFixBearingVsBearingRaw = sensorsUSBLFixBearingVsBearingRaw


    def getSensorsUSBLFixBearingVsBearingRaw(self):
        """Returns the sensorsUSBLFixBearingVsBearingRaw status of the profile
        
        Returns
        -------
            bool
                The sensorsUSBLFixBearingVsBearingRaw status of the profile"""
        return self.sensorsUSBLFixBearingVsBearingRaw
    

    def setSensorsUSBLFixElevationVsElevationRaw(self, sensorsUSBLFixElevationVsElevationRaw):
        """Sets the sensorsUSBLFixElevationVsElevationRaw flag for the profile. If true, it will show sensorsUSBLFixElevationVsElevationRaw related plots.
        
        Parameters
        ----------
            sensorsUSBLFixElevationVsElevationRaw: bool
                The sensorsUSBLFixElevationVsElevationRaw status of the profile. If true, it will show sensorsUSBLFixElevationVsElevationRaw related plots."""
        if (type(sensorsUSBLFixElevationVsElevationRaw) != bool):
            raise TypeError("sensorsUSBLFixElevationVsElevationRaw must be a boolean")

        self.sensorsUSBLFixElevationVsElevationRaw = sensorsUSBLFixElevationVsElevationRaw


    def getSensorsUSBLFixElevationVsElevationRaw(self):
        """Returns the sensorsUSBLFixElevationVsElevationRaw status of the profile
        
        Returns
        -------
            bool
                The sensorsUSBLFixElevationVsElevationRaw status of the profile"""
        return self.sensorsUSBLFixElevationVsElevationRaw
    

    def setSensorsUSBLFixRange(self, sensorsUSBLFixRange):
        """Sets the sensorsUSBLFixRange flag for the profile. If true, it will show sensorsUSBLFixRange related plots.
        
        Parameters
        ----------
            sensorsUSBLFixRange: bool
                The sensorsUSBLFixRange status of the profile. If true, it will show sensorsUSBLFixRange related plots."""
        if (type(sensorsUSBLFixRange) != bool):
            raise TypeError("sensorsUSBLFixRange must be a boolean")

        self.sensorsUSBLFixRange = sensorsUSBLFixRange


    def getSensorsUSBLFixRange(self):
        """Returns the sensorsUSBLFixRange status of the profile
        
        Returns
        -------
            bool
                The sensorsUSBLFixRange status of the profile"""
        return self.sensorsUSBLFixRange
    

    def setSensorsUSBLFixRangeVsBearingVsElevation(self, sensorsUSBLFixRangeVsBearingVsElevation):
        """Sets the sensorsUSBLFixRangeVsBearingVsElevation flag for the profile. If true, it will show sensorsUSBLFixRangeVsBearingVsElevation related plots.
        
        Parameters
        ----------
            sensorsUSBLFixRangeVsBearingVsElevation: bool
                The sensorsUSBLFixRangeVsBearingVsElevation status of the profile. If true, it will show sensorsUSBLFixRangeVsBearingVsElevation related plots."""
        if (type(sensorsUSBLFixRangeVsBearingVsElevation) != bool):
            raise TypeError("sensorsUSBLFixRangeVsBearingVsElevation must be a boolean")

        self.sensorsUSBLFixRangeVsBearingVsElevation = sensorsUSBLFixRangeVsBearingVsElevation


    def getSensorsUSBLFixRangeVsBearingVsElevation(self):
        """Returns the sensorsUSBLFixRangeVsBearingVsElevation status of the profile
        
        Returns
        -------
            bool
                The sensorsUSBLFixRangeVsBearingVsElevation status of the profile"""
        return self.sensorsUSBLFixRangeVsBearingVsElevation
    

    def setSensorsUSBLFixSourceID(self, sensorsUSBLFixSourceID):
        """Sets the sensorsUSBLFixSourceID flag for the profile. If true, it will show sensorsUSBLFixSourceID related plots.
        
        Parameters
        ----------
            sensorsUSBLFixSourceID: bool
                The sensorsUSBLFixSourceID status of the profile. If true, it will show sensorsUSBLFixSourceID related plots."""
        if (type(sensorsUSBLFixSourceID) != bool):
            raise TypeError("sensorsUSBLFixSourceID must be a boolean")

        self.sensorsUSBLFixSourceID = sensorsUSBLFixSourceID


    def getSensorsUSBLFixSourceID(self):
        """Returns the sensorsUSBLFixSourceID status of the profile
        
        Returns
        -------
            bool
                The sensorsUSBLFixSourceID status of the profile"""
        return self.sensorsUSBLFixSourceID
    

    def setSpeedOverGround(self, speedOverGround):
        """Sets the speedOverGround flag for the profile. If true, it will show speedOverGround related plots.
        
        Parameters
        ----------
            speedOverGround: bool
                The speedOverGround status of the profile. If true, it will show speedOverGround related plots."""
        if (type(speedOverGround) != bool):
            raise TypeError("speedOverGround must be a boolean")

        self.speedOverGround = speedOverGround


    def getSpeedOverGround(self):
        """Returns the speedOverGround status of the profile
        
        Returns
        -------
            bool
                The speedOverGround status of the profile"""
        return self.speedOverGround
    

    def setUtcTime(self, utcTime):
        """Sets the utcTime flag for the profile. If true, it will show utcTime related plots.
        
        Parameters
        ----------
            utcTime: bool
                The utcTime status of the profile. If true, it will show utcTime related plots."""
        if (type(utcTime) != bool):
            raise TypeError("utcTime must be a boolean")

        self.utcTime = utcTime


    def getUtcTime(self):
        """Returns the utcTime status of the profile
        
        Returns
        -------
            bool
                The utcTime status of the profile"""
        return self.utcTime
    

    def setAtual_charge(self, atual_charge):
        """Sets the atual_charge flag for the profile. If true, it will show atual_charge related plots.
        
        Parameters
        ----------
            atual_charge: bool
                The atual_charge status of the profile. If true, it will show atual_charge related plots."""
        if (type(atual_charge) != bool):
            raise TypeError("atual_charge must be a boolean")

        self.atual_charge = atual_charge


    def getAtual_charge(self):
        """Returns the atual_charge status of the profile
        
        Returns
        -------
            bool
                The atual_charge status of the profile"""
        return self.atual_charge
    

    def setCharging(self, charging):
        """Sets the charging flag for the profile. If true, it will show charging related plots.
        
        Parameters
        ----------
            charging: bool
                The charging status of the profile. If true, it will show charging related plots."""
        if (type(charging) != bool):
            raise TypeError("charging must be a boolean")

        self.charging = charging


    def getCharging(self):
        """Returns the charging status of the profile
        
        Returns
        -------
            bool
                The charging status of the profile"""
        return self.charging
    

    def setEqualize(self, equalize):
        """Sets the equalize flag for the profile. If true, it will show equalize related plots.
        
        Parameters
        ----------
            equalize: bool
                The equalize status of the profile. If true, it will show equalize related plots."""
        if (type(equalize) != bool):
            raise TypeError("equalize must be a boolean")

        self.equalize = equalize


    def getEqualize(self):
        """Returns the equalize status of the profile
        
        Returns
        -------
            bool
                The equalize status of the profile"""
        return self.equalize
    

    def setMx(self, Mx):
        """Sets the Mx flag for the profile. If true, it will show Mx related plots.
        
        Parameters
        ----------
            Mx: bool
                The Mx status of the profile. If true, it will show Mx related plots."""
        if (type(Mx) != bool):
            raise TypeError("Mx must be a boolean")

        self.Mx = Mx


    def getMx(self):
        """Returns the Mx status of the profile
        
        Returns
        -------
            bool
                The Mx status of the profile"""
        return self.Mx
    

    def setMy(self, My):
        """Sets the My flag for the profile. If true, it will show My related plots.
        
        Parameters
        ----------
            My: bool
                The My status of the profile. If true, it will show My related plots."""
        if (type(My) != bool):
            raise TypeError("My must be a boolean")

        self.My = My


    def getMy(self):
        """Returns the My status of the profile
        
        Returns
        -------
            bool
                The My status of the profile"""
        return self.My
    

    def setMz(self, Mz):
        """Sets the Mz flag for the profile. If true, it will show Mz related plots.
        
        Parameters
        ----------
            Mz: bool
                The Mz status of the profile. If true, it will show Mz related plots."""
        if (type(Mz) != bool):
            raise TypeError("Mz must be a boolean")

        self.Mz = Mz


    def getMz(self):
        """Returns the Mz status of the profile
        
        Returns
        -------
            bool
                The Mz status of the profile"""
        return self.Mz
    

    def setMagAbs(self, magAbs):
        """Sets the magAbs flag for the profile. If true, it will show magAbs related plots.
        
        Parameters
        ----------
            magAbs: bool
                The magAbs status of the profile. If true, it will show magAbs related plots."""
        if (type(magAbs) != bool):
            raise TypeError("magAbs must be a boolean")

        self.magAbs = magAbs


    def getMagAbs(self):
        """Returns the magAbs status of the profile
        
        Returns
        -------
            bool
                The magAbs status of the profile"""
        return self.magAbs
    

    def setVoltage(self, voltage):
        """Sets the voltage flag for the profile. If true, it will show voltage related plots.
        
        Parameters
        ----------
            voltage: bool
                The voltage status of the profile. If true, it will show voltage related plots."""
        if (type(voltage) != bool):
            raise TypeError("voltage must be a boolean")

        self.voltage = voltage


    def getVoltage(self):
        """Returns the voltage status of the profile
        
        Returns
        -------
            bool
                The voltage status of the profile"""
        return self.voltage
    

    def setOverviewPf(self, overviewPf):
        """Sets the overviewPf flag for the profile. If true, it will show overviewPf related plots.
        
        Parameters
        ----------
            overviewPf: bool
                The overviewPf status of the profile. If true, it will show overviewPf related plots."""
        if (type(overviewPf) != bool):
            raise TypeError("overviewPf must be a boolean")

        self.overviewPf = overviewPf


    def getOverviewPf(self):
        """Returns the overviewPf status of the profile
        
        Returns
        -------
            bool
                The overviewPf status of the profile"""
        return self.overviewPf
    

    def setOverviewFilterDrUsbl(self, overviewFilterDrUsbl):
        """Sets the overviewFilterDrUsbl flag for the profile. If true, it will show overviewFilterDrUsbl related plots.
        
        Parameters
        ----------
            overviewFilterDrUsbl: bool
                The overviewFilterDrUsbl status of the profile. If true, it will show overviewFilterDrUsbl related plots."""
        if (type(overviewFilterDrUsbl) != bool):
            raise TypeError("overviewFilterDrUsbl must be a boolean")

        self.overviewFilterDrUsbl = overviewFilterDrUsbl


    def getOverviewFilterDrUsbl(self):
        """Returns the overviewFilterDrUsbl status of the profile
        
        Returns
        -------
            bool
                The overviewFilterDrUsbl status of the profile"""
        return self.overviewFilterDrUsbl


    def getActual_charge(self):
        """Returns the actual_charge status of the profile
        
        Returns
        -------
            bool
                The actual_charge status of the profile"""
        return self.actual_charge
    

    def setCharging(self, charging):
        """Sets the charging flag for the profile. If true, it will show charging related plots.
        
        Parameters
        ----------
            charging: bool
                The charging status of the profile. If true, it will show charging related plots."""
        if (type(charging) != bool):
            raise TypeError("charging must be a boolean")

        self.charging = charging


    def update(self, name=None, usbl=False, altimeter=False, batMonit=False,
                insidePressure=False, imu=False, gps=False, depthCell=False,
                thrusters=False, equalize=False, Mx=False, My=False, Mz=False,
                magAbs=False, voltage=False, overviewPf=False, overviewFilterDrUsbl=False,
                actual_charge=False, charging=False, controlSurge=False, filterVsVirtualTarget=False,
                crossTrackAlongTrack=False, Ax=False, Ay=False, Az=False, current=False,
                temperature=False, speed=False, errors=False, Gx=False, Gy=False,
                Gz=False, altitude=False, pitch=False, roll=False, yaw=False,
                latitude=False, longitude=False, magX=False, magY=False, magZ=False,
                maxCell=False, maxTemp=False, measurementUSBLFixBearing=False, 
                measurementUSBLFixElevation=False, measurementUSBLFixBearingRaw=False,
                measurementUSBLFixElevationRaw=False, measurementUSBLFixRange=False,
                measurementUSBLFixSoundSpeed=False, measurementUSBLFixSourceID=False,
                measurementUSBLFixTypeID=False, pressure=False, mode=False, numberPacks=False,
                recvBitRate=False, recvBitDestinationAddress=False, recvDuration=False,
                recvIntegrity=False, recvMsgID=False, recvPropagationTime=False,
                recvRelativeVelocity=False, recvRSSI=False, recvSourceAddress=False,
                satellites=False, sendBitRate=False, sendBitDestinationAddress=False,
                sendDuration=False, sendIntegrity=False, sendMsgID=False,
                sendPropagationTime=False, sendRelativeVelocity=False, sendRSSI=False,
                sendSourceAddress=False, sendTypeID=False, sensorsUSBLFixBearingVsBearingRaw=False,
                sensorsUSBLFixElevationVsElevationRaw=False, sensorsUSBLFixRange=False,
                sensorsUSBLFixRangeVsBearingVsElevation=False, sensorsUSBLFixSourceID=False,
                speedOverGround=False, utcTime=False, minTemp=False, minCell=False,):
        """Updates the profile with the given parameters. If no name is given,
        the name will remain unchanged. If any of the other parameters are not given,
        they will be set to false.
        """
        if (name == None):
            name = self.getName()
        
        oldProfile = self.clone()
        self.setName(name)
        self.setUsbl(usbl)
        self.setAltimeter(altimeter)
        self.setBatMonit(batMonit)
        self.setInsidePressure(insidePressure)
        self.setImu(imu)
        self.setGps(gps)
        self.setDepthCell(depthCell)
        self.setThrusters(thrusters)
        self.setControlSurge(controlSurge)
        self.setFilterVsVirtualTarget(filterVsVirtualTarget)
        self.setCrossTrackAlongTrack(crossTrackAlongTrack)
        self.setAx(Ax)
        self.setAy(Ay)
        self.setAz(Az)
        self.setCurrent(current)
        self.setErrors(errors)
        self.setGx(Gx)
        self.setGy(Gy)
        self.setGz(Gz)
        self.setSpeed(speed)
        self.setTemperature(temperature)
        self.setActual_charge(actual_charge)
        self.setOverviewPf(overviewPf)
        self.setOverviewFilterDrUsbl(overviewFilterDrUsbl)
        self.setCharging(charging)
        self.setEqualize(equalize)
        self.setMx(Mx)
        self.setMy(My)
        self.setMz(Mz)
        self.setMagAbs(magAbs)
        self.setVoltage(voltage)
        self.setAltitude(altitude)
        self.setLatitude(latitude)
        self.setLongitude(longitude)
        self.setMagX(magX)
        self.setMagY(magY)
        self.setMagZ(magZ)
        self.setMaxCell(maxCell)
        self.setMaxTemp(maxTemp)
        self.setMeasurementUSBLFixBearing(measurementUSBLFixBearing)
        self.setMeasurementUSBLFixBearingRaw(measurementUSBLFixBearingRaw)
        self.setMeasurementUSBLFixElevation(measurementUSBLFixElevation)
        self.setMeasurementUSBLFixElevationRaw(measurementUSBLFixElevationRaw)
        self.setMeasurementUSBLFixRange(measurementUSBLFixRange)
        self.setMeasurementUSBLFixSoundSpeed(measurementUSBLFixSoundSpeed)
        self.setMeasurementUSBLFixSourceID(measurementUSBLFixSourceID)
        self.setMeasurementUSBLFixTypeID(measurementUSBLFixTypeID)
        self.setMinCell(minCell)
        self.setMinTemp(minTemp)
        self.setPitch(pitch)
        self.setRoll(roll)
        self.setYaw(yaw)
        self.setPressure(pressure)
        self.setMode(mode)
        self.setNumberPacks(numberPacks)
        self.setRecvBitRate(recvBitRate)
        self.setRecvBitDestinationAddress(recvBitDestinationAddress)
        self.setRecvDuration(recvDuration)
        self.setRecvIntegrity(recvIntegrity)
        self.setRecvMsgID(recvMsgID)
        self.setRecvPropagationTime(recvPropagationTime)
        self.setRecvRelativeVelocity(recvRelativeVelocity)
        self.setRecvRSSI(recvRSSI)
        self.setRecvSourceAddress(recvSourceAddress)
        self.setSatellites(satellites)
        self.setSendBitRate(sendBitRate)
        self.setSendBitDestinationAddress(sendBitDestinationAddress)
        self.setSendDuration(sendDuration)
        self.setSendIntegrity(sendIntegrity)
        self.setSendMsgID(sendMsgID)
        self.setSendPropagationTime(sendPropagationTime)
        self.setSendRelativeVelocity(sendRelativeVelocity)
        self.setSendRSSI(sendRSSI)
        self.setSendSourceAddress(sendSourceAddress)
        self.setSendTypeID(sendTypeID)
        self.setSensorsUSBLFixBearingVsBearingRaw(sensorsUSBLFixBearingVsBearingRaw)
        self.setSensorsUSBLFixElevationVsElevationRaw(sensorsUSBLFixElevationVsElevationRaw)
        self.setSensorsUSBLFixRange(sensorsUSBLFixRange)
        self.setSensorsUSBLFixRangeVsBearingVsElevation(sensorsUSBLFixRangeVsBearingVsElevation)
        self.setSensorsUSBLFixSourceID(sensorsUSBLFixSourceID)
        self.setSpeedOverGround(speedOverGround)
        self.setUtcTime(utcTime)
        try:
            Profile.deleteProfile(oldProfile) # Remove old version from profiles.json
        except ValueError:
            pass
        Profile.serializeClass(self) # Add new version to profiles.json


    def delete(self):
        """Removes itself from profiles.json"""

        Profile.deleteProfile(self)


    def filter(self, files):
        """Filters the files based on the profile
        
        Parameters
        ----------
            files: list
                list of files to filter
        Returns
        -------
            list
                list of relevant files for this profile"""
        if (type(files) not in (list, tuple)):
            raise TypeError("Files must be a list or tuple")
        elif (files == [] or files == ()):
            raise ValueError("Files can't be empty")

        #filtered_files = files
        for file in files:
            if (type(file) != str):
                raise TypeError("Files must be a list or tuple of strings")
            elif (file == None or file == ""):
                raise ValueError("Files can't contain None/Null or empty strings")
            
        filtered_files = self.__filter_aux(files)

        return filtered_files
            

    def __filter_aux(self, files):
        """Auxiliary function to filter files based on the profile"""

        output_files = [file for file in files]
        for file in files:
            lowerCaseFile = file.lower()
            if (self.getAltimeter() and re.search("altimeter", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getUsbl() and re.search("usbl", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getBatMonit() and re.search("batmonit", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getInsidePressure() and re.search("insidepressure", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getImu() and re.search("imu", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getGps() and re.search("gps", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getDepthCell() and re.search("depthcell", lowerCaseFile) != None):
                output_files.remove(file)
            elif (self.getThrusters() and re.search("thruster", lowerCaseFile) != None):
                output_files.remove(file)

        return output_files

        
    def clone(self):
        """Clones the profile"""
        return Profile(self.getName(), self.getUsbl(), self.getAltimeter(),
                       self.getDepthCell(), self.getGps(), self.getImu(),
                       self.getInsidePressure(), self.getBatMonit(), 
                       self.getThrusters())


    ########################################
    ######       public static        ######
    ######          methods           ######
    ########################################


    @staticmethod
    def deserializeClass(jsonData): # TODO - create override method that takes list of jsonData instead of jsonData
        """Deserializes a JSON data into a Profile object"""
        if (jsonData == None): # TODO - Check if jsonData is a JSON object / better input validation
            raise ValueError("JSON data can't be None/Null")
        
        return Profile(jsonData['name'], jsonData['usbl'], jsonData['altimeter'],
                        jsonData['depthCell'], jsonData['gps'], jsonData['imu'],
                        jsonData['insidePressure'], jsonData['batMonit'], jsonData['thrusters'])
    
    @staticmethod
    def deserializeFile(filePath): # TODO - create overriden method that takes jsonData instead of filePath
        """Deserializes a JSON file a list of Profile objects"""
        if (type(filePath) != str):
            raise TypeError("File path must be a string")
        elif (filePath == None or filePath == ""):
            raise ValueError("File path can't be None/Null or empty")

        try:
            with open(filePath) as jsonFile:
                portalocker.lock(jsonFile, portalocker.LockFlags.EXCLUSIVE) # Lock file
                jsonData = json.load(jsonFile) # Read JSON
                if (type(jsonData) != list):
                    # If there was only one profile on the json file
                    jsonData = [jsonData]

                deserializedProfiles = []
                for profile in jsonData: # Convert JSON into list of Profile objects
                    deserializedProfiles.append(Profile.deserializeClass(profile))
        except FileNotFoundError as fileNotFoundError:
            raise fileNotFoundError
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception
    
        return deserializedProfiles
    

    @staticmethod
    def deserializeFileWithoutCreatingProfiles(filePath):
        """Deserializes a JSON file into a list of JSON objects.
        
        Use this method to avoid recursion errors when creating Profile objects.
        The recursion would occur when calling deserializeClass() which calls
        the constructor."""
        if (type(filePath) != str):
            raise TypeError("File path must be a string")
        elif (filePath == None or filePath == ""):
            raise ValueError("File path can't be None/Null or empty")

        try:
            with open(filePath) as jsonFile:
                portalocker.lock(jsonFile, portalocker.LockFlags.EXCLUSIVE) # Lock file
                jsonData = json.load(jsonFile) # Read JSON
                if (type(jsonData) != list):
                    # If there was only one profile on the json file
                    jsonData = [jsonData]
        except FileNotFoundError as fileNotFoundError:
            raise fileNotFoundError
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception
    
        return jsonData
    

    @staticmethod
    def serializeClass(profile):
        """Serializes a Profile object into a JSON string"""
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")
        elif (profile.getName() == None or profile.getName() == ""):
            raise ValueError("Profile name can't be None/Null or empty")
        elif (Profile.profileAlreadyExists(profile)):
            raise ValueError("Profile already exists")

        deserializedProfiles = []
        try:
            deserializedProfiles = Profile.deserializeFile("profiles.json")
        except FileNotFoundError as fileNotFoundError: # TODO - remove "as" keyword?
            json.dump(profile, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception
        
        for deserializedProfile in deserializedProfiles:
            if (deserializedProfile.getName().lower() == profile.getName().lower()):
                raise ValueError("Profile already exists")
            
        deserializedProfiles.append(profile)
        profiles = deserializedProfiles
        profiles.sort()

        file = open("profiles.json", "w")
        portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE) # Lock file
        json.dump(profiles, file, indent=4, cls=Profile.ProfileEncoder)
        file.close()

        return Profile.ProfileEncoder().encode(profile)

    
    @staticmethod
    def serializeProfiles(profiles):
        """Serializes a list or tuple of Profile objects into a JSON string"""
        if (type(profiles) not in (list, tuple)):
            raise TypeError("Profiles must be a list or tuple")
        elif (profiles == None or len(profiles) == 0):
            raise ValueError("Profiles can't be None/Null or empty")

        for profile in profiles:
            if (type(profile) != Profile):
                raise TypeError("Profile must be a Profile object")
            
        # TODO call serializeClass for each profile in profiles

        file = open("profiles.json", "w")
        portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE) # Lock file
        json.dump(profiles, file, indent=4, cls=Profile.ProfileEncoder)
        file.close()

        return json.dumps([profile.__dict__ for profile in profiles])
    

    @staticmethod
    def deleteProfile(profile):
        """Deletes a profile from the profiles.json file"""
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")

        Profile.deleteProfileByName(profile.getName())


    @staticmethod
    def deleteProfileByName(profileName):
        """Deletes a profile from the profiles.json file"""
        if (type(profileName) != str):
            raise TypeError("Profile name must be a string")
        elif (profileName == None or profileName == ""):
            raise ValueError("Profile name can't be None/Null or empty")

        profiles = []
        try:
            deserializedProfiles = Profile.deserializeFile("profiles.json")
            foundProfile = False
            for deserializedProfile in deserializedProfiles:
                if (deserializedProfile.getName().lower() == profileName.lower()):
                    deserializedProfiles.remove(deserializedProfile)
                    foundProfile = True
                    break
            if (not foundProfile):
                raise ValueError("Profile doesn't exist")
            profiles = deserializedProfiles
        except FileNotFoundError as fileNotFoundError:
            raise fileNotFoundError
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception


        file = open("profiles.json", "w")
        portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE) # Lock file
        json.dump(profiles, file, indent=4, cls=Profile.ProfileEncoder)
        file.close()

    
    @staticmethod
    def profileAlreadyExists(profile):
    
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")
        elif (profile.getName() == None or profile.getName() == ""):
            raise ValueError("Profile name can't be None/Null or empty")
        
        try:
            deserializedProfiles = Profile.deserializeFileWithoutCreatingProfiles("profiles.json")
            for deserializedProfile in deserializedProfiles:
                if (profile.getName().lower() == deserializedProfile['name'].lower()):
                    return True
                
        except FileNotFoundError as fileNotFoundError:
            return False
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception
        
        return False
    

    @staticmethod
    def loadProfile(profileName):
        """Loads a profile from the profiles.json file"""
        if (type(profileName) != str):
            raise TypeError("Profile name must be a string")
        elif (profileName == ""):
            raise ValueError("Profile name can't be None/Null or empty")

        deserializedProfiles = []
        try:
            deserializedProfiles = Profile.deserializeFile("profiles.json")
        except FileNotFoundError as fileNotFoundError:
            raise fileNotFoundError
        except PermissionError as permissionError:
            raise permissionError
        except Exception as exception:
            raise exception

        for deserializedProfile in deserializedProfiles:
            if (deserializedProfile.getName().lower() == profileName.lower()):
                return deserializedProfile
        
        raise ValueError("Profile doesn't exist")

    
    ########################################
    ######       To String method     ######
    ########################################

    def __str__(self):
        return "Profile = { name: " + self.getName() + ", USBL: " + str(self.getUsbl()) + ", Altimeter: " + str(self.getAltimeter()) + ", DepthCell: " + str(self.getDepthCell()) + ", GPS: " + str(self.getGps()) + ", IMU: " + str(self.getImu()) + ", InsidePressure: " + str(self.getInsidePressure()) + ", BatMonit: " + str(self.getBatMonit()) + ", Thrusters: " + str(self.getThrusters()) + "}"
    
    ########################################
    ######       Less Than method     ######
    ########################################

    def __lt__(self, other):
        if (type(other) != Profile):
            raise TypeError("Other must be a Profile object")
        if (self.getName() == None or other.getName() == None):
            raise ValueError("Name can't be None/Null")

        return self.getName() < other.getName()
    
    ########################################
    ######       Equals   method      ######
    ########################################

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return False
        
        return (self.getAltimeter() == other.getAltimeter() and 
                self.getUsbl() == other.getUsbl() and
                self.getName() == other.getName() and
                self.getDepthCell() == other.getDepthCell() and
                self.getGps() == other.getGps() and
                self.getImu() == other.getImu() and
                self.getInsidePressure() == other.getInsidePressure() and
                self.getBatMonit() == other.getBatMonit() and 
                self.getThrusters() == other.getThrusters())


############################################
######      Other module methods      ######
############################################

def readJSONfile(file):
    """Reads a JSON file and returns the data
    
    Parameters
    ----------
        file: str
            The path to the JSON file
    Returns
    -------
        dict
            The data from the JSON file"""
    if (type(file) != str):
        raise TypeError("File must be a string")
    elif (file == None or file == ""):
        raise ValueError("File can't be None/Null or empty")

    try:
        with open(file) as jsonFile:
            portalocker.lock(jsonFile, portalocker.LockFlags.SHARED) # Lock file
            data = json.load(jsonFile)
            return data
    except FileNotFoundError as fileNotFoundError:
        raise fileNotFoundError
    except PermissionError as permissionError:
        raise permissionError


############################################
######       Test the class           ######
############################################

if __name__ == '__main__':

   pass