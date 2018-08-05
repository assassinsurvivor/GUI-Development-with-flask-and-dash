import base64
import io
import os
import time
import json

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from PIL import Image
from io import BytesIO
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import scipy.spatial.distance as spatial_distance
from tosee import trapcolors as colo


reader_t=pd.read_csv("helper_data/Diagnosis_important.csv")
atr=reader_t["code"].tolist()

IMAGE_DATASETS = []
WORD_EMBEDDINGS = ('diagnosis_3000','diagnosis_400')

df_desc=pd.read_csv("helper_data/for_description.csv")
df_tohave=df_desc["desc"].tolist()

df_desc_2=pd.read_csv("helper_data/for_description_2.csv")
df_tohave_2=df_desc_2["desc"].tolist()

arr=['V72.31', '795', 'V22.1', '715.36', '285.9', 'V72.42', 'V25.09','V72.41', '300.3', 'V65.3', '518.89', '839.21', '627.3', 'V10.83','515', '723.1', '478.19', '716.98', '564.1', '311']

def merge(a, b):
    return dict(a, **b)


def omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


def numpy_to_b64(array, scalar=True):
    # Convert from 0-1 to 0-255
    if scalar:
        array = np.uint8(255 * array)

    im_pil = Image.fromarray(array)
    buff = BytesIO()
    im_pil.save(buff, format="png")
    im_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    return im_b64


def Card(children, **kwargs):
    return html.Section(
        children,
        style=merge({
            'padding': 20,
            'margin': 5,
            'borderRadius': 5,
            'border': 'thin lightgrey solid',

            # Remove possibility to select the text for better UX
            'user-select': 'none',
            '-moz-user-select': 'none',
            '-webkit-user-select': 'none',
            '-ms-user-select': 'none'
        }, kwargs.get('style', {})),
        **omit(['style'], kwargs)
    )


def NamedSlider(name, short, min, max, step, val, marks=None):
    if marks:
        step = None
    else:
        marks = {i: i for i in range(min, max + 1, step)}

    return html.Div(
        style={'margin': '25px 5px 30px 0px'},
        children=[
            f"{name}:",
            html.Div(style={'margin-left': '5px'}, children=[
                dcc.Slider(id=f'slider-{short}',
                           min=min,
                           max=max,
                           marks=marks,
                           step=step,
                           value=val)
            ])
        ])


def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f'div-{short}',
        style=merge({
            'display': 'inline-block'
        }, kwargs.get('style', {})),
        children=[
            f'{name}:',
            dcc.RadioItems(
                id=f'radio-{short}',
                options=options,
                value=val,
                labelStyle={
                    'display': 'inline-block',
                    'margin-right': '7px',
                    'font-weight': 300
                },
                style={
                    'display': 'inline-block',
                    'margin-left': '7px'
                }
            )
        ],
        **omit(['style'], kwargs)
    )


