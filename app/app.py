# Run this app with 'python3 app.py' and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from file_navigation import file_navigation as fn
from profiles import profiles
import base64
from bs4 import BeautifulSoup
import copy
import re


##############################
###    Suggested Debug     ###
###         Format         ###
##############################

"""print("(callback) <function_name>: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
print("		(callback) <function_name>: other useful things")
print("")
"""

##############################
###        Constants       ###
##############################

ALL_HTML = '/all.html'
ALL_HTML2 = 'all.html'
PLOTS = 'plots'
DRIVERS = 'drivers'
VEHICLES = 'vehicles'

FILTER_NAMES = ["usbl", "altimeter", "depthCell", "gps", "imu", "insidePressure", "batMonit", 'thrusters']
NUM_FILTERS = len(FILTER_NAMES)
USBL_EXTENSIONS = ["USBL (send)", "USBL (recv)", "USBL (sensors_usbl_fix)"]

HELP = """The Cluster of Analysis for Intelligent Systems (CAIS) is a data visualization tool, developed for analysis of data gathered by the vehicles and robots developed at ISR\'s Dynamical Systems and Ocean Robotics lab."""
HELP2 = """\nIt works by taking advantage of the tree like nature of the machine\'s file system. Any directory or html file placed somewhere on the Assets/ directories sub-tree (Assets is on the same folder as the executable) will be detected by CAIS. All one has to do is select what they wish to see on each dropdown menu. CAIS then follows that path on the file system to display the already plotted graphs."""
HELP3 = """\nAfter a particular .html file is selected, a hyperlink will appear. Once clicked, it opens a new tab with the plot."""
HELP4 = """\nAdditionally, if the button "Plot Directory" is clicked, it generates a all.html file on the current directory by concatenating all other html files on that directory. If there are no html, nothing will be generated.\nThe CAIS web application is built using Dash Plotly (a Flask based framework). By default, Dash servers run with a flag called \'Hot Reloading\'. This means that whenever a file is saved within the Assets folder or on any part of it\'s directory sub-tree, Dash reloads the application page, losing its current state. To avoid this, the server should be run with app.py containing the following line of code:"""
HELP5 = """app.run_server(debug=False, dev_tools_hot_reload=False)"""
HELP6 = """\nWhenever a file is saved (including app.py itself) or a directory is created/deleted, you should either:"""
HELP7 = """a) Refresh the web page"""
HELP8 = """b) Change the first drop down"""
HELP9 = """c) Run app.py again"""
HELP10 = """\nYou can create a new profile to restrict the kind of plots you see. The filters you pick on the profile creation menu are the ones you won't see displayed. You can't create a profile if another one with that name already exists"""
HELP11 = """\nThe load and delete options are radio buttons (selecting one deselects the other). After picking the action you want, just pick the profile on the dropdown bellow the radio buttons."""
HELP += '\n' + HELP2 + '\n' + HELP3 + '\n' + HELP4 + '\n' + HELP5 + '\n' + HELP6 + '\n' + HELP7 + '\n' + HELP8 + '\n' + HELP9 + '\n' + HELP10 + '\n' + HELP11

PATH_TO_PROFILES = fn.extend_dir('profiles')

##############################
###    Global Variables    ###
##############################

home = fn.extend_dir('assets')
home = fn.build_dir('days', home)
loaded_profile = None
last_directories = [home, home, home, home, home, home, home]

host = 'http://127.0.0.1:8050/'

dsor_logo = 'assets/logos/DSOR_logo_v05a.jpg'
isr_logo = 'assets/logos/isr_logo_red_background.png'


##############################
###   Auxilary Functions   ###
##############################

# Using base64 encoding and decoding
def b64_image(image_filename):
    """Take the path to an image and use base 64 to process file"""

    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def path_cat(path):
    return path[path.find('assets'):]


def filter(files):
    """Take a list or tuple of files and filter them based on the current
    loaded profile."""
    if type(files) != str or type(files) != tuple:
        raise TypeError("filter: Expect a list or tuple of files but received ", str(type(files)))
    if loaded_profile == None:
        raise RuntimeError("filter: No profile has been loaded")
    
    return loaded_profile.filter(files)


