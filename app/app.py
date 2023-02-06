# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import file_navigation as fn
import base64
import webbrowser
from bs4 import BeautifulSoup
import copy


##############################
###    Suggested Debug     ###
###      
##############################


##############################
###        Constants       ###
##############################

ALL_HTML = '/all.html'
ALL_HTML2 = 'all.html'

##############################
###    Global Variables    ###
##############################

#home = fn.get_pwd()
home = fn.extend_dir('assets')
#print("home = ", home)
#print("content = ", fn.get_directories(path=home))
last_directories = [home, home, home]
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
    merged_html = fn.get_pwd() + ALL_HTMl
    with open(merged_html, "w", encoding='utf-8') as file:
        file.write(str(output_file))


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
        ####        Dropdowns      ###
        ##############################
        
        html.Br(),
        html.Label('Main Directory'),
        dcc.Dropdown([{'label': i, 'value': i} for i in fn.get_directories(path=home) if (i not in {'logos'})],
        id='Home directory'),

        html.Br(),
        html.Label('Second level Directory'),
        dcc.Dropdown((),
        id='Second level dir'),

        html.Br(),
        html.Label('Third level Directory'),
        dcc.Dropdown((),
        id='Third level dir'),

        html.Br(),
        html.Button('Plot Directory',
        id='plot button',
        n_clicks=0,
        #style={'margin-left': '40px'}
        ),

        html.Br(),
        html.Label('Fourth level Directory'),
        dcc.Dropdown((),
        id='Fourth level dir'),

        html.Br(),
        dcc.Link('',
        href='',
        target='_blank',
        refresh=True,
        id='plot',),

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
    print("(callback) update_second_level_dir: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    print("     (callback) update_second_level_dir: fn.get_directories()", fn.get_directories())
    print("     (callback) update_second_level_dir: input_value in fn.get_directories()", str(input_value in fn.get_directories()))
    print("")
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
        
        return [{'label': i, 'value': i} for i in options if i not in ('logos')]
    
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
    #print("")
    if (type(input_value) == str) and (not (fn.is_part_of_path(fn.get_pwd(),input_value)) and (input_value in fn.get_directories())):
        # If the path actually changed
        fn.change_directory(last_directories[1])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[2] = path

        options = []
        options.extend(fn.get_directories())
        options.extend(fn.get_html_files())

        return [{'label': i, 'value': i} for i in options]
    
    return ()

@app.callback(
    Output('Fourth level dir', 'options'),
    ###Output('plot', 'children'), # Remover se der merda
    ###Output('plot', 'href'), # Remover se der merda
    Input('Third level dir', 'value'),
    Input('plot button', 'n_clicks'),
)
def update_fourth_level_dir(input_value_dir, n_clicks_plot):
    callback_trigger = ctx.triggered_id

    print("(callback) update_fourth_level_dir: Input = {" + str(input_value_dir) + ", " + str(n_clicks_plot) + "} ; path = ", fn.get_pwd())

    if callback_trigger == 'Third level dir':
        # Triggered by directory change

        # Roll back directory
        fn.change_directory(last_directories[2])

        if (type(input_value_dir) == str) and not (fn.is_part_of_path(fn.get_pwd(), input_value_dir)):
            if (input_value_dir in fn.get_directories()):
                # Extend path if it was a directory

                #fn.change_directory(last_directories[2])
                path = fn.extend_dir(input_value_dir)
                fn.change_directory(path)

                options = []
                options.extend(fn.get_directories())
                options.extend(fn.get_html_files())

                return [{'label': i, 'value': i} for i in options]
            ###elif (input_value_dir in fn.get_html_files()):
                #### Prepare plot if it was an html file
                ###path = fn.extend_dir(str(input_value_dir))

                ###return (), path, path_cat(path)

    elif callback_trigger == 'plot button':
        # Triggered by merge button

        files = fn.get_html_files()
        if (len(files) != 0) and input_value_dir != None:
            # html files found on present working directory
            
            merge_html_files(files)
            
            webbrowser.open_new(host + 'assets/all.html')

            return [{'label': i, 'value': i} for i in fn.get_html_files()]

    return ()


@app.callback(
    Output('plot', 'children'),
    Output('plot', 'href'),
    Input('Fourth level dir', 'value'),
)
def update_plot(input_value):

    #print("(callback) update_plot: Input = " + str(input_value) + " ; path = ", fn.get_pwd())
    
    if input_value == None or not (input_value in fn.get_html_files()):
        return '',  ''

    path = fn.extend_dir(str(input_value))
    
    return path, path_cat(path)


##############################
###      Main Function     ###
##############################

if __name__ == '__main__':
    app.run_server(debug=True)