import json
import os
import re

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
                  gps=True, imu=True, insidePressure=True, batMonit=True):
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
                                                 insidePressure, batMonit)
        except ValueError as valueError:
            raise valueError
        except TypeError as typeError:
            raise typeError
        
        self.name = name
        self.usbl = usbl
        self.altimeter = altimeter
        self.depthCell = depthCell
        self.gps = gps
        self.imu = imu
        self.insidePressure = insidePressure
        self.batMonit = batMonit


    ########################################
    ######     private methods        ######
    ########################################

    @classmethod
    def __validateConstructorAttributes(self, name, usbl, altimeter, depthCell, gps, imu, insidePressure, batMonit):
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


    ########################################
    ######     normal  methods        ######
    ########################################

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


    def update(self, name=None, usbl=False, altimeter=False, batMonit=False,
                insidePressure=False, imu=False, gps=False, depthCell=False):
        """Updates the profile with the given parameters. If no name is given,
        the name will remain unchanged. If any of the other parameters are not given,
        they will be set to false.
        
        Parameters
        ----------
            name: str
                The name of the profile
            usbl: bool
                The USBL status of the profile. If true, it will show USBL related plots.
            altimeter: bool
                The altimeter status of the profile. If true, it will show altimeter related plots.
            batMonit: bool
                The batMonit status of the profile. If true, it will show batMonit related plots.
            insidePressure: bool
                The insidePressure status of the profile. If true, it will show insidePressure related plots.
            imu: bool
                The imu status of the profile. If true, it will show imu related plots.
            gps: bool
                The gps status of the profile. If true, it will show gps related plots.
            depthCell: bool
                The depthCell status of the profile. If true, it will show depthCell related plots.
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
            raise TypeError("Files must be a list")
        elif (files == [] or files == ()):
            raise ValueError("Files can't be empty")

        filtered_files = files
        for file in files:
            if (type(file) != str):
                raise TypeError("Files must be a list of strings")
            elif (file == None or file == ""):
                raise ValueError("Files can't contain None/Null or empty strings")
            
            filtered_files = self.__filter_aux(files)

        return filtered_files
            

    def __filter_aux(self, files):
        """Auxiliary function to filter files based on the profile"""
        for file in files:
            lowerCaseFile = file.lower()
            if (self.getAltimeter() and re.search("altimeter", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getUsbl() and re.search("usbl", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getBatMonit() and re.search("batmonit", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getInsidePressure() and re.search("insidepressure", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getImu() and re.search("imu", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getGps() and re.search("gps", lowerCaseFile) != None):
                files.remove(file)
            elif (self.getDepthCell() and re.search("depthcell", lowerCaseFile) != None):
                files.remove(file)

        return files

        
    def clone(self):
        """Clones the profile"""
        return Profile(self.getName(), self.getUsbl(), self.getAltimeter(),
                       self.getDepthCell(), self.getGps(), self.getImu(),
                       self.getInsidePressure(), self.getBatMonit())


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
                        jsonData['insidePressure'], jsonData['batMonit'])
    
    @staticmethod
    def deserializeFile(filePath): # TODO - create overriden method that takes jsonData instead of filePath
        """Deserializes a JSON file a list of Profile objects"""
        if (type(filePath) != str):
            raise TypeError("File path must be a string")
        elif (filePath == None or filePath == ""):
            raise ValueError("File path can't be None/Null or empty")

        try:
            with open(filePath) as jsonFile:
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
        except FileNotFoundError as fileNotFoundError:
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

        json.dump(profiles, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
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

        json.dump(profiles, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
        return json.dumps([profile.__dict__ for profile in profiles])
    

    @staticmethod
    def deleteProfile(profile):
        """Deletes a profile from the profiles.json file"""
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")

        profiles = []
        try:
            deserializedProfiles = Profile.deserializeFile("profiles.json")
            foundProfile = False
            for deserializedProfile in deserializedProfiles:
                if (deserializedProfile.getName().lower() == profile.getName().lower()):
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

        json.dump(profiles, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)

    
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

    
    ########################################
    ######       To String method     ######
    ########################################

    def __str__(self):
        return "Profile = { name: " + self.getName() + ", USBL: " + str(self.getUsbl()) + ", Altimeter: " + str(self.getAltimeter()) + ", DepthCell: " + str(self.getDepthCell()) + ", GPS: " + str(self.getGps()) + ", IMU: " + str(self.getImu()) + ", InsidePressure: " + str(self.getInsidePressure()) + ", BatMonit: " + str(self.getBatMonit()) + "}"
    
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
                self.getBatMonit() == other.getBatMonit())


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

    # Create a profile
    #profile = Profile("Eletronics", True, False)
    #print(profile)

    # Serialize profile to JSON
    #Profile.serializeClass(profile)
    #print(Profile.serializeClass(profile))

    # Serialize 3 profiles to JSON
    #Profile.serializeProfiles([profile, Profile("Control", False, False), Profile("Admin", True, True)])
    #print(Profile.serializeProfiles([profile, Profile("Control", False, False), Profile("Admin", True, True)]))

    # Read the json file with one profile
    #print(readJSONfile("profile.json"))

    # Read the json file with 3 profiles
    #print(readJSONfile("profiles.json"))

    # Deserialize json data corresponding to one profile
    #deserializedProfile = Profile.deserializeClass(readJSONfile("profile.json"))
    #print(deserializedProfile)

    # Deserialize json data corresponding to 3 profiles
    # deserializedProfiles = Profile.deserializeFile("profiles.json")
    # for profile in deserializedProfiles:
    #    print(profile)

    # Serialize profiles to JSON with repeated profiles
    # if os.path.exists("profiles.json"):
    #     # Delete file for testing purposes
    #     os.remove("profiles.json")
    # try:
    #     Profile.serializeClass(Profile("Eletronics", True, False))
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e
    # try:
    #     Profile.serializeClass(Profile("Eletronics", False, False)) # Should throw an exception
    #     print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    # except Exception as e:
    #     print("Profile already exists")
    # try:
    #     Profile.serializeClass(Profile("Control", False, False))
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e
    # try:
    #     Profile.serializeClass(Profile("Admin", True, True))
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e
    # try:
    #     Profile.serializeClass(Profile("Admin", True, True)) # Should throw an exception
    #     print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    # except Exception as e:
    #     print("Profile already exists")
    # try:
    #     Profile.serializeClass(Profile("Eletronics", True, False)) # Should throw an exception
    #     print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    # except Exception as e:
    #     print("Profile already exists")
    # try:
    #     Profile.serializeClass(Profile("Robotics", False, False))
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e

    # deserializedProfiles = Profile.deserializeFile("profiles.json")
    # print("Printing all previously serialized classes from profiles.json")
    # for profile in deserializedProfiles:
    #     print(profile)

    # Delete a profile
    # try:
    #     Profile.deleteProfile(Profile("Eletronics", True, False))
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e

    # Delete a profile that doesn't exist
    # try:
    #     Profile.deleteProfile(Profile("Eletronics", True, False)) # Should throw a ValueError
    #     print("This should have never been printed. An exception due to non-existing profile should have been thrown")
    # except ValueError as e:
    #     print("Profile doesn't exist")
    # except Exception as e:
    #     print("Something very weird happened")
    #     raise e

    # filter files
    # files = ['Altimeter', 'USBL', 'altimeter', 'drivers', 'ALTIMETER']
    # expected = ['USBL', 'drivers']
    # profile = Profile("Eletronics", False, True)
    # print("Profile: " + str(profile))
    # filteredFiles = profile.filter(files)
    # print("Filtered files: " + str(filteredFiles))
    # print("filteredFiles == expected: " + str(filteredFiles == expected))

    # update profile
    # profile = Profile("Eletronics", False, True)
    # oldProfile = profile.clone()
    # print(str(profile))
    # print("Before update: oldProfile == profile: " + str(oldProfile == profile))
    # profile.update("DSOR", True, True)
    # print(str(profile))
    # print("After update: oldProfile == profile: " + str(oldProfile == profile))

    # update profile with invalid name
    pass