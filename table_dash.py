import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
from server import server

app = dash.Dash(name='app3', sharing=True, server=server, url_base_pathname='/app3')

app.scripts.config.serve_locally = True


DF_WALMART = pd.read_csv(r'helper_data\patients_train.csv')



ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]


app.layout = html.Div([
    html.H4('CERVICAL CANCER SCREENING'),
    dt.DataTable(
        rows=DF_WALMART.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(DF_WALMART.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('PATIENT_AGE_GROUP', 'ETHNICITY', 'HOUSEHOLD_INCOME',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': pd.DataFrame(list(dff.groupby(['PATIENT_AGE_GROUP'].count()["IS_SCREENER"].index))),
        
        'y': pd.DataFrame([i/j for i,j in zip((dff.groupby(['PATIENT_AGE_GROUP'].sum()["IS_SCREENER"].tolist())),(dff.groupby(['PATIENT_AGE_GROUP'].count()["IS_SCREENER"].tolist())))]),
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['ETHNICITY'],
        'y': dff['IS_SCREENER'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['HOUSEHOLD_INCOME'],
        'y': dff['IS_SCREENER'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
