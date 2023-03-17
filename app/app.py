# Run this app with 'python3 app.py' and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import file_navigation as fn
import base64
#import webbrowser
from bs4 import BeautifulSoup
import copy


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


def treat_seventh_lvl_dropdown(input_value_dir):
    # Roll back directory
    fn.change_directory(last_directories[6])

    #print("")
    #print("(aux function) treat__seventh_level_dir: Input = " + str(input_value_dir) + " ; path = ", fn.get_pwd())
    #print("     (aux) treat_seventh_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (aux) treat_seventh_level_dir: input_value in fn.get_directories()", str(input_value_dir in fn.get_directories()))
    #print("")

    if (type(input_value_dir) == str) and not (fn.is_part_of_path(fn.get_pwd(), input_value_dir)):
        if (input_value_dir in fn.get_directories()):
            # Extend path if it was a directory

            path = fn.extend_dir(input_value_dir)
            fn.change_directory(path)

            options = []
            options.extend(fn.get_directories())
            options.extend(fn.get_html_files())

            return [{'label': i, 'value': i} for i in options], '', ''

        elif (input_value_dir in fn.get_html_files()):
            # Prepare plot if it was an html file
                path = fn.extend_dir(str(input_value_dir))

                return (), path, path_cat(path)

    return (), '', ''


def eighth_level_dir_dropdown(input_value_dir):

    print("     eight_level_dir_dropdown: input_value_dir = ", input_value_dir)

    if (input_value_dir in fn.get_html_files()):
        # Prepare plot if it was an html file
            path = fn.extend_dir(str(input_value_dir))

            options = []
            options.extend(fn.get_directories())
            options.extend(fn.get_html_files())

            return [{'label': i, 'value': i} for i in options], path, path_cat(path)

    return (), '', ''


def merge_button_click():
    files = fn.get_html_files()
    if (len(files) != 0):
        # html files found on present working directory
            
        merge_html_files(files)

        path = fn.extend_dir(ALL_HTML2)

        return [{'label': i, 'value': i} for i in files], path, path_cat(path)
    
    return [{'label': i, 'value': i} for i in files], '', ''


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
        html.Label('2. Vehicles or log of the day'),
        dcc.Dropdown((),
        id='Second level dir'),

        html.Br(),
        html.Label('3. Vehicle'),
        dcc.Dropdown((),
        id='Third level dir'),

        html.Br(),
        html.Label('4. Fourth level Directory'),
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
        html.Label('5. Fifth level Directory'),
        dcc.Dropdown((),
        id='Fifth level dir',
        ),

        html.Br(),
        html.Label('6. Sixth level Directory'),
        dcc.Dropdown((),
        id='Sixth level dir',
        ),

        html.Br(),
        html.Label('7. Seventh level Directory'),
        dcc.Dropdown((),
        id='Seventh level dir',
        ),

        html.Br(),
        html.Label('8. Eighth level Directory'),
        dcc.Dropdown((),
        id='Eighth level dir',
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
        fn.change_directory(str(path))
        last_directories[1] = path

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
        fn.change_directory(str(path))
        last_directories[2] = path

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
        path = fn.build_dir(PLOTS, path)
        fn.change_directory(str(path))
        last_directories[3] = path

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_fourth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options]
    
    #print("")
    return ()

@app.callback(
    Output('Fifth level dir', 'options'),
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
        if (input_value == 'overall'):
            path = fn.build_dir(DRIVERS, path)
        fn.change_directory(str(path))
        last_directories[4] = path

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_fifth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options]
    
    #print("")
    return ()

@app.callback(
    Output('Sixth level dir', 'options'),
    Input('Fifth level dir', 'value'),
)
def update_sixth_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[4])

    #print("(callback) update_sixth_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_sixth_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_sixth_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[4])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[5] = path

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_sixth_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options]
    
    #print("")
    return ()

@app.callback(
    Output('Seventh level dir', 'options'),
    Input('Sixth level dir', 'value'),
)
def update_seventh_level_dir(input_value):

    # Roll back to parent directory
    fn.change_directory(last_directories[5])

    #print("(callback) update_seventh_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    #print("     (callback) update_seventh_level_dir: fn.get_directories()", fn.get_directories())
    #print("     (callback) update_seventh_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[5])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[6] = path

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        #print("     (callback) update_seventh_level_dir: options = ", options)
        #print("")

        return [{'label': i, 'value': i} for i in options]
    
    #print("")
    return ()


@app.callback(
    Output('Eighth level dir', 'options'),
    Output('plot', 'children'),
    Output('plot', 'href'),
    Input('Seventh level dir', 'value'),
    Input('Eighth level dir', 'value'),
    Input('plot button', 'n_clicks'),
)
def update_eighth_level_dir(seventh_dir, eighth_dir, n_clicks_plot):
    callback_trigger = ctx.triggered_id

    print("(callback) update_eighth_level_dir: Input = {" + str(seventh_dir) + ", " + str(eighth_dir) + ", " + str(n_clicks_plot) + "} ; path = ", fn.get_pwd())

    if (seventh_dir == None and eighth_dir == None and n_clicks_plot == 0):
        return (), '', ''

    if callback_trigger == 'Seventh level dir':
        # Triggered by directory change
        print("     (callback) update_eighth_level_dir: Callback triggered by directory change (Seventh level dir)")
        return treat_seventh_lvl_dropdown(seventh_dir)

    elif callback_trigger == 'plot button':
        # Triggered by merge button

        print("     (callback) update_eighth_level_dir: Callback triggered by merge button")
        return merge_button_click()

    elif callback_trigger == 'Eighth level dir':
        # Triggered by directory change

        print("     (callback) update_eighth_level_dir: Callback triggered by directory change (Eighth level dir)")
        return eighth_level_dir_dropdown(eighth_dir)

    return (), '', ''


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