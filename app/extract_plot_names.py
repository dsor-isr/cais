import os

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


def dfs(vehicle_path=os.getcwd()):
    if not os.path.isdir(vehicle_path):
        raise ValueError("The path provided is not a directory")
    
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
        html_files = [file_name for file_name in dir_content if is_html_file(file_name) 
                      and file_name != "all.html"]
        directories = [file_name for file_name in dir_content if is_dir(path + "/" + file_name)]

        # add plots to output
        output = output.union(set(remove_html_extension_from_files(html_files)))

        for dir in directories:
            file_path = path + "/" + dir
            if os.path.isdir(file_path):
                # Only add directories as nodes with children to the stack
                push_stack(path_stack, file_path)

    return output


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


if __name__ == "__main__":

    print("This script will extract all plot names in the provided directory and all subdirectories")
    print("")
    print("If you don't provide a starting directory, the current working directory will be used")
    print("Current working directory: " + os.getcwd())
    print("")

    answer = ""
    vehicle_path = ""
    while answer != "y" and answer != "n":
        answer = input("Do you want to use the current working directory? (y/n) ")

        if answer == "n":
            print("")
            vehicle_path = process_dir(input("Please provide a starting directory: "))
            print("")
            print("Using directory: " + vehicle_path)
            while not is_dir(vehicle_path):
                vehicle_path = process_dir(input("The path provided is not a directory, please try again: "))

            break
        elif answer == "y":
            print("")
            print("Using current working directory")
            vehicle_path = os.getcwd()
            break
        else:
            print("Invalid input, please try again")

        print("")


    plots = sorted(dfs(vehicle_path))
    plots = [plot for plot in plots if not plot.endswith("copy")]
    print_plots(plots)
    write_to_file("plot_names.txt", plots)