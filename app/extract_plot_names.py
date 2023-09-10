import os
from profiles import profiles

path_stack = []


def pop_stack(path_stack):
    path_stack
    if len(path_stack) > 0:
        return path_stack.pop()
    
    return None


def push_stack(path_stack, path):
    path_stack
    path_stack.append(path)


def remove_html_extension(file_name):
    return file_name.replace('.html', '')


def remove_html_extension_from_files(files):
    return [remove_html_extension(file_name) for file_name in files]


def is_html_file(file_name):
    return file_name.endswith('.html')


def is_dir(file_name):
    return os.path.isdir(file_name)


def dfs(vehicle_path=os.getcwd(), findPlots=True, findDrivers=False):
    if not os.path.isdir(vehicle_path):
        raise ValueError("The path provided is not a directory")
    if (not findPlots and not findDrivers):
        raise ValueError("The flags findPlots and findDrivers can't both be false. Otherwise, the search won't output anything")
    if (findPlots and findDrivers):
        raise ValueError("The flags findPlots and findDrivers can't both be true.")

    path_stack
    push_stack(path_stack, vehicle_path)
    output = set()

    # Depth First Search main loop
    while True:
        path = pop_stack(path_stack)
        if path is None:
            break

        # process plots and directories
        dir_content = os.listdir(path)

        if (findPlots):
            html_files = [file_name for file_name in dir_content if is_html_file(file_name) 
                        and file_name != "all.html"]
            # add plots to output
            output = output.union(set(remove_html_extension_from_files(html_files)))
        elif (findDrivers and path.endswith("drivers")):
            # add drivers to output
            output = output.union(set(dir_content))

        directories = [file_name for file_name in dir_content if is_dir(path + "/" + file_name)]

        # Add directories to stack to continue the search
        for dir in directories:
            file_path = path + "/" + dir
            if os.path.isdir(file_path):
                # Only add directories as nodes with children to the stack
                push_stack(path_stack, file_path)

    return output


def dfs_output_full_path(vehicle_path=os.getcwd()):
    if not os.path.isdir(vehicle_path):
        raise ValueError("The path provided is not a directory")

    path_stack
    push_stack(path_stack, vehicle_path)
    output = set()
    while True:
        path = pop_stack(path_stack)
        if path is None:
            break

        # process plots and directories
        dir_content = os.listdir(path)

        html_files = [path + "/" + file_name for file_name in dir_content if is_html_file(file_name) 
                    and file_name != "all.html"]
        # add plots to output
        output = output.union(set(html_files))

        directories = [file_name for file_name in dir_content if is_dir(path + "/" + file_name)]

        # Add directories to stack to continue the search
        for dir in directories:
            file_path = path + "/" + dir
            if os.path.isdir(file_path):
                # Only add directories as nodes with children to the stack
                push_stack(path_stack, file_path)

    return output


def build_dictionary(plots):
    if (type(plots) not in (list, tuple)):
        raise TypeError("The plots argument must be of type list or tuple")
    if (len(plots) == 0):
        raise ValueError("The plots argument must contain at least one plot")
    
    output = dict()
    for plot in plots:
        lowerCasePlot = plot.lower()
        split = plot.split("/")
        driver = None
        if (not split[-1].endswith(".html")):
            raise ValueError("Something went wrong. Plot doesn't end with .html: " + plot)

        if ("overall" in lowerCasePlot and "drivers" in lowerCasePlot):
            split = plot.split("/")
            if (len(split) < 3):
                raise ValueError("Something went wrong. Path too small for plot: " + plot)
            
            driver = split[-2]
        elif ("missions" in lowerCasePlot or "_mission" in lowerCasePlot):
            driver = "mission specific"

        if (driver != None):
            if (driver in output and split[-1] not in output[driver]):
                output[driver].append(split[-1])
            else:
                output[driver] = [split[-1]]

    return output


def create_drivers_json(path=os.getcwd()):
    if (not os.path.isdir(path)):
        raise ValueError("The path provided is not a directory")
    
    days = os.listdir(path)

    for day in days:
        if (os.path.isdir(path + "/" + day)):
            plots = sorted(dfs_output_full_path(path + "/" + day))
            plots = [plot for plot in plots if not plot.endswith("copy")]
            dictionary = build_dictionary(plots)
            profiles.JSONDump(dictionary, path + "/" + day + "/drivers.json")



def write_to_file(file_name, output):
    with open(file_name, 'w') as f:
        size = len(output)
        for i in range(size):
            if i < size - 1:
                f.write('\'' + output[i] + '\'' + ", ")
            else:
                f.write('\'' + output[i] + '\'')


def process_dir(input_path):
    if input_path[0] == "~":
        return os.path.expanduser(input_path)
    
    return input_path


def print_plots(plots):
    print("\nPlots:")
    for plot in plots:
        print(plot)


def get_plots(path=os.getcwd()):
    output = sorted(dfs(vehicle_path=path))
    output = [plot for plot in output if not plot.endswith("copy")]
    return output


def get_plot_paths(path=os.getcwd()):
    output = sorted(dfs_output_full_path(vehicle_path=path))
    output = [plot for plot in output if not plot.endswith("copy")]
    return output


def get_drivers(path=os.getcwd()):
    output = sorted(dfs(vehicle_path=path, findPlots=False, findDrivers=True))
    output = [driver for driver in output if not driver.endswith("copy")]
    return output


if __name__ == "__main__":
    create_drivers_json("/home/goncalo/cais/app/assets/days")
    # print("This script will extract all plot names in the provided directory and all subdirectories")
    # print("")
    # print("If you don't provide a starting directory, the current working directory will be used")
    # print("Current working directory: " + os.getcwd())
    # print("")

    # answer = ""
    # vehicle_path = ""
    # while answer != "y" and answer != "n":
    #     answer = input("Do you want to use the current working directory? (y/n) ")

    #     if answer == "n":
    #         print("")
    #         vehicle_path = process_dir(input("Please provide a starting directory: "))
    #         print("")
    #         print("Using directory: " + vehicle_path)
    #         while not is_dir(vehicle_path):
    #             vehicle_path = process_dir(input("The path provided is not a directory, please try again: "))

    #         break
    #     elif answer == "y":
    #         print("")
    #         print("Using current working directory")
    #         vehicle_path = os.getcwd()
    #         break
    #     else:
    #         print("Invalid input, please try again")

    #     print("")


    # plots = sorted(dfs(vehicle_path))
    # plots = [plot for plot in plots if not plot.endswith("copy")]
    # print_plots(plots)
    # write_to_file("plot_names.txt", plots)