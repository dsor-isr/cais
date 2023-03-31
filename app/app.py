# Run this app with 'python3 app.py' and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import file_navigation as fn
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
HELP += '\n' + HELP2 + '\n' + HELP3 + '\n' + HELP4 + '\n' + HELP5 + '\n' + HELP6 + '\n' + HELP7 + '\n' + HELP8 + '\n' + HELP9

##############################
###    Global Variables    ###
##############################

#home = fn.get_pwd()
home = fn.extend_dir('assets')
home = fn.build_dir('days', home)
#print("home = ", home)
#print("content = ", fn.get_directories(path=home))
last_directories = [home, home, home, home, home, home, home]
#fn.change_directory(home)

host = 'http://127.0.0.1:8050/'

dsor_logo = 'assets/logos/DSOR_logo_v05a.jpg'
isr_logo = 'assets/logos/isr_logo_red_background.png'

last_dropdown_changed = 0


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
        label_6 = '6. '
        label_7 = '7. '
        options = []
        if (re.search("mission specific graphics", input_value) == None):
            path = fn.extend_dir(input_value)
            fn.change_directory(str(path))
            last_directories[5] = path
            reset_upper_directories(6)

            label_6 = ""
            if (fn.is_part_of_path(fn.get_pwd(), 'overall')):
                # If previously chose overall on the Overview (3rd dropdown)
                if (input_value == "USBL"):
                    label_6 = '6. USBL Type'
                    label_7 = '7. Plots'
                else:
                    label_6 = '6. Plots'
                options.extend(fn.get_html_files() + fn.get_directories())
            else:
                # If previously chose missions on the Overview (3rd dropdown)
                label_6 = '6. Drivers'
                label_7 = '7. Plots'
                options = [option for option in USBL_EXTENSIONS]
                options.extend(fn.get_directories())
                options.remove("USBL")
        else:
            #print("AAAAAAAAAAAAAAAAAA")
            reset_upper_directories(5)
            options.extend(fn.get_html_files())
            #print("fn.get_html_files() = ", fn.get_html_files())
            label_6 = '6. Plots'

        
        #fn.change_directory(last_directories[4])
        #path = fn.extend_dir(input_value)
        #fn.change_directory(str(path))
        #last_directories[5] = path

        #print("     (callback) treat_fifth_level_dropdown: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options], (), "", "", label_6, '7. '
    
    #print("")
    return (), (), "", "", '6. ', '7. '


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

            return last_dir_options, [{'label': i, 'value': i} for i in options], "", "", '6. Drivers', '7. Plots'
        elif (input_value in fn.get_html_files()):
            # Prepare plot if it was an html file
                #print("\t\tupdate_sixth_level_dir: Adding html file to the plot")
                last_dir_options = fn.get_html_files()
                #print("last_dir_options = ", last_dir_options)
                path = fn.extend_dir(str(input_value))
                reset_upper_directories(6) # TODO maybe este não é preciso ???

                return last_dir_options, (), path, path_cat(path), '6. Plots', '7. '
    
    #print("")
    return (), (), "", "", '6. ', '7. '


def treat_seventh_lvl_dropdown(input_value_dir):
    # Roll back directory
    fn.change_directory(last_directories[6])

    #print("")
    #print("(aux function) treat__seventh_level_dir: Input = " + str(input_value_dir) + " ; path = ", fn.get_pwd())
    #print("     (aux) treat_seventh_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (aux) treat_seventh_level_dir: input_value in fn.get_directories()", str(input_value_dir in fn.get_directories()))
    #print("")

    if (type(input_value_dir) == str) and not (fn.is_part_of_path(fn.get_pwd(), input_value_dir)):

        seventh_dropdown_options = fn.get_directories() + fn.get_html_files()
        if (input_value_dir in fn.get_directories()):
            # Extend path if it was a directory
            path = fn.extend_dir(input_value_dir) # TODO este branch provavelmente já não é usado
            fn.change_directory(path)

            options = []
            options.extend(fn.get_html_files())

            return seventh_dropdown_options, [{'label': i, 'value': i} for i in options], '', '', '6. Drivers', '7. ' # TODO o primeiro () devia ter lá merdas do dropdown anterior

        elif (input_value_dir in fn.get_html_files()):
            # Prepare plot if it was an html file
                fn.change_directory(last_directories[5])
                sixth_dir_options = fn.get_directories() + USBL_EXTENSIONS
                fn.change_directory(last_directories[6])
                seventh_dir_options = fn.get_html_files()
                path = fn.extend_dir(str(input_value_dir))

                return sixth_dir_options, seventh_dir_options, path, path_cat(path), '6. Drivers', '7. Plots'

    return (), (), '', '', '6. '


