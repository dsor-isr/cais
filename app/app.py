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
import extract_plot_names as epn
import webbrowser
import sys


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
HELP10 = """\nYou can create a new profile to restrict the kind of plots you see. The filters you pick on the profile creation menu are the ones you will see displayed. You can't create a profile if another one with that name already exists"""
HELP11 = """\nThe load and delete options are radio buttons (selecting one deselects the other). After picking the action you want, just pick the profile on the dropdown bellow the radio buttons."""
HELP += '\n' + HELP2 + '\n' + HELP3 + '\n' + HELP4 + '\n' + HELP5 + '\n' + HELP6 + '\n' + HELP7 + '\n' + HELP8 + '\n' + HELP9 + '\n' + HELP10 + '\n' + HELP11
CHANGE_DIR_MESSAGE = "Instead of placing the plots within the CAIS app, you can store them someplace else.\n\nInsert the path to the directory you want to go to. The directory must have the expected structure (see README.md). In particular, the \"root\" directory should be \"days\"."

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

def merge_dictionaries(dict1, dict2):
    if (type(dict1) != dict or type(dict2) != dict):
        raise TypeError("Arguments should be dictionaries")
    
    output = {key: value[:] for key, value in dict1.items()}
    for key in dict2:
        if not key in output:
            output[key] = dict2[key]
        else:
            res = set(output[key]).union(set(dict2[key]))
            output[key] = list(res)

    return output


# Using base64 encoding and decoding
def b64_image(image_filename):
    """Take the path to an image and use base 64 to process file"""

    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def path_cat(path):
    return path[path.find('assets'):]


def merge_html_files(files, merged_html=fn.get_pwd() + ALL_HTML):

    if not type(files) == list or len(files) == 0:
        raise TypeError("merge_html_files: Expected a file of type list with size > 0, but received something else.")

    with open(merged_html, 'w') as merged_file:
        for file in files:
            if (file != ALL_HTML2 or not file.endswith(ALL_HTML2)):
                with open(file, 'r') as f:
                    # Read html files as BeautifulSoup objects and store them
                    contents = f.read()

                    soup = BeautifulSoup(contents, 'lxml')

                merged_file.write(str(soup))


def create_profile(driver_filters, profile_name, plot_filters):
    """Creates a new profile with the given checklist values"""
    if (type(driver_filters) == list and len(driver_filters) == 0):
        driver_filters = epn.get_drivers()
    if (type(plot_filters) == list and len(plot_filters) == 0):
        plot_filters = epn.get_plots()
    
    profile = {'name': profile_name, 'driverFilters': driver_filters, 'plotFilters': plot_filters}
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
    profiles.deleteProfileByName(profile_name)
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


def get_loaded_profile_name():
    """Returns the name of the loaded profile"""

    if (loaded_profile == None):
        return None
    else:
        return loaded_profile['name']
    

def apply_profile_driver_filters(data):
    """Applies the filters of the loaded profile to the data"""

    if (type(data) != list and type(data) != tuple):
        raise TypeError("apply_profile_filters: Expected a list or tuple, but received ", str(type(data)))
    elif (len(data) == 0):
        return data

    if (get_loaded_profile_name() == None):
        # No filters to be applied
        return data

    return profiles.filter(data, loaded_profile, True)


def apply_profile_plot_filters(data):
    """Applies the filters of the loaded profile to the data"""

    if (type(data) != list and type(data) != tuple):
        raise TypeError("apply_profile_filters: Expected a list or tuple, but received ", str(type(data)))
    elif (len(data) == 0):
        return data

    if (get_loaded_profile_name() == None):
        # No filters to be applied
        return data

    return profiles.filter(data, loaded_profile, False, True)


def apply_profile_plot_filters_to_paths(paths):
    """Applies the filters of the loaded profile to the given paths"""

    if (type(paths) != list and type(paths) != tuple):
        raise TypeError("apply_profile_filters: Expected a list or tuple, but received ", str(type(paths)))
    elif (len(paths) == 0):
        return paths

    if (get_loaded_profile_name() == None):
        # No filters to be applied
        return paths
    
    output = apply_profile_plot_filters(paths)

    return output


def reset_upper_directories(dropdown_index):
    """Resets the directories of the upper dropdowns, so that they don't point irrelevant directories"""

    #global last_directories
    for i in range(dropdown_index, len(last_directories)):
        last_directories[i] = home


def treat_fifth_level_dropdown(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[4])

    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories()) or input_value == 'mission specific graphics'):
        # If the path actually changed
        fn.change_directory(last_directories[4])
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

        
        options = apply_profile_plot_filters(options)

        return [{'label': i, 'value': i} for i in options], (), ""
    
    return (), (), ""