def merge_html_files(files):

    if not type(files) == list or len(files) == 0:
        raise TypeError("merge_html_files: Expected a file of type list with size > 0, but received something else.")

    soup_objects = []

    # Iterate over the files
    for file in files:
        if (file != ALL_HTML2):
            # This if prevents from concatenating old all.html files
            with open(file, 'r') as f:
                # Read html files as BeautifulSoup objects and store them
                contents = f.read()

                soup = BeautifulSoup(contents, 'lxml')
                soup_objects.append(soup)

    output_file = soup_objects[0]

    # Append the contents of each html to a baseline html file
    for soup in soup_objects[1::]:
        for element in soup.body:
            output_file.body.append(copy.copy(element))


    # Save the new merged html file in the file system
    merged_html = fn.get_pwd() + ALL_HTML
    with open(merged_html, "w", encoding='utf-8') as file:
        file.write(str(output_file))


def create_profile(checklist_values, profile_name):
    """Creates a new profile with the given checklist values"""
    
    profile = {'name': profile_name, 'filters': checklist_values}
    if (type(profile_name) != str):
        raise TypeError("create_profile: Expected a string for profile_name but received ", str(type(profile_name)))
    elif (profile_name == ""):
        raise ValueError("create_profile: profile_name is empty")

    pwd = fn.get_pwd()
    fn.change_directory(PATH_TO_PROFILES)
    try:
        profiles.serializeClass(profile)
    except ValueError as e:
        pass
    fn.change_directory(pwd)


def delete_profile(profile_name):
    """Deletes a profile with the given name"""

    if (type(profile_name) != str):
        raise TypeError("delete_profile: Expected a string for profile_name but received ", str(type(profile_name)))
    elif (profile_name == ""):
        raise ValueError("delete_profile: profile_name is empty")

    pwd = fn.get_pwd()
    fn.change_directory(PATH_TO_PROFILES)
    profiles.Profile.deleteProfileByName(profile_name)
    fn.change_directory(pwd)


def load_profiles():
    path = fn.build_dir("profiles.json", PATH_TO_PROFILES)
    profile_names = []
    if (fn.is_valid_file(path)):
        deserialized_profiles = profiles.readJSONfile(path)
        for profile in deserialized_profiles:
            profile_names.append(profile['name'])

    return profile_names


def load_profile(profile_name):
    """Loads a profile with the given name"""

    if (type(profile_name) != str):
        raise TypeError("load_profile: Expected a string for profile_name but received ", str(type(profile_name)))
    elif (profile_name == ""):
        raise ValueError("load_profile: profile_name is empty")

    pwd = fn.get_pwd()
    fn.change_directory(PATH_TO_PROFILES)
    global loaded_profile
    loaded_profile = profiles.loadProfile(profile_name)
    fn.change_directory(pwd)


def unload_profile():
    """Unloads the currently loaded profile"""

    global loaded_profile
    loaded_profile = None


def build_current_profile_label_string():
    """Builds the string that will be displayed in the current profile label"""

    return "Current Profile: {}".format(str(get_loaded_profile_name()))


def checklist_filters_to_booleans(checklist_values):
    """Converts the values of the checklist to booleans"""

    if (checklist_values == None):
        raise ValueError("checklist_filters_to_booleans: checklist_values is None")
    if (type(checklist_values) != list and type(checklist_values) != tuple):
        raise TypeError("checklist_filters_to_booleans: Expected a list or tuple, but received ", str(type(checklist_values)))

    print("checklist_values: ", checklist_values)
    booleans = [False for i in range(NUM_FILTERS)]
    for i in checklist_values:
        if (type(i) != str):
            raise TypeError("checklist_filters_to_booleans: Expected a list of strings, but received a list with a non-string element")
        
        if (i in FILTER_NAMES):
            index = FILTER_NAMES.index(i)
            booleans[index] = True
        else:
            raise ValueError("checklist_filters_to_booleans: At least one of the values of the checklist is not a valid filter")

    return booleans


def get_loaded_profile_name():
    """Returns the name of the loaded profile"""

    if (loaded_profile == None):
        return None
    else:
        return loaded_profile['name']

def apply_profile_filters(data):
    """Applies the filters of the loaded profile to the data"""

    if (type(data) != list and type(data) != tuple):
        raise TypeError("apply_profile_filters: Expected a list or tuple, but received ", str(type(data)))
    elif (len(data) == 0):
        raise ValueError("apply_profile_filters: data is empty")

    if (get_loaded_profile_name() == None):
        # No filters to be applied
        return data

    return loaded_profile.filter(data)


def reset_upper_directories(dropdown_index):
    """Resets the directories of the upper dropdowns, so that they don't point irrelevant directories"""

    #global last_directories
    #print("reset_upper_directories: home = ", home)

    for i in range(dropdown_index, len(last_directories)):
        #print("reset_upper_directories: (before) i = " + str(i) + " ; last_directories[i] = ", last_directories[i])
        last_directories[i] = home
        #print("reset_upper_directories: (after) i = " + str(i) + " ; last_directories[i] = ", last_directories[i])


def treat_fifth_level_dropdown(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[4])

    #print("(callback) treat_fifth_level_dropdown: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) treat_fifth_level_dropdown: fn.get_directories()", fn.get_directories())
    #print("     (callback) treat_fifth_level_dropdown: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories()) or input_value == 'mission specific graphics'):
        # If the path actually changed
        fn.change_directory(last_directories[4])
        label_6 = '6. Plots'
        label_7 = '7. '
        options = []
        if (re.search("mission specific graphics", input_value) == None):
            path = fn.extend_dir(input_value)
            fn.change_directory(str(path))
            last_directories[5] = path
            reset_upper_directories(6)

            options.extend(fn.get_html_files())
        else:
            reset_upper_directories(5)
            options.extend(fn.get_html_files())

        
        #fn.change_directory(last_directories[4])
        #path = fn.extend_dir(input_value)
        #fn.change_directory(str(path))
        #last_directories[5] = path

        #print("     (callback) treat_fifth_level_dropdown: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options], (), ""
    
    #print("")
    return (), (), ""


def treat_sixth_lvl_dropdown(input_value):

    # Roll back to parent directory
    if (not fn.is_html_file(input_value)):
        fn.change_directory(last_directories[5])

    #print("(callback) treat_sixth_lvl_dropdown: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) treat_sixth_lvl_dropdown: fn.get_directories()", fn.get_directories())
    #print("     (callback) treat_sixth_lvl_dropdown: fn.get_html_files()", fn.get_html_files())
    #print("     (callback) treat_sixth_lvl_dropdown: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    #print("     (callback) treat_sixth_lvl_dropdown: input_value in fn.get_html_files()", str(input_value in fn.get_html_files()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value))):
        # If the path actually changed
        if (input_value in (fn.get_directories() + USBL_EXTENSIONS)):
            # Extend path if it was a directory
            last_dir_options = fn.get_directories()
            if (re.search("missions", fn.get_pwd()) != None):
                # If previously chose missions, instead of overall
                last_dir_options += USBL_EXTENSIONS
                last_dir_options.remove("USBL")
            fn.change_directory(last_directories[5])
            path = fn.extend_dir(input_value)
            #fn.change_directory(str(path))
            options = []
            #print("input value = " + input_value +" ; USBL_EXTENSIONS = ", USBL_EXTENSIONS)
            #print("input_value in USBL_EXTENSIONS = ", str(input_value in USBL_EXTENSIONS))
            if (input_value in USBL_EXTENSIONS):
                # USBL requires an extra directory jump to reach the html files
                #print("     (callback) treat_sixth_lvl_dropdown: Picked a type of USBL. Extending accordingly")
                path = fn.extend_dir("USBL")
                fn.change_directory(str(path))
                if (re.search("(send)", input_value) != None):
                    path = fn.extend_dir("send")
                elif (re.search("(sensors_usbl_fix)", input_value) != None):
                    path = fn.extend_dir("sensors_usbl_fix")
                elif (re.search("(recv)", input_value) != None):
                    path = fn.extend_dir("recv")
            fn.change_directory(str(path))
            
            #print("     (callback) treat_sixth_lvl_dropdown: pwd = ", fn.get_pwd())
            options.extend(fn.get_directories())
            options.extend(fn.get_html_files())
            
            last_directories[6] = path

            #print("     (callback) treat_sixth_lvl_dropdown: options = ", options)
            #print("")

            return last_dir_options, [{'label': i, 'value': i} for i in options], ""
        elif (input_value in fn.get_html_files()):
            # Prepare plot if it was an html file
                #print("\t\tupdate_sixth_level_dir: Adding html file to the plot")
                last_dir_options = fn.get_html_files()
                #print("last_dir_options = ", last_dir_options)
                path = fn.extend_dir(str(input_value))
                reset_upper_directories(6) # TODO maybe este não é preciso ???

                return last_dir_options, path, path_cat(path)
    
    #print("")
    return (), (), ""


def merge_button_click():
    files = fn.get_html_files()
    if (len(files) != 0):
        # html files found on present working directory
        #print("     (callback) merge_button_click: Going to merge files")
        #print("     (callback) merge_button_click: last_directories = ", last_directories)
        #print("     (callback) merge_button_click: last_directories[5] = ", last_directories[5])
        #print("     (callback) merge_button_click: last_directories[6] = ", last_directories[6])
        merge_html_files(files)
        path = fn.extend_dir(ALL_HTML2)

        sixth_dir_options = fn.get_html_files()
            
        #print("     (callback) merge_button_click: pwd = ", fn.get_pwd())
        return sixth_dir_options, path, path_cat(path)
    
    #print("     (callback) merge_button_click: No html files found on present working directory. Not merging files.")
    
    return [{'label': i, 'value': i} for i in files], (), ''


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


##############################
###     Custom Bootstrap   ###
###        Components      ###
##############################


# Nav/Footer placed at the bottom of the html page
nav = dbc.Nav(
    [
        html.Br(),
        dbc.NavItem(dbc.NavLink("Institute for Systems and Robotics", href="https://welcome.isr.tecnico.ulisboa.pt/")),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Dynamical Systems and Ocean Robotics", href="https://welcome.isr.tecnico.ulisboa.pt/projects_cat/dsor/")),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Instituto Superior Técnico", href="https://tecnico.ulisboa.pt/pt/")),
        html.Br(),

    ], style={'position':'fixed', 'bottom':0, 'width':'100%'},
)


##############################
###        HTML Layout     ###
##############################


load_figure_template('CERULEAN')

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

server = app.server


app.layout = html.Div([
    
    nav,
    
    ##############################
    ####      First Div      #####
    ##############################
    
    html.Div(children=[
        
        ##############################
        ###         Logos          ###
        ##############################
        
        html.Img(src=b64_image(isr_logo),
        id='ISR logo',
        style={'position':'sticky', 'height':'20%', 'display':'inline'},
        ),
        
        html.Img(src=b64_image(dsor_logo),
        id='DSOR logo',
        style={'position':'sticky', 'height':'20%', 'width':'30%', 'display':'inline'},
        ),
        
        html.H1('Cluster of Analysis for Intelligent Systems'),


        ##############################
        ####        Buttons        ###
        ##############################

        dbc.Button('Plot Directory',
        id='plot button',
        n_clicks=0,
        style={'display':'inline'},
        ),

        dbc.Button(
            "Help", 
            id="open-help-body-scroll", 
            n_clicks=0,
            style={'display':'inline'},
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Help")),
                dbc.ModalBody(HELP),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-help-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-help-body-scroll",
            scrollable=True,
            is_open=False,
            style={'white-space':'pre-line'}
        ),
        
        
        ##############################
        ####   Left   Dropdowns    ###
        ##############################
        
        html.Br(),
        html.Label('1. Day'),
        dcc.Dropdown([{'label': i, 'value': i} for i in fn.get_directories(path=home) if (i not in {'logos'})],
        id='Home directory'),

        html.Br(),
        html.Label('2. Vehicle'),
        dcc.Dropdown((),
        id='Second level dir'),

        html.Br(),
        html.Label('3. Overview'),
        dcc.Dropdown((),
        id='Third level dir'),


        ##############################
        ####     path to HTML      ###
        ##############################

        html.Br(),
        dcc.Link('',
        href='',
        target='_blank',
        refresh=True,
        id='plot',),


        html.P(id='placeholder') # TODO remove later

    ], style={'padding': 10, 'flex': 1}),

    ##############################
    ####      Second Div     #####
    ##############################

    html.Div(children=[
    
        ##############################
        ####     Radio Items       ###
        ##############################

        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Load Profile", "value": 'Load Profile', "id": "load profile button"},
                {"label": "Delete Profile", "value": 'Delete Profile', "id": "delete profile button"},
            ],
            value='Load Profile',
        ),

        ##############################
        ####        Buttons        ###
        ##############################

        dbc.Button('Create Profile',
            id='create profile button',
            n_clicks=0,
            style={'margin-left': '25px'}
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Create Profile")),
                dbc.ModalBody("Pick the name of the new profile and the filters you want to apply to it (the ones selected won't be displayed on the dropdowns). It isn't possible to create a profile if another one already exists with that name."),
                html.Label('Enter the profile name:'),
                dcc.Input(value='', type='text', id='profile name'),
                dcc.Checklist(['gps', 'depthCell', 'altimeter', 'insidePressure', 'usbl', 'imu', 'batMonit', 'thrusters'],
                    inputStyle={"margin-right": "5px", 'margin-left': '20px'},
                    id='create profile checklist',
                ),
                html.Br(),
                html.Label("Select the drivers you want to see"),
                dbc.RadioItems(
                    id="driver radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Select All Drivers", "value": 'Select All Drivers', "id": "Select All Drivers"},
                        {"label": "Deselect All Drivers", "value": 'Deselect All Drivers', "id": "Deselect All Drivers"},
                    ],
                    value='Deselect All Drivers',
                ),
                dcc.Dropdown(
                    id='create profile driver dropdown',
                    placeholder = 'Select drivers',
                    options=['gps', 'depthCell', 'altimeter', 'insidePressure', 'usbl', 'imu', 'batMonit', 'thrusters'],
                    multi=True,
                    clearable=True,
                    style={'color': '#49B0EA'},
                ),
                html.Label("Select the specific plots you want to see"),
                dbc.RadioItems(
                    id="plots radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Select All Plots", "value": 'Select All Plots', "id": "Select All Plots"},
                        {"label": "Deselect All Plots", "value": 'Deselect All Plots', "id": "Deselect All Plots"},
                    ],
                    value='Deselect All Plots',
                ),
                dcc.Dropdown(
                    id='create profile plots dropdown',
                    placeholder = 'Select specific plots',
                    options=['control_surge.html', 'overview_filter_dr_usbl.html', 'filter_vs_virtual_target.html', 'overview_pf.html', 'crossTrackAlongTrack.html'],
                    multi=True,
                    clearable=True,
                    style={'color': '#49B0EA'},
                ),
                dbc.ModalFooter(
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "create",
                                id="create modal create button",
                                className="ms-auto",
                                n_clicks=0),
                            dbc.Button("Cancel",
                                id="create modal cancel button",
                                className="ms-auto",
                                n_clicks=0),
                        ],
                    ),
                ),
            ],
            id="create profile modal",
            scrollable=True,
            is_open=False,
            style={'white-space':'pre-line'},
            size="xl",
        ),
        dcc.Store(id='create profile checklist memory'),
        html.Div(id="output"),

        ##############################
        ####   Right   Dropdowns   ###
        ##############################

        html.Label(children='placeholder',
        id='load delete label'),
        dcc.Dropdown((),
        id='Load Delete Dropdown',
        ),
        html.Label(
            children="Current Profile: {}".format(str(get_loaded_profile_name())),
            id='current profile name',),

        html.P(id='center dropdowns', # This is here so the dropdowns won't show up at the top of the page
        style={'height': '8%'}),

        html.Br(),
        html.Label(children='4. ',
        id='Fourth level dir label'),
        dcc.Dropdown((),
        id='Fourth level dir'),

        html.Br(),
        html.Label(children='5. ',
        id='Fifth level dir label'),
        dcc.Dropdown((),
        id='Fifth level dir',
        ),

        html.Br(),
        html.Label(children='6. Plots',
        id='Sixth level dir label'),
        dcc.Dropdown((),
        id='Sixth level dir',
        ),
    
    ], style={'padding': 10, 'flex': 1}),
    

], style={'display': 'flex', 'flex-direction': 'row'})