def eighth_level_dir_dropdown(input_value_dir):

    #print("     eight_level_dir_dropdown: input_value_dir = ", input_value_dir)
    if (last_directories[6] != home):
        pwd = fn.get_pwd() # Save current directory
        fn.change_directory(last_directories[6]) # Roll back to seventh dropdown
        seventh_dropdown_options = fn.get_directories() + fn.get_html_files() # Get options for seventh dropdown
        fn.change_directory(pwd) # Roll back to current directory

    if (input_value_dir in fn.get_html_files()):
        # Prepare plot if it was an html file
            path = fn.extend_dir(str(input_value_dir))

            options = []
            options.extend(fn.get_directories())
            options.extend(fn.get_html_files())

            return seventh_dropdown_options, [{'label': i, 'value': i} for i in options], path, path_cat(path) # TODO o primeiro () devia ter lá merdas do dropdown anterior

    return (), (), '', ''


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

        sixth_dir_options = ()
        seventh_dir_options = ()
        if (last_directories[5] != home):
            # The fifth directory has already been reached
            fn.change_directory(last_directories[5])
            #print("     (callback) merge_button_click: fn.get_directories()", fn.get_html_files())
            sixth_dir_options = fn.get_html_files() + fn.get_directories()
            #print("     (callback) merge_button_click: sixth_dir_options = ", sixth_dir_options)
        elif (last_directories[4] != home):
            fn.change_directory(last_directories[4])
            #print("     (callback) merge_button_click: last_directories[4] = ", last_directories[4])
            #print("     (callback) merge_button_click: fn.get_directories()", fn.get_directories())
            #print("     (callback) merge_button_click: fn.get_html_files()", fn.get_html_files())
            sixth_dir_options = fn.get_html_files() + fn.get_directories()
            sixth_dir_options.remove("drivers")
            #print("     (callback) merge_button_click: sixth_dir_options = ", sixth_dir_options)
        if (last_directories[6] != home):
            # The sixth directory has already been reached
            fn.change_directory(last_directories[6])
            #print("     (callback) merge_button_click: fn.get_directories()", fn.get_html_files())
            seventh_dir_options = fn.get_html_files()
            #print("     (callback) merge_button_click: seventh_dir_options = ", seventh_dir_options)
            
        #print("     (callback) merge_button_click: pwd = ", fn.get_pwd())
        return sixth_dir_options, seventh_dir_options, path, path_cat(path), '6. Plots', '7. '
    
    #print("     (callback) merge_button_click: No html files found on present working directory. Not merging files.")
    
    return [{'label': i, 'value': i} for i in files], (), '', '', '6, ', '7. '


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
        
        #html.Button('Plot Directory',
        #id='plot button',
        #n_clicks=0,
        #style={'display':'inline'},
        #style={'margin-left': '40px'}
        #),

        dbc.Button('Plot Directory',
        id='plot button',
        n_clicks=0,
        style={'display':'inline'},
        #style={'margin-left': '40px'}
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

        html.Br(),
        html.Label(children='4. ',
        id='Fourth level dir label'),
        #html.Label('4. Fourth level Directory'),
        dcc.Dropdown((),
        id='Fourth level dir'),

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
        ####   Right   Dropdowns   ###
        ##############################

        html.P(id='center dropdowns', # This is here so the dropdowns won't show up at the top of the page
        style={'height': '28%'}),


        html.Br(),
        html.Label(children='5. ',
        id='Fifth level dir label'),
        dcc.Dropdown((),
        id='Fifth level dir',
        ),

        html.Br(),
        html.Label(children='6. ',
        id='Sixth level dir label'),
        dcc.Dropdown((),
        id='Sixth level dir',
        ),

        html.Br(),
        html.Label(children='7. ',
        id='Seventh level dir label'),
        dcc.Dropdown((),
        id='Seventh level dir',
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
        path = fn.extend_dir(input_value)
        path = fn.build_dir(PLOTS, path)
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
        if (input_value == "overall"):
            label = "4. Specificity"
        elif (input_value == "missions"):
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
            options.extend(fn.get_html_files())
            label = '5. Drivers'

        #print("     (callback) update_fifth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options], label
    
    #print("")
    return (), '5. '

#@app.callback(
#    Output('Sixth level dir', 'options'),
#    Output('Sixth level dir label', 'children'),
#    Input('Fifth level dir', 'value'),
#)
#def update_sixth_level_dir(input_value):

    # Roll back to parent directory
#    fn.change_directory(last_directories[4])

    #print("(callback) update_sixth_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_sixth_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_sixth_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
#    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories()) or input_value == 'mission specific graphics'):
#        # If the path actually changed
#        fn.change_directory(last_directories[4])
#        label = '6. '
#        options = []
#        if (re.search("mission specific graphics", input_value) == None):
#            path = fn.extend_dir(input_value)
#            fn.change_directory(str(path))
#            last_directories[5] = path
#            label = '6. Drivers'
#            options.extend(fn.get_directories())
#        else:
#            options.extend(fn.get_html_files())
#            label = '6. Plots'


        #print("     (callback) update_sixth_level_dir: options = ", options)
        #print("")

#        return [{'label': i, 'value': i} for i in options], label
    
    #print("")
#    return (), '6. '


@app.callback(
    Output('Sixth level dir', 'options'),
    Output('Seventh level dir', 'options'),
    Output('plot', 'children'),
    Output('plot', 'href'),
    Output('Sixth level dir label', 'children'),
    Output('Seventh level dir label', 'children'),
    Input('Sixth level dir', 'value'),
    Input('Seventh level dir', 'value'),
    Input('plot button', 'n_clicks'),
    Input('Fifth level dir', 'value'),
)
def update_seventh_level_dir(sixth_dir, seventh_dir, n_clicks_plot, fifth_dir):
    callback_trigger = ctx.triggered_id

    #print("(callback) update_seventh_level_dir: \n\tInput = {" + str(sixth_level_dir) + ", " + str(seventh_dir) + ", " + str(eighth_dir) + ", " + str(n_clicks_plot) + "}")
    #print("\tpath = ", fn.get_pwd())

    if (seventh_dir == None and fifth_dir == None and n_clicks_plot == 0 and sixth_dir == None):
        return (), (), '', '', '6. ', '7. '

    if callback_trigger == 'Sixth level dir':
        # Triggered by directory change
        #print("     (callback) update_seventh_level_dir: Callback triggered by directory change (Seventh level dir)")
        return treat_sixth_lvl_dropdown(sixth_dir)

    elif callback_trigger == 'plot button':
        # Triggered by merge button
        #print("     (callback) update_seventh_level_dir: Callback triggered by merge button")
        return merge_button_click()

    elif callback_trigger == 'Seventh level dir':
        # Triggered by directory change
        #print("     (callback) update_seventh_level_dir: Callback triggered by directory change (Eighth level dir)")
        return treat_seventh_lvl_dropdown(seventh_dir)

    elif callback_trigger == 'Fifth level dir':
        #print("     (callback) update_seventh_level_dir: Callback triggered by directory change (Sixth level dir)")
        return treat_fifth_level_dropdown(fifth_dir)

    return (), (), '', '', '6. ', '7. '


app.callback(
    Output("modal-help-body-scroll", "is_open"),
    [
        Input("open-help-body-scroll", "n_clicks"),
        Input("close-help-body-scroll", "n_clicks"),
    ],
    [State("modal-help-body-scroll", "is_open")],
)(toggle_modal)


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