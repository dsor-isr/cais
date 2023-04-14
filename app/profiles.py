import json
import os

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

    # TODO - add filter functions
    # TODO - Add more fields
    # TODO - Create default profiles
    # TODO - Delete Profiles from CAIS
    #           - Find way to ask if user is sure
    #           - Find way to ask for a password for deletion (store encrypted version of password?)
    # TODO - Add Profiles to CAIS
    # TODO - Update Profiles in CAIS

    # TODO - See the differences between pickle and json
    # TODO - I think we no longer use pickle. Remove from here and requirements.txt


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

    def __init__(self, name, usbl=True, altimeter=True):
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
        """
        try:
            self.__validateConstructorAttributes(name, usbl, altimeter)
        except Exception as e:
            raise e

        self.name = name
        self.usbl = usbl
        self.altimeter = altimeter
    

    ########################################
    ######     private methods        ######
    ########################################

    @classmethod
    def __validateConstructorAttributes(self, name, usbl, altimeter):
        """Validates the attributes of the constructor"""
        if (type(name) != str):
            raise TypeError("Name must be a string")
        elif (name == None or name == ""):
            raise ValueError("Name can't be None/Null or empty")
        if (type(usbl) != bool):
            raise TypeError("USBL must be a boolean")
        if (type(altimeter) != bool):
            raise TypeError("Altimeter must be a boolean")


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


    ########################################
    ######       public static        ######
    ######          methods           ######
    ########################################


    @staticmethod
    def deserializeClass(jsonData): # TODO - create override method that takes list of jsonData instead of jsonData
        """Deserializes a JSON data into a Profile object"""
        if (jsonData == None): # TODO - Check if jsonData is a JSON object / better input validation
            raise ValueError("JSON data can't be None/Null")

        return Profile(jsonData['name'], jsonData['usbl'], jsonData['altimeter'])

    
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
        except FileNotFoundError as e:
            raise e
        except PermissionError as e:
            raise e
        except Exception as e:
            raise e
    
        return deserializedProfiles
    

    @staticmethod
    def serializeClass(profile):
        """Serializes a Profile object into a JSON string"""
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")
        elif (profile.getName() == None or profile.getName() == ""):
            raise ValueError("Profile name can't be None/Null or empty")

        # TODO - read profiles.json
        #            - Catch exception if file doesn't exist
        #      - check if profile already exists
        #      - append profile to profiles
        #      - sort by name
        #      - write profiles to profiles.json
        profiles = [profile]
        try:
            deserializedProfiles = Profile.deserializeFile("profiles.json")
            for deserializedProfile in deserializedProfiles:
                if (deserializedProfile.getName().lower() == profile.getName().lower()):
                    raise ValueError("Profile already exists")
            
            deserializedProfiles.append(profile)
            profiles = deserializedProfiles
            profiles.sort()
        except FileNotFoundError as e:
            json.dump(profile, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
        except PermissionError as e:
            raise e
        except Exception as e:
            raise e

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
        except FileNotFoundError as e:
            json.dump(profile, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
        except PermissionError as e:
            raise e
        except Exception as e:
            raise e

        json.dump(profiles, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)

    
    ########################################
    ######       To String method     ######
    ########################################

    def __str__(self):
        return "Profile = {name: " + self.getName() + ", USBL: " + str(self.getUsbl()) + ", Altimeter: " + str(self.getAltimeter()) + "}"
    
    ########################################
    ######       Less Than method     ######
    ########################################

    def __lt__(self, other):
        if (type(other) != Profile):
            raise TypeError("Other must be a Profile object")
        if (self.getName() == None or other.getName() == None):
            raise ValueError("Name can't be None/Null")
        
        return self.getName() < other.getName()


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
    except FileNotFoundError as e:
        raise e
    except PermissionError as e:
        raise e





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
    if os.path.exists("profiles.json"):
        # Delete file for testing purposes
        os.remove("profiles.json")
    try:
        Profile.serializeClass(Profile("Eletronics", True, False))
    except Exception as e:
        print("Something very weird happened")
        raise e
    try:
        Profile.serializeClass(Profile("Eletronics", False, False)) # Should throw an exception
        print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    except Exception as e:
        print("Profile already exists")
    try:
        Profile.serializeClass(Profile("Control", False, False))
    except Exception as e:
        print("Something very weird happened")
        raise e
    try:
        Profile.serializeClass(Profile("Admin", True, True))
    except Exception as e:
        print("Something very weird happened")
        raise e
    try:
        Profile.serializeClass(Profile("Admin", True, True)) # Should throw an exception
        print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    except Exception as e:
        print("Profile already exists")
    try:
        Profile.serializeClass(Profile("Eletronics", True, False)) # Should throw an exception
        print("This should have never been printed. An exception due to pre-existing profile should have been thrown")
    except Exception as e:
        print("Profile already exists")
    try:
        Profile.serializeClass(Profile("Robotics", False, False))
    except Exception as e:
        print("Something very weird happened")
        raise e

    deserializedProfiles = Profile.deserializeFile("profiles.json")
    print("Printing all previously serialized classes from profiles.json")
    for profile in deserializedProfiles:
        print(profile)

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