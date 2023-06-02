import json
import os
import re
import portalocker


class Profile:
    
    class ProfileEncoder(json.JSONEncoder):
        """Class used to serialize profiles into a JSON string"""
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
    """Loads a profile from the profiles.json file
    
    Parameters
    ----------
        profileName: str
            The name of the profile to load"""
    if (type(profileName) != str):
        raise TypeError("Profile name must be a string")
    elif (profileName == ""):
        raise ValueError("Profile name can't be empty")

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
    """Serializes a Profile object into a JSON string
    
    Parameters
    ----------
        profile: dict
            The profile object to serialize"""
    if (type(profile) != dict):
        raise TypeError("Profile must be a dictionary object")
    elif (profile == None):
        raise ValueError("Profile can't be None/Null")
    else:
        try:
            if (profile['name'] == None or profile['name'] == ""):
                raise ValueError("Profile name can't be None/Null or empty")
        except KeyError as keyError:
            raise KeyError("Profile must have a name")

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
    """Deletes a profile from the profiles.json file
    
    Parameters
    ----------
        profileName: str
            The name of the profile to delete"""
    if (type(profileName) != str):
        raise TypeError("Profile name must be a string")
    elif (profileName == ""):
        raise ValueError("Profile name can't be empty")

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
    """Validates a profile
    
    Parameters
    ----------
        profile: dict
            The profile to validate"""
    if (type(profile) != dict):
        raise TypeError("Profile must be a dictionary")
    elif (len(profile) == 0):
        raise ValueError("Profile can't be an empty dictionary")
    if (not 'name' in profile or not 'driverFilters' in profile or not 'plotFilters' in profile):
        raise ValueError("Profile must contain name, driverFilters and plotFilters")
    if (type(profile['name']) != str):
        raise TypeError("Profile name must be a string")
    if (profile['name'] == ""):
        raise ValueError("Profile name can't be empty")
    if (type(profile['driverFilters']) != list):
        raise TypeError("Profile driverFilters must be a list")
    elif (len(profile['driverFilters']) == 0):
        raise ValueError("Profile driverFilters can't be empty")
    if (type(profile['plotFilters']) != list):
        raise TypeError("Profile plotFilters must be a list")
    elif (len(profile['plotFilters']) == 0):
        raise ValueError("Profile plotFilters can't be empty")
    
    for driverFilter in profile['driverFilters']:
        if (type(driverFilter) != str):
            raise TypeError("Profile driverFilters must be a list of strings")
        elif (driverFilter == ""):
            raise ValueError("Profile driverFilters can't contain empty strings")
        
    for plotFilter in profile['plotFilters']:
        if (type(plotFilter) != str):
            raise TypeError("Profile plotFilters must be a list of strings")
        elif (plotFilter == ""):
            raise ValueError("Profile plotFilters can't contain empty strings")
    

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
    """Filters the files based on the driver filters
    
    Parameters
    ----------
        files: list
            list of files to filter
        driverFilters: list
            list of driver filters
    """
    if (type(files) not in (list, tuple)):
        raise TypeError("Files must be a list or tuple")
    if (type(driverFilters) not in (list, tuple)):
        raise TypeError("Driver filters must be a list or tuple")

    output_files = [file for file in files]
    for file in files:
        if (type(file) != str):
            raise TypeError("Files must be a list or tuple of strings")
        elif (file == ""):
            raise ValueError("Files can't contain empty strings")
        lowerCaseFile = file
        if (not lowerCaseFile in driverFilters):
            output_files.remove(file)

    return output_files


def __filter_plots(files, plotFilters):
    """Filters the files based on the plot filters

    Parameters
    ----------
        files: list
            list of files to filter
        plotFilters: list
            list of plot filters
    """
    if (type(plotFilters) not in (list, tuple)):
        raise TypeError("Plot filters must be a list or tuple")
    if (type(files) not in (list, tuple)):
        raise TypeError("Files must be a list or tuple")
    
    output_files = [file for file in files]
    for file in files:
        processedFile = file
        processedFile = processedFile.replace('.html', '')
        if (not processedFile in plotFilters):
            output_files.remove(file)

    return output_files



if __name__ == '__main__':
   pass