import dash
import dash_core_components as dcc
import dash_html_components as html
import time
import plotly.graph_objs as go
import random
import glob
import os
import flask
from flask import Flask
app = dash.Dash()



image_directory = r'C:\Users\PT18999\Desktop\imager/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'



app.layout = html.Div([
    html.Div([
        html.H2('Model Performance',
                style={'float': 'left',
                       }),
        ]),


    dcc.Dropdown(id='dropper',
                 options=[{'label': i.split(".")[0], 'value': i} for i in list_of_images],
                 value=["DNN Architecture"],
                 ),
    html.Img(id='image'),
##    dcc.Dropdown(id='vehicle-data-name',
##                 options=[{'label': s, 'value': s}
##                          for s in data_dict.keys()],
##                 value=['CNN Architecture','DNN Architecture','LSTM Architecture'],
##                 multi=True
##                 ),
##    html.Div(children=html.Div(id='graphs'), className='row'),
    
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})




@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('dropper', 'value')])
def update_image_src(value):
    return static_image_route + value



@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)





external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