def treat_sixth_lvl_dropdown(input_value):

    # Roll back to parent directory
    if (not fn.is_html_file(input_value)):
        fn.change_directory(last_directories[5])

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
            options = []
            fn.change_directory(str(path))
            
            options.extend(fn.get_directories())
            options.extend(fn.get_html_files())
            
            last_directories[6] = path

            return last_dir_options, [{'label': i, 'value': i} for i in options], ""
        elif (input_value in fn.get_html_files()):
            # Prepare plot if it was an html file
                last_dir_options = fn.get_html_files()
                last_dir_options = options = apply_profile_plot_filters(last_dir_options)
                path = fn.extend_dir(str(input_value))
                reset_upper_directories(6) # TODO maybe este não é preciso ???

                return last_dir_options, path, path_cat(path)
    
    return (), (), ""


def merge_button_click():
    files = fn.get_html_files()
    files = apply_profile_plot_filters(files)
    if (len(files) != 0):
        # html files found on present working directory
        merge_html_files(files, fn.get_pwd() + ALL_HTML)
        path = fn.extend_dir(ALL_HTML2)

        sixth_dir_options = fn.get_html_files()
            
        return sixth_dir_options, path, path_cat(path)
    
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

        dbc.ButtonGroup([
            dbc.Button('Plot Directory',
            id='plot button',
            n_clicks=0,
            style={'display':'inline'},
            ),

            dbc.Button(
                "Change search directory", 
                id="change directory button", 
                n_clicks=0,
                style={'display':'inline'},
            ),

            dbc.Button(
                "Help", 
                id="open-help-body-scroll", 
                n_clicks=0,
                style={'display':'inline'},
            )]
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

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Change search directory")),
                dbc.ModalBody([CHANGE_DIR_MESSAGE,
                               html.Br(),
                               dbc.Input(
                                    id="change directory input",
                                    placeholder="Enter directory",
                                    type="text",
                                    value="",
                               ),
                               ]),
                dbc.ModalFooter(
                    dbc.ButtonGroup([
                        dbc.Button(
                            "Change directory",
                            id="change-dir-modal-button",
                            className="ms-auto",
                            n_clicks=0,
                        ),

                        dbc.Button(
                            "Close",
                            id="change-dir-close-body-scroll",
                            className="ms-auto",
                            n_clicks=0,
                        ),
                    ]),
                ),
            ],
            id="change directory modal",
            scrollable=True,
            is_open=False,
            style={'white-space':'pre-line'}
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Error")),
                dbc.ModalBody("The specified directory is either empty or doesn't exist.",
                    id='change-dir-error-message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="change-dir-error-close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    ),
                ),
            ],
            id="change directory error modal",
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
        html.H4("Current Plot:"),
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

        dbc.Button('Plot Profile',
            id='plot profile button',
            n_clicks=0,
            style={'margin-left': '25px'}
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Create Profile")),
                dbc.ModalBody([
                    dbc.ButtonGroup(
                        [
                            dbc.Button("Update dropdowns",
                                id="update dropdowns",
                                className="ms-auto",
                                n_clicks=0),
                        ]
                    ),
                    html.Br(),
                    html.Label("Pick the name of the new profile and the filters you want to apply to it (the ones selected are displayed on the dropdowns). It isn't possible to create a profile if another one already exists with that name."),
                    html.Br(),
                    html.Label('Enter the profile name:'),
                    html.Br(),
                    dcc.Input(value='', type='text', id='profile name'),
                    html.Br(),
                    html.Label("Select the drivers you want to see"),
                    html.Br(),
                    dbc.ButtonGroup([
                        dbc.Button("Select All",
                            id="select all drivers",
                            className="ms-auto",
                            n_clicks=0),
                        dbc.Button("Deselect All",
                            id="deselect all drivers",
                            className="ms-auto",
                            n_clicks=0),
                    ]
                    ),
                    # dbc.RadioItems(
                    #     id="driver radios",
                    #     className="btn-group",
                    #     inputClassName="btn-check",
                    #     labelClassName="btn btn-outline-primary",
                    #     labelCheckedClassName="active",
                    #     options=[
                    #         {"label": "Select All Drivers", "value": 'Select All Drivers', "id": "Select All Drivers"},
                    #         {"label": "Deselect All Drivers", "value": 'Deselect All Drivers', "id": "Deselect All Drivers"},
                    #     ],
                    #     value='Deselect All Drivers',
                    # ),
                    dcc.Dropdown(
                        id='create profile driver dropdown',
                        placeholder = 'Select drivers',
                        options=[],
                        multi=True,
                        clearable=True,
                        style={'color': '#49B0EA'},
                    ),
                    html.Br(),
                    html.Label("Select the specific plots you want to see"),
                    html.Br(),
                    dbc.ButtonGroup([
                        dbc.Button("Select All",
                            id="select all plots",
                            className="ms-auto",
                            n_clicks=0),
                        dbc.Button("Deselect All",
                            id="deselect all plots",
                            className="ms-auto",
                            n_clicks=0),
                    ]
                    ),
                    dcc.Dropdown(
                        id='create profile plots dropdown',
                        placeholder = 'Select specific plots',
                        options=[],
                        multi=True,
                        clearable=True,
                        style={'color': '#49B0EA'},
                ),
                ]),
                dbc.ModalFooter(
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Create",
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
            id='current profile name',
        ),

        html.P(id='center dropdowns', # This is here so the dropdowns won't show up at the top of the page
        style={'height': '8.5%'}),

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

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Plot Profile (ERROR)")),
                dbc.ModalBody([
                    html.Label("An error occured while trying to generate an html file with all plots for the selected profile. One of the likely causes for the error is:\n - No profile was selected\n - No Day was selected on the first dropdown\n - No Vehicle was selected on the second dropdown\n - No Overview was selected on the third dropdown\n\nAll four of these conditions have to be met."),
                ]),
                dbc.ModalFooter(
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Close",
                                id="plot profile error modal close button",
                                className="ms-auto",
                                n_clicks=0),
                        ],
                    ),
                ),
            ],
            id="plot profile error modal",
            scrollable=True,
            is_open=False,
            style={'white-space':'pre-line'},
            size="xl",
        ),

        ##############################
        ####    path to Profile    ###
        ####         plot          ###
        ##############################

        html.Br(),
        html.H4("Current Profile Plot:"),
        dcc.Link('',
        href='',
        target='_blank',
        refresh=True,
        id='plot profile',),


        ##############################
        ####         Timer         ###
        ##############################
        dcc.Interval(
            id='driver json update timer',
            interval=1000 * 60 * 60 * 24, # one week in milliseconds
            n_intervals=0
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

        
        return [{'label': i, 'value': i} for i in options if i not in ('logos')]
    
    return ()


@app.callback(
    Output('Third level dir', 'options'),
    Input('Second level dir', 'value'),
)
def update_third_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[1])

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


        return [{'label': i, 'value': i} for i in options]
    
    return ()


