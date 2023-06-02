import json
import os
import re
import portalocker


class Profile:
    
    class ProfileEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__



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
            print(file)
            data = json.load(jsonFile)
            return data
    except FileNotFoundError as fileNotFoundError:
        raise fileNotFoundError
    except PermissionError as permissionError:
        raise permissionError


def loadProfile(profileName):
    """Loads a profile from the profiles.json file"""
    if (type(profileName) != str):
        raise TypeError("Profile name must be a string")
    elif (profileName == ""):
        raise ValueError("Profile name can't be None/Null or empty")

    deserializedProfiles = []
    try:
        deserializedProfiles = readJSONfile("profiles.json")
    except FileNotFoundError as fileNotFoundError:
        raise fileNotFoundError
    except PermissionError as permissionError:
        raise permissionError
    except Exception as exception:
        raise exception

    for deserializedProfile in deserializedProfiles:
        if (deserializedProfile['name'].lower() == profileName.lower()):
            return deserializedProfile
        
    raise ValueError("Profile doesn't exist")


def serializeClass(profile):
    """Serializes a Profile object into a JSON string"""
    if (type(profile) != dict):
        raise TypeError("Profile must be a Profile object")
    elif (profile == None):
        raise ValueError("Profile can't be None/Null")
    elif (profile['name'] == None or profile['name'] == ""):
        raise ValueError("Profile name can't be None/Null or empty")

    deserializedProfiles = []
    try:
        deserializedProfiles = readJSONfile("profiles.json")
    except FileNotFoundError as fileNotFoundError: # TODO - remove "as" keyword?
        json.dump(profile, open("profiles.json", "w"), indent=4, cls=Profile.ProfileEncoder)
    except PermissionError as permissionError:
        raise permissionError
    except Exception as exception:
        raise exception
    
    for deserializedProfile in deserializedProfiles:
        if (deserializedProfile['name'].lower() == profile['name'].lower()):
            raise ValueError("Profile already exists")
            
    deserializedProfiles.append(profile)
    profiles = deserializedProfiles

    file = open("profiles.json", "w")
    portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE) # Lock file
    json.dump(profiles, file, indent=4, cls=Profile.ProfileEncoder)
    file.close()



def deleteProfileByName(profileName):
    """Deletes a profile from the profiles.json file"""
    if (type(profileName) != str):
        raise TypeError("Profile name must be a string")
    elif (profileName == None or profileName == ""):
        raise ValueError("Profile name can't be None/Null or empty")

    profiles = []
    try:
        deserializedProfiles = readJSONfile("profiles.json")
        foundProfile = False
        for deserializedProfile in deserializedProfiles:
            if (deserializedProfile['name'].lower() == profileName.lower()):
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


def validate_profile(profile):
    if (type(profile) != dict):
        raise TypeError("Profile must be a dictionary")
    if (not 'name' in profile or not 'driverFilters' in profile or not 'plotFilters' in profile):
        raise ValueError("Profile must contain name, driverFilters and plotFilters")
    if (type(profile['name']) != str):
        raise TypeError("Profile name must be a string")
    if (['name'] == ""):
        raise ValueError("Profile name can't be empty")
    if (type(profile['driverFilters']) != list):
        raise TypeError("Profile driverFilters must be a list")
    if (type(profile['plotFilters']) != list):
        raise TypeError("Profile plotFilters must be a list")
    

def filter(files, profile, filterDrivers=False, filterPlots=False):
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
    if (type(profile) != dict):
        raise TypeError("Profile must be a dictionary")

    for file in files:
        if (type(file) != str):
            raise TypeError("Files must be a list or tuple of strings")
        elif (file == None or file == ""):
            raise ValueError("Files can't contain None/Null or empty strings")
        
    filtered_files = [file for file in files]
    if (filterDrivers):
        filtered_files = __filter_drivers(files, profile['driverFilters'])
    elif (filterPlots):
        filtered_files = __filter_plots(files, profile['plotFilters'])

    return filtered_files
            

def __filter_drivers(files, driverFilters):
    output_files = [file for file in files]
    for file in files:
        lowerCaseFile = file
        if (not lowerCaseFile in driverFilters):
            output_files.remove(file)

    return output_files


def __filter_plots(files, plotFilters):
    output_files = [file for file in files]
    for file in files:
        processedFile = file
        processedFile = processedFile.replace('.html', '')
        if (not processedFile in plotFilters):
            output_files.remove(file)

    return output_files


############################################
######       Test the class           ######
############################################

if __name__ == '__main__':

   pass