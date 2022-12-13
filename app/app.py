# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import file_navigation as fn
import base64
import webbrowser

##############################
###    Global Variables    ###
##############################


home = fn.get_pwd()
last_directories = [home, home, home]
plot_dir = home
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
        dcc.Dropdown([{'label': i, 'value': i} for i in fn.get_directories() if i not in ('images', '__pycache__')],
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
        html.Label('Fourth level Directory'),
        dcc.Dropdown((),
        id='Fourth level dir'),

        html.Br(),
        dcc.Link('CLICK HERE FOR PLOT',
        href='',
        target='_blank',
        refresh=True,
        id='plot'),

        html.Button('open directory',
        id='plot button',
        n_clicks=0,
        style={'margin-left': '40px'}),
        html.Div(id='hidden-div', style={'display':'none'}),        

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

    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(),input_value)):
        # If the path actually changed
        fn.change_directory(last_directories[0])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[1] = path

        return [{'label': i, 'value': i} for i in fn.get_directories() if i not in ('logos')]
    
    return ()

@app.callback(
    Output('Third level dir', 'options'),
    Input('Second level dir', 'value'),
)
def update_third_level_dir(input_value):

    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(),input_value)):
        # If the path actually changed
        fn.change_directory(last_directories[1])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[2] = path

        return [{'label': i, 'value': i} for i in fn.get_directories()]
    
    return ()

@app.callback(
    Output('Fourth level dir', 'options'),
    Input('Third level dir', 'value'),
)
def update_fourth_level_dir(input_value):

    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(), input_value)):
        fn.change_directory(last_directories[2])
        path = fn.extend_dir(input_value)
        fn.change_directory(path)

        global plot_dir
        plot_dir = path

        return [{'label': i, 'value': i} for i in fn.get_html_files()]
    
    return ()

@app.callback(
    Output('hidden-div', 'children'),
    Input('plot button', 'n_clicks'),
)
def plot_directory(n_clicks):
    if plot_dir != home:
        fn.change_directory(plot_dir)
        for files in fn.get_html_files():
            path = fn.extend_dir(files)
            webbrowser.open_new_tab(host + path_cat(path))

    return html.Div('')


@app.callback(
    Output('plot', 'href'),
    Input('Fourth level dir', 'value'),
)
def update_plot(input_value):

    if input_value == None:
        return ''

    path = fn.extend_dir(str(input_value))
    
    return path_cat(path)


##############################
###      Main Function     ###
##############################

if __name__ == '__main__':
    app.run_server(debug=True)