@app.callback(
    Output('Fourth level dir', 'options'),
    Output('Fourth level dir label', 'children'),
    Input('Third level dir', 'value'),
)
def update_fourth_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[2])

    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[2])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[3] = path
        reset_upper_directories(4)

        options = []
        options.extend(fn.get_directories())

        label = ""
        if (input_value.lower() == "overall"):
            label = "4. Specificity"
        elif (input_value.lower() == "missions"):
            label = "4. Missions"


        return [{'label': i, 'value': i} for i in options], label
    
    return (), "4. "

@app.callback(
    Output('Fifth level dir', 'options'),
    Output('Fifth level dir label', 'children'),
    Input('Fourth level dir', 'value'),
)
def update_fifth_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[3])
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
            options = apply_profile_driver_filters(options)
            label = '5. Drivers'


        return [{'label': i, 'value': i} for i in options], label
    
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

    if (fifth_dir == None and n_clicks_plot == 0 and sixth_dir == None):
        return (), (), ''

    if callback_trigger == 'Sixth level dir':
        return treat_sixth_lvl_dropdown(sixth_dir)

    elif callback_trigger == 'plot button':
        # Triggered by merge button
        return merge_button_click()


    elif callback_trigger == 'Fifth level dir':
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
     State("radios", "value"),
     State("create profile plots dropdown", "value")],
)
def profile_callback(n_create_button, n_cancel_button, n_confirm_create,
                             dropdown_val, load_delete_radio_value, is_open, checklist_value, 
                             profile_name, radio_value, plot_filters):
    callback_trigger = ctx.triggered_id

    if (callback_trigger == "create profile button"):
        return True, load_profiles(), build_current_profile_label_string(), "Pick if you want to Load or Delete a profile", get_loaded_profile_name()
    
    elif (callback_trigger == "create modal create button"):
        create_profile(checklist_value, profile_name, plot_filters)

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
    Input("select all drivers", "n_clicks"),
    Input("deselect all drivers", "n_clicks"),
    [State("create profile driver dropdown", "options"),
     State("create profile driver dropdown", "value")],
)
def profile_drivers_dropdown_value(select_all, deselect_all, drivers, selected_drivers):
    callback_trigger = ctx.triggered_id
    if (callback_trigger in ("select all drivers", "deselect all drivers")):
        if (callback_trigger == "select all drivers"):
            return [driver for driver in drivers]
        else:
            return []
    else:
        if (type(selected_drivers) == list):
            return [driver for driver in selected_drivers]
        return []
    