demo_layout = html.Div(
    className="container",
    style={
        'width': '90%',
        'max-width': 'none',
        'font-size': '1.5rem',
        'padding': '10px 30px'
    },
    children=[
        # Header
        html.Div(className="row", children=[
            html.H2(
                't-SNE EDA',
                id='title',
                style={
                    'float': 'left',
                    'margin-top': '20px',
                    'margin-bottom': '0',
                    'margin-left': '7px'
                }
            ),

            html.Img(
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQW0j8jQYgAglxmwxx2mc-XKCuaFZhOo5eVyaNVogSQBctiQW8j",
                style={
                    'height': '100px',
                    'float': 'right'
                }
            )
        ]),

        # Body
        html.Div(className="row", children=[
            html.Div(className="eight columns", children=[
                dcc.Graph(
                    id='graph-3d-plot-tsne',
                    style={'height': '98vh'}
                )
            ]),

            html.Div(className="four columns", children=[
                Card([
                    dcc.Dropdown(
                        id='dropdown-dataset',
                        searchable=False,
                        options=[
                            # TODO: Generate more data
                            {'label': 'diagnosis_3000', 'value': 'diagnosis_3000'},
                            {'label': 'diagnosis_400', 'value': 'diagnosis_400'}
                           
                        ],
                        placeholder="Select a dataset"
                    ),

                    NamedSlider(
                        name="Number of Iterations",
                        short="iterations",
                        min=250,
                        max=1000,
                        step=None,
                        val=500,
                        marks={i: i for i in [250, 500, 750, 1000]}
                    ),

                    NamedSlider(
                        name="Perplexity",
                        short="perplexity",
                        min=3,
                        max=100,
                        step=None,
                        val=30,
                        marks={i: i for i in [3, 10, 30, 50, 100]}
                    ),

                    NamedSlider(
                        name="Initial PCA Dimensions",
                        short="pca-dimension",
                        min=25,
                        max=100,
                        step=None,
                        val=50,
                        marks={i: i for i in [25, 50, 100]}
                    ),

                    NamedSlider(
                        name="Learning Rate",
                        short="learning-rate",
                        min=10,
                        max=200,
                        step=None,
                        val=100,
                        marks={i: i for i in [10, 50, 100, 200]}
                    ),

                    html.Div(id='div-wordemb-controls', style={'display': 'none'}, children=[
                        NamedInlineRadioItems(
                            name="Display Mode",
                            short="wordemb-display-mode",
                            options=[
                                {'label': ' Regular', 'value': 'regular'},
                                {'label': ' Top-10 Neighbors', 'value': 'neighbors'},
                                {'label': ' Top-50 Neighbors', 'value': 'neighborss'}
                                
                            ],
                            val='regular'),

                        dcc.Dropdown(id='dropdown-word-selected', placeholder='Select word to display its neighbors')
                    ])
                ]),

                Card(style={'padding': '5px'}, children=[
                    html.Div(id='div-plot-click-message',
                             style={'text-align': 'center',
                                    'margin-bottom': '7px',
                                    'font-weight': 'bold'}
                             ),

                    html.Div(id='div-plot-click-image'),

                    html.Div(id='div-plot-click-wordemb')
                ])
            ])
        ]),

        
        
    ]
)


