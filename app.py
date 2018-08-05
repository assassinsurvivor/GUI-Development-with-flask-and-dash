# -*- coding: utf-8 -*-
import os
import dash
from server import server

from demo import demo_layout, demo_callbacks
from local import local_layout, local_callbacks

app = dash.Dash(name='app6', sharing=True, server=server, url_base_pathname='/tsne')
server = app.server

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

    demo_mode = True
else:
    demo_mode = False

demo_mode=True

# App
if demo_mode:
    app.layout = demo_layout
else:
    app.layout = local_layout


# Callbacks
if demo_mode:
    demo_callbacks(app)
else:
    local_callbacks(app)


# Load external CSS
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-tsne/master/custom_styles.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
