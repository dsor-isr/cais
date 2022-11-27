# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import file_navigation as fn
import base64

home = fn.get_pwd()
last_directories = [home, home]

image_path = 'images/cats/cat-png-17.png'

# Using base64 encoding and decoding
def b64_image(image_filename):

    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')



app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div(children=[
        html.Label('Main Directory'),
        dcc.Dropdown(fn.get_directory_content(),
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
        html.H1('Pets'),
        html.Img(src=b64_image(image_path),
        id='plot'),

    ], style={'padding': 10, 'flex': 1}),

], style={'display': 'flex', 'flex-direction': 'row'})


@app.callback(
    Output('Second level dir', 'options'),
    #Output('Third level dir', 'options'),
    Input('Home directory', 'value'),
)
def update_second_level_dir(input_value):
    # TODO check if selected input is a directory. The alternative is to only show directories (on this level)

    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(),input_value)):
        # If the path actually changed
        fn.change_directory(last_directories[0])
        path = fn.extend_dir(input_value)
        fn.change_directory(str(path))
        last_directories[1] = path

        return [{'label': i, 'value': i} for i in fn.get_directory_content()]
    
    return ()


@app.callback(
    Output('Third level dir', 'options'),
    Input('Second level dir', 'value'),
)
def update_third_level_dir(input_value):
    # TODO check if selected input is a directory. The alternative is to only show directories (on this level)

    if (type(input_value) == str) and not (fn.is_part_of_path(fn.get_pwd(), input_value)):
        fn.change_directory(last_directories[1])
        path = fn.extend_dir(input_value)
        #last_dir = fn.get_pwd()
        fn.change_directory(path)

        # TODO changing main directory isn't changing it's grandchildren directories (maybe use fn.is_part_of_path() and update all sub dirs)

        return [{'label': i, 'value': i} for i in fn.get_directory_content()]
    
    return ()


@app.callback(
    Output('plot', 'src'),
    Input('Third level dir', 'value'),
)
def update_plot(input_value):

    if input_value == None:
        return

    path = fn.extend_dir(str(input_value))

    return b64_image(path)



if __name__ == '__main__':
    app.run_server(debug=True)