def demo_callbacks(app):
    def generate_figure_image(groups, layout):
        data = []

        for idx, val in groups:
            scatter = go.Scatter3d(
                name=idx,
                x=val['x'],
                y=val['y'],
                z=val['z'],
                text=[idx for _ in range(val['x'].shape[0])],
                textposition='top',
                mode='markers',
                marker=dict(
                    size=3,
                    symbol='circle'
                )
            )
            data.append(scatter)

        figure = go.Figure(
            data=data,
            layout=layout
        )

        return figure

    def generate_figure_word_vec(embedding_df, layout, wordemb_display_mode, selected_word, dataset):
        # Regular displays the full scatter plot with only circles
        if wordemb_display_mode == 'regular':
            plot_mode = 'markers'

        # Nearest Neighbors displays only the 200 nearest neighbors of the selected_word, in text rather than circles
        elif wordemb_display_mode == 'neighbors':
            if not selected_word:
                return go.Figure()
            plot_mode = 'markers'

            # Get the nearest neighbors indices using Euclidean distance
            vector = data_dict[dataset].set_index('0')
            selected_vec = vector.loc[selected_word]
            def compare_pd(vector):
                return spatial_distance.euclidean(vector, selected_vec)
            distance_map = vector.apply(compare_pd, axis=1)
            neighbors_idx = distance_map.sort_values()[:10].index

            # Select those neighbors from the embedding_df
            embedding_df = embedding_df.loc[neighbors_idx]
        elif wordemb_display_mode == 'neighborss':
            if not selected_word:
                return go.Figure()
            plot_mode = 'markers'

            # Get the nearest neighbors indices using Euclidean distance
            vector = data_dict[dataset].set_index('0')
            selected_vec = vector.loc[selected_word]
            def compare_pd(vector):
                return spatial_distance.euclidean(vector, selected_vec)
            distance_map = vector.apply(compare_pd, axis=1)
            neighbors_idx = distance_map.sort_values()[:50].index

            # Select those neighbors from the embedding_df
            embedding_df = embedding_df.loc[neighbors_idx]

            


        if dataset == 'diagnosis_3000':
            texter=df_tohave
            co=colo
        else:
            texter=df_tohave_2
            co='#17becf' 
        names=list(embedding_df.index)
          

        

        

        scatter = go.Scatter3d(
            name=embedding_df.index,
            x=embedding_df['x'],
            y=embedding_df['y'],
            z=embedding_df['z'],
            text=texter,
            textposition='middle-center',
            showlegend=False,
            mode=plot_mode,
            marker=dict(
            size=3,
            color=co,
            symbol='circle'
                )
            
        )

        figure = go.Figure(
            data=[scatter],
            layout=layout
        )

        return figure

    @app.server.before_first_request
    def load_image_data():
        global data_dict

        data_dict = {
            'diagnosis_3000': pd.read_csv("data/diagnosis_3000.csv"),
            'diagnosis_400':pd.read_csv("data/diagnosis_400.csv")
            
        }

    @app.callback(Output('div-wordemb-controls', 'style'),
                  [Input('dropdown-dataset', 'value')])
    def show_wordemb_controls(dataset):
        if dataset in WORD_EMBEDDINGS:
            return None
        else:
            return {'display': 'none'}

    @app.callback(Output('dropdown-word-selected', 'disabled'),
                  [Input('radio-wordemb-display-mode', 'value')])
    def disable_word_selection(mode):
        if mode == 'neighbors' or mode=="neighborss":
            return False
        else:
            return True

    @app.callback(Output('dropdown-word-selected', 'options'),
                  [Input('dropdown-dataset', 'value')])
    def fill_dropdown_word_selection_options(dataset):
        if dataset in WORD_EMBEDDINGS:
            return [{'label': i, 'value': i} for i in atr]
        else:
            return []

    @app.callback(Output('graph-3d-plot-tsne', 'figure'),
                  [Input('dropdown-dataset', 'value'),
                   Input('slider-iterations', 'value'),
                   Input('slider-perplexity', 'value'),
                   Input('slider-pca-dimension', 'value'),
                   Input('slider-learning-rate', 'value'),
                   Input('dropdown-word-selected', 'value'),
                   Input('radio-wordemb-display-mode', 'value')])
    def display_3d_scatter_plot(dataset, iterations, perplexity, pca_dim, learning_rate, selected_word, wordemb_display_mode):
        if dataset:
            path = f'demo_embeddings/{dataset}/iterations_{iterations}/perplexity_{perplexity}/pca_{pca_dim}/learning_rate_{learning_rate}'

            try:
                embedding_df = pd.read_csv(path + f'/data.csv', index_col=0, encoding="ISO-8859-1")

            except FileNotFoundError as error:
                print(error, "\nThe dataset was not found. Please generate it using generate_demo_embeddings.py")
                return go.Figure()

            # Plot layout
            axes = dict(
                title='',
                showgrid=True,
                zeroline=False,
                showticklabels=False
            )

            layout = go.Layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(
                    xaxis=axes,
                    yaxis=axes,
                    zaxis=axes
                )
            )

            # For Image datasets
            if dataset in IMAGE_DATASETS:
                embedding_df['label'] = embedding_df.index

                groups = embedding_df.groupby('label')
                figure = generate_figure_image(groups, layout)

            # Everything else is word embeddings
            elif dataset in WORD_EMBEDDINGS:
                figure = generate_figure_word_vec(
                    embedding_df=embedding_df,
                    layout=layout,
                    wordemb_display_mode=wordemb_display_mode,
                    selected_word=selected_word,
                    dataset=dataset
                )

            else:
                figure = go.Figure()

            return figure

    @app.callback(Output('div-plot-click-image', 'children'),
                  [Input('graph-3d-plot-tsne', 'clickData'),
                   Input('dropdown-dataset', 'value'),
                   Input('slider-iterations', 'value'),
                   Input('slider-perplexity', 'value'),
                   Input('slider-pca-dimension', 'value'),
                   Input('slider-learning-rate', 'value')])
    def display_click_image(clickData,
                            dataset,
                            iterations,
                            perplexity,
                            pca_dim,
                            learning_rate):
        if dataset in IMAGE_DATASETS and clickData:
            # Load the same dataset as the one displayed
            path = f'demo_embeddings/{dataset}/iterations_{iterations}/perplexity_{perplexity}/pca_{pca_dim}/learning_rate_{learning_rate}'

            try:
                embedding_df = pd.read_csv(path + f'/data.csv', encoding="ISO-8859-1")

            except FileNotFoundError as error:
                print(error, "\nThe dataset was not found. Please generate it using generate_demo_embeddings.py")
                return

            # Convert the point clicked into float64 numpy array
            click_point_np = np.array([clickData['points'][0][i] for i in ['x', 'y', 'z']]).astype(np.float64)
            # Create a boolean mask of the point clicked, truth value exists at only one row
            bool_mask_click = embedding_df.loc[:, 'x':'z'].eq(click_point_np).all(axis=1)
            # Retrieve the index of the point clicked, given it is present in the set
            if bool_mask_click.any():
                clicked_idx = embedding_df[bool_mask_click].index[0]

                # Retrieve the image corresponding to the index
                image_vector = data_dict[dataset].iloc[clicked_idx]
                if dataset == 'cifar_gray_3000':
                    image_np = image_vector.values.reshape(32, 32).astype(np.float64)
                else:
                    image_np = image_vector.values.reshape(28, 28).astype(np.float64)

                # Encode image into base 64
                image_b64 = numpy_to_b64(image_np)

                return html.Img(
                    src='data:image/png;base64, ' + image_b64,
                    style={
                        'height': '25vh',
                        'display': 'block',
                        'margin': 'auto'
                    }
                )
        return None

    @app.callback(Output('div-plot-click-wordemb', 'children'),
                  [Input('graph-3d-plot-tsne', 'clickData'),
                   Input('dropdown-dataset', 'value')])
    def display_click_word_neighbors(clickData, dataset):
        if dataset in WORD_EMBEDDINGS and clickData:
            selected_word = clickData['points'][0]['text']

            # Get the nearest neighbors indices using Euclidean distance
            vector = data_dict[dataset].set_index('0')
            selected_vec = vector.loc[selected_word]
            def compare_pd(vector):
                return spatial_distance.euclidean(vector, selected_vec)
            distance_map = vector.apply(compare_pd, axis=1)
            nearest_neighbors = distance_map.sort_values()[1:6]

            trace = go.Bar(
                x=nearest_neighbors.values,
                y=nearest_neighbors.index,
                width=0.5,
                orientation='h'
            )

            layout = go.Layout(
                title=f'5 nearest neighbors of "{selected_word}"',
                xaxis=dict(title='Euclidean Distance'),
                margin=go.Margin(l=60, r=60, t=35, b=35)
            )

            fig = go.Figure(data=[trace], layout=layout)

            return dcc.Graph(
                id='graph-bar-nearest-neighbors-word',
                figure=fig,
                style={'height': '25vh'},
                config={'displayModeBar': False}
            )

        else:
            return None

    @app.callback(Output('div-plot-click-message', 'children'),
                  [Input('graph-3d-plot-tsne', 'clickData'),
                   Input('dropdown-dataset', 'value')])
    def display_click_message(clickData, dataset):
        """
        Displays message shown when a point in the graph is clicked, depending whether it's an image or word
        :param clickData:
        :param dataset:
        :return:
        """
        if dataset in IMAGE_DATASETS:
            if clickData:
                return "Image Selected"
            else:
                return "Click a data point on the scatter plot to display its corresponding image."

        elif dataset in WORD_EMBEDDINGS:
            if clickData:
                return None
            else:
                return "Click a word on the plot to see its top 5 neighbors."


