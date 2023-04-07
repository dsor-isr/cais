import json
import pickle

class Profile:
    # TODO - add filter functions
    # TODO - Add more fields
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
        """Creates a Profile object"""
        try:
            self.__validateConstructorAttributes(name, usbl, altimeter)
        except Exception as e:
            raise e

        #print("Before setting attributes:")
        #print("name = " + name)
        #print("usbl = " + str(usbl))
        #print("altimeter = " + str(altimeter))
        #print("self.name = " + self.name)
        #print("self.usbl = " + str(self.usbl))
        #print("self.altimeter = " + str(self.altimeter))

        self.name = name
        self.usbl = usbl
        self.altimeter = altimeter

        #print("After setting attributes:")
        #print("self.name = " + self.name)
        #print("self.usbl = " + str(self.usbl))
        #print("self.altimeter = " + str(self.altimeter))
    

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
        """Sets the name of the profile"""
        if (type(name) != str):
            raise TypeError("Name must be a string")
        elif (name == None or name == ""):
            raise ValueError("Name can't be None/Null or empty")

        self.name = name


    def getName(self):
        """Returns the name of the profile"""
        return self.name

    
    def setUsbl(self, usbl):
        """Sets the usbl flag for the profile. If true, it will show USBL related plots."""
        if (type(usbl) != bool):
            raise TypeError("USBL must be a boolean")

        self.usbl = usbl

    
    def getUsbl(self):
        """Returns the USBL status of the profile"""
        return self.usbl

    
    def setAltimeter(self, altimeter):
        """Sets the altimeter flag for the profile. If true, it will show altimeter related plots."""
        if (type(altimeter) != bool):
            raise TypeError("Altimeter must be a boolean")

        self.altimeter = altimeter


    def getAltimeter(self):
        """Returns the altimeter status of the profile"""
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

        #print("jsonData['name'] = " + jsonData['name'])
        #print("jsonData['usbl'] = " + str(jsonData['usbl']))
        #print("jsonData['altimeter'] = " + str(jsonData['altimeter']))

        return Profile(jsonData['name'], jsonData['usbl'], jsonData['altimeter'])

    
    @staticmethod
    def deserializeFile(filePath): # TODO - create override method that takes jsonData instead of filePath
        """Deserializes a JSON file into a Profile object"""
        if (type(filePath) != str):
            raise TypeError("File path must be a string") # TODO - Check if file exists
        elif (filePath == None or filePath == ""):
            raise ValueError("File path can't be None/Null or empty")

        try:
            with open(filePath) as jsonFile:
                jsonData = json.load(jsonFile)
                print("jsonData = " + str(jsonData))
                #return Profile.deserializeClass(jsonData)
        except Exception as e: # TODO - Catch specific exceptions
            raise e
    

    @staticmethod
    def serializeClass(profile):
        """Serializes a Profile object into a JSON string"""
        if (type(profile) != Profile):
            raise TypeError("Profile must be a Profile object")
        elif (profile == None):
            raise ValueError("Profile can't be None/Null")


        json.dump(profile, open("profile.json", "w"), indent=4, cls=Profile.ProfileEncoder)
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

        json.dump(profiles, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
        return json.dumps([profile.__dict__ for profile in profiles])

    
    ########################################
    ######       To String method     ######
    ########################################

    def __str__(self):
        return "Profile = {name: " + self.getName() + ", USBL: " + str(self.getUsbl()) + ", Altimeter: " + str(self.getAltimeter()) + "}"


############################################
######      Other module methods      ######
############################################

def readJSONfile(file):
    """Reads a JSON file and returns the data"""
    if (type(file) != str):
        raise TypeError("File must be a string")
    elif (file == None or file == ""):
        raise ValueError("File can't be None/Null or empty")

    try:
        with open(file) as jsonFile:
            data = json.load(jsonFile)
            return data
    except Exception as e: # TODO - Catch specific exceptions
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
    deserializedProfiles = Profile.deserializeFile("profiles.json")
    print(deserializedProfiles)

    #second_profile = Profile.deserializeClass("profile.json")

    #print(second_profile)