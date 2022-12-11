# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import file_navigation as fn
import base64

home = fn.get_pwd()
last_directories = [home, home, home]

#image_path = 'images/cats/cat-png-17.png'

# Using base64 encoding and decoding
def b64_image(image_filename):

    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def path_cat(path):
    return path[path.find('assets'):]

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div(children=[
        html.Label('Main Directory'),
        dcc.Dropdown(fn.get_directories(),
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
        dcc.Link('CLICK HERE TO PLOT',
        href='',
        target='_blank',
        refresh=True,
        id='plot'),

        #html.Br(),
        #html.H1('Pets'),
        #html.Img(src=b64_image(image_path),
        #id='plot'),

    ], style={'padding': 10, 'flex': 1}),

], style={'display': 'flex', 'flex-direction': 'row'})


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

        return [{'label': i, 'value': i} for i in fn.get_directories()]
    
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


        return [{'label': i, 'value': i} for i in fn.get_html_files()]
    
    return ()


@app.callback(
    Output('plot', 'href'),
    Input('Fourth level dir', 'value'),
)
def update_plot(input_value):

    if input_value == None:
        return ''

    path = fn.extend_dir(str(input_value))
    
    return path_cat(path)



if __name__ == '__main__':
    app.run_server(debug=True)