@app.callback(
    Output("create profile plots dropdown", "value"),
    Input("select all plots", "n_clicks"),
    Input("deselect all plots", "n_clicks"),
    [State("create profile plots dropdown", "options"),
     State("create profile driver dropdown", "value"),],
)
def profile_drivers_dropdown_value(select_all, deselect_all, plots, drivers):
    callback_trigger = ctx.triggered_id
    if (callback_trigger == "select all plots"):
        return [plot for plot in plots]
    elif (callback_trigger == "deselect All Plots"):
        return []
    else:
        return []
    

@app.callback(
    Output("create profile driver dropdown", "options"),
    Output("create profile plots dropdown", "options"),
    Input("update dropdowns", "n_clicks"),
    Input("create profile driver dropdown", "value"),
    Input("driver json update timer", "n_intervals"),
)
def profile_drivers_dropdown_value(n_clicks, selected_drivers, n_intervals):
    global home

    # Update drivers.json for each day
    epn.create_drivers_json(home)

    # Get list of days
    days = fn.get_directories(path=home)

    drivers = []
    plots = []
    dictionaries = []
    for day in days:
        file = home + "/" + day + "/drivers.json"
        data = profiles.readJSONfile(file)
        dictionaries.append(data)
        for driver in data:
            if (not driver in drivers):
                drivers.append(driver)
            for plot in data[driver]:
                if (plot not in plots):
                    plots.append(plot)

    if (n_clicks == 0 and selected_drivers in (None, [])):
        return drivers, plots

    if (len(dictionaries) > 1 and (selected_drivers != None and len(selected_drivers) > 0)):
        # Merge all drivers.json into one dictionary
        merged_dict = dictionaries[-1]
        dictionaries.pop()
        for dictionary in dictionaries:
            merged_dict = merge_dictionaries(merged_dict, dictionary)

        plots = profiles.getPlotsByDrivers(selected_drivers, merged_dict)

    return drivers, plots


@app.callback(
    Output("plot profile", "children"),
    Output("plot profile", "href"),
    Output("plot profile error modal", "is_open"),
    Input("plot profile button", "n_clicks"),
    Input("plot profile error modal close button", "n_clicks"),
    [
        State("Home directory", "value"),
        State("Second level dir", "value"),
        State("Third level dir", "value"),
    ]
)
def plot_profile(n_clicks, close, home_dir, second_dir, third_dir):
    callback_trigger = ctx.triggered_id

    if (n_clicks == 0 and home_dir == None and second_dir == None 
        and third_dir == None and close == 0):
        # Do Nothing
        return '', '', False
    if (callback_trigger == "plot profile button"):
        if (home_dir == None or second_dir == None or third_dir == None or 
         get_loaded_profile_name() == None):
            return '', '', True
        else:
            root_dir = home + "/" + home_dir + "/" + "vehicles" + "/" + second_dir + "/" + "plots" + "/"
            root_dir = root_dir + fn.get_directories(path=root_dir)[0] + "/" + third_dir
            files = epn.get_plot_paths(root_dir)
            files = apply_profile_plot_filters_to_paths(files)
            if (len(files) != 0):
                # html files found on present working directory
                path = root_dir + "/" + get_loaded_profile_name() + ".html"
                merge_html_files(files, path)

            return path, path_cat(path), False
    elif (callback_trigger == "plot profile error modal close button"):
        return '', '', False
    
    return '', '', False


@app.callback(
    Output("change directory modal", "is_open"),
    Output("change directory error modal", "is_open"),
    Output("Home directory", "options"),
    Input("change directory button", "n_clicks"),
    Input("change-dir-close-body-scroll", "n_clicks"),
    Input("change-dir-modal-button", "n_clicks"),
    Input("change-dir-error-close-body-scroll", "n_clicks"),
    State("change directory input", "value"),
    State("Home directory", "options"),
)
def change_directory_modal(n_clicks_open, n_clicks_close, n_clicks_save,
                        n_clicks_error, directory, home_dir_options):
    callback_trigger = ctx.triggered_id

    if (n_clicks_open == 0):
        return False, False, home_dir_options
    
    if (callback_trigger == "change directory button"):
        return True, False, home_dir_options
    elif (callback_trigger == "change-dir-close-body-scroll"):
        return False, False, home_dir_options
    elif (callback_trigger == "change-dir-modal-button"):
        if (type(directory) != str or fn.is_valid_directory(directory) == False):
            return True, True, home_dir_options
        else:
            global home
            home = directory
            reset_upper_directories(0)
            fn.change_directory(directory)
            home_dir_options = fn.get_directories()
            return False, False, home_dir_options
    elif (callback_trigger == "change-dir-error-close-body-scroll"):
        return True, False, home_dir_options
        
    return False, False, home_dir_options


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

    # app.run_server(debug=True, dev_tools_hot_reload=False, host='0.0.0.0')  # TODO set debug to False after app is functional

    app.run_server(debug=True, dev_tools_hot_reload=False)  # TODO set debug to False after app is functional