##############################
###   Callback Functions   ###
##############################


@app.callback(
    Output('Second level dir', 'options'),
    Input('Home directory', 'value'),
)
def update_second_level_dir(input_value):
    #print("(callback) update_second_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_second_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_second_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    # Roll back to parent directory
    fn.change_directory(last_directories[0])
    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(),input_value)):
        # If the path actually changed
        path = fn.extend_dir(input_value)
        path = fn.build_dir(VEHICLES, path)
        fn.change_directory(str(path))
        last_directories[1] = path
        reset_upper_directories(2)

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_second_level_dir: options = ", options)
        #print("")
        
        return [{'label': i, 'value': i} for i in options if i not in ('logos')]
    
    #print("")
    return ()


@app.callback(
    Output('Third level dir', 'options'),
    Input('Second level dir', 'value'),
)
def update_third_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[1])

    #print("(callback) update_third_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_third_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_third_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[1])

        # Skip irrelevant directories
        path = fn.extend_dir(input_value)
        valid_dir = fn.is_valid_directory(path)
        if (valid_dir):
            # Check if plots subdirectory exists
            path = fn.build_dir(PLOTS, path)
            valid_dir = fn.is_valid_directory(path)
        if (valid_dir and len(fn.get_directories(True, path)) > 0):
            # Check if any plots were actually produced
            path = fn.build_dir(fn.get_directories(True, path)[0], path)
        else:
            return ()
        
        fn.change_directory(str(path))
        last_directories[2] = path
        reset_upper_directories(3)

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_third_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options]
    
    #print("")
    return ()


@app.callback(
    Output('Fourth level dir', 'options'),
    Output('Fourth level dir label', 'children'),
    Input('Third level dir', 'value'),
)
def update_fourth_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[2])

    #print("(callback) update_fourth_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_fourth_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_fourth_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[2])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[3] = path
        reset_upper_directories(4)

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        label = ""
        if (input_value.lower() == "overall"):
            label = "4. Specificity"
        elif (input_value.lower() == "missions"):
            label = "4. Missions"

        #print("     (callback) update_fourth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options], label
    
    #print("")
    return (), "4. "

@app.callback(
    Output('Fifth level dir', 'options'),
    Output('Fifth level dir label', 'children'),
    Input('Fourth level dir', 'value'),
)
def update_fifth_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[3])

    #print("(callback) update_fifth_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_fifth_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_fifth_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[3])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[4] = path
        reset_upper_directories(5)

        options = []
        options.extend(fn.get_directories())
        label = "5. "
        if (re.search("mission", input_value) != None):
            options.extend(["mission specific graphics"])
            label = '5. Mission details'
        else:
            options.extend(fn.get_html_files()) # TODO - is this extended necessary?
            print("     (callback) update_fifth_level_dir: options = ", options)
            options = apply_profile_filters(options)
            label = '5. Drivers'

        #print("     (callback) update_fifth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options], label
    
    #print("")
    return (), '5. '


@app.callback(
    Output('Sixth level dir', 'options'),
    Output('plot', 'children'),
    Output('plot', 'href'),
    Input('Sixth level dir', 'value'),
    Input('plot button', 'n_clicks'),
    Input('Fifth level dir', 'value'),
)
def update_seventh_level_dir(sixth_dir, n_clicks_plot, fifth_dir):
    callback_trigger = ctx.triggered_id

    #print("(callback) update_seventh_level_dir: \n\tInput = {" + str(sixth_level_dir) + ", " + str(seventh_dir) + ", " + str(eighth_dir) + ", " + str(n_clicks_plot) + "}")
    #print("\tpath = ", fn.get_pwd())

    if (fifth_dir == None and n_clicks_plot == 0 and sixth_dir == None):
        return (), (), ''

    if callback_trigger == 'Sixth level dir':
        # Triggered by directory change
        #print("     (callback) update_seventh_level_dir: Callback triggered by directory change (Seventh level dir)")
        return treat_sixth_lvl_dropdown(sixth_dir)

    elif callback_trigger == 'plot button':
        # Triggered by merge button
        #print("     (callback) update_seventh_level_dir: Callback triggered by merge button")
        return merge_button_click()


    elif callback_trigger == 'Fifth level dir':
        #print("     (callback) update_seventh_level_dir: Callback triggered by directory change (Sixth level dir)")
        return treat_fifth_level_dropdown(fifth_dir)

    return (), (), ''


app.callback(
    Output("modal-help-body-scroll", "is_open"),
    [
        Input("open-help-body-scroll", "n_clicks"),
        Input("close-help-body-scroll", "n_clicks"),
    ],
    [State("modal-help-body-scroll", "is_open")],
)(toggle_modal)


@app.callback(
    Output("create profile modal", "is_open"),
    Output("Load Delete Dropdown", "options"),
    Output("current profile name", "children"),
    Output("load delete label", "children"),
    Output("Load Delete Dropdown", "value"),
    [
        Input("create profile button", "n_clicks"),
        Input("create modal cancel button", "n_clicks"),
        Input("create modal create button", "n_clicks"),
        Input("Load Delete Dropdown", "value"),
        Input("radios", "value"),
    ],
    [State("create profile modal", "is_open"),
     State("create profile driver dropdown", "value"),
     State('profile name', 'value'),
     State("radios", "value"),],
)
def profile_callback(n_create_button, n_cancel_button, n_confirm_create,
                             dropdown_val, load_delete_radio_value, is_open, checklist_value, 
                             profile_name, radio_value):
    callback_trigger = ctx.triggered_id

    if (callback_trigger == "create profile button"):
        return True, load_profiles(), build_current_profile_label_string(), "Pick if you want to Load or Delete a profile", get_loaded_profile_name()
    
    elif (callback_trigger == "create modal create button"):
        create_profile(checklist_value, profile_name)

    elif (callback_trigger == "radios" and radio_value == "Delete Profile"):
        return False, load_profiles(), build_current_profile_label_string(), load_delete_radio_value, None

    elif (callback_trigger == "Load Delete Dropdown" and dropdown_val != None):
        if (radio_value == "Load Profile"):
            load_profile(dropdown_val)

        elif (radio_value == "Delete Profile"):

            if ((get_loaded_profile_name() != None) and 
                (dropdown_val == get_loaded_profile_name())):
                # If the profile to delete is the loaded one
                unload_profile()

            delete_profile(dropdown_val)

    return False, load_profiles(), build_current_profile_label_string(), load_delete_radio_value, get_loaded_profile_name()


@app.callback(
    Output("create profile driver dropdown", "value"),
    Input("driver radios", "value"),
    [State("create profile driver dropdown", "options"),],
)
def profile_drivers_dropdown(input_value, drivers):
    if (input_value == "Select All Drivers"):
        return [driver for driver in drivers]
    elif (input_value == "Deselect All Drivers"):
        return []
    else:
        return []
    

@app.callback(
    Output("create profile plots dropdown", "value"),
    Input("plots radios", "value"),
    [State("create profile plots dropdown", "options"),],
)
def profile_drivers_dropdown(input_value, plots):
    if (input_value == "Select All Plots"):
        return [plot for plot in plots]
    elif (input_value == "Deselect All Plots"):
        return []
    else:
        return []

##############################
###      Main Function     ###
##############################

if __name__ == '__main__':

    ###########################################################################
    ####                                                                   ####
    ####  Warning: By default, Dash applications run with Hot Reload       ####
    ####    enabled. This means that everytime the code is changed or a    ####
    ####    file is saved in the working directory, it reloads the app.    ####
    ####    Since Dash applications are stateless, it resets everything.   ####
    ####                                                                   ####
    ####    For CAIS, this is mostly an issue when merging html files.     ####
    ####    To prevent problems, always run the server with                ####
    ####    dev_tools_hot_reload=False.                                    ####
    ####                                                                   ####
    ####    If you add new folders or files manually or with a script,     ####
    ####    you need to restart the application or refresh the page/change ####
    ####    one of the upper dropdowns.                                    ####
    ####                                                                   ####
    ####    For more on this, read: https://dash.plotly.com/devtools       ####
    ####    and https://github.com/plotly/dash/issues/1293                 ####
    ####                                                                   ####
    ###########################################################################

    app.run_server(debug=True, dev_tools_hot_reload=False)  # TODO set debug to False after app is fully functional