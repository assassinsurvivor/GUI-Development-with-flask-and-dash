import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from scipy import stats
from server import server
import plotly.graph_objs as go
import plotly.plotly as py


colors = {
    'background': 'white',
    'text': 'black'
}


fi=pd.read_csv("helper_data/feature_importances.csv")
df=pd.read_csv("helper_data/data3.csv")
fid=fi.iloc[0:10,:]





dff=pd.read_csv("helper_data/Patients_train.csv")
dff = dff[["PATIENT_AGE_GROUP","PATIENT_STATE", "ETHNICITY", "HOUSEHOLD_INCOME", "EDUCATION_LEVEL", "IS_SCREENER"]]
age_group_totals = dff.groupby(['PATIENT_AGE_GROUP']).size()
screener_rates = dff.groupby(['PATIENT_AGE_GROUP']).apply(lambda x: x.IS_SCREENER.sum()/x.shape[0])
conf_ints = [stats.binom.interval(.95, age_group_totals[x],screener_rates[x])/age_group_totals[x] for x in screener_rates.index]
xer=[x[1]-x[0] for x in conf_ints]

hispi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["ETHNICITY"].apply(lambda x:x=="HISPANIC")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
allo=dff[dff.groupby(["PATIENT_AGE_GROUP"])["ETHNICITY"].apply(lambda x:x=="ALL OTHER")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
african=dff[dff.groupby(["PATIENT_AGE_GROUP"])["ETHNICITY"].apply(lambda x:x=="AFRICAN AMERICAN")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
causi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["ETHNICITY"].apply(lambda x:x=="CAUCASIAN")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())

trace1 = go.Bar(
    x=hispi.index,
    y=hispi,
    name='HISPANIC'
)
trace2 = go.Bar(
    x=allo.index,
    y=allo,
    name='ALL OTHER'
)

trace3 = go.Bar(
    x=african.index,
    y=african,
    name='AFRICAN AMERICAN'
)

trace4 = go.Bar(
    x=causi.index,
    y=causi,
    name='CAUCASIAN'
)

data = [trace1, trace2,trace3,trace4]
layout = go.Layout(
    barmode='group',
    title= "Screening rate by ethnicity",
    yaxis= {'title':'screening rate'},
    xaxis={'title':"Age group"},
)

fig_eth = go.Figure(data=data, layout=layout)


hispi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["HOUSEHOLD_INCOME"].apply(lambda x:x=="$100K+")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
allo=dff[dff.groupby(["PATIENT_AGE_GROUP"])["HOUSEHOLD_INCOME"].apply(lambda x:x=="<$50-99K")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
african=dff[dff.groupby(["PATIENT_AGE_GROUP"])["HOUSEHOLD_INCOME"].apply(lambda x:x=="<=$49K")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
causi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["HOUSEHOLD_INCOME"].apply(lambda x:x=="UNKNOWN")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())

trace1 = go.Bar(
    x=hispi.index,
    y=hispi,
    name='$100k+'
)
trace2 = go.Bar(
    x=allo.index,
    y=allo,
    name='<$50-99K'
)

trace3 = go.Bar(
    x=african.index,
    y=african,
    name='<=$49K'
)

trace4 = go.Bar(
    x=causi.index,
    y=causi,
    name='UNKNOWN'
)

data = [trace1, trace2,trace3,trace4]
layout = go.Layout(
    barmode='group',
    title= "Screening rate by income",
    yaxis= {'title':'screening rate'},
    xaxis={'title':"Age group"},
)

fig_inc = go.Figure(data=data, layout=layout)


hispi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["EDUCATION_LEVEL"].apply(lambda x:x=="ASSOCIATE DEGREE AND ABOVE")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
allo=dff[dff.groupby(["PATIENT_AGE_GROUP"])["EDUCATION_LEVEL"].apply(lambda x:x=="HIGH SCHOOL OR LESS")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
african=dff[dff.groupby(["PATIENT_AGE_GROUP"])["EDUCATION_LEVEL"].apply(lambda x:x=="SOME COLLEGE")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())
causi=dff[dff.groupby(["PATIENT_AGE_GROUP"])["EDUCATION_LEVEL"].apply(lambda x:x=="UNKNOWN")].groupby(["PATIENT_AGE_GROUP"])["IS_SCREENER"].apply(lambda x:x.sum()/x.count())

trace1 = go.Bar(
    x=hispi.index,
    y=hispi,
    name='associate degree'
)
trace2 = go.Bar(
    x=allo.index,
    y=allo,
    name='high school'
)

trace3 = go.Bar(
    x=african.index,
    y=african,
    name='college'
)

trace4 = go.Bar(
    x=causi.index,
    y=causi,
    name='unknown'
)

data = [trace1, trace2,trace3,trace4]
layout = go.Layout(
    barmode='group',
    title= "Screening rate by education",
    yaxis= {'title':'screening rate'},
    xaxis={'title':"Age group"},
)

fig_edu = go.Figure(data=data, layout=layout)

data=pd.read_csv("helper_data/data_read.csv")
df_map = data.groupby("PATIENT_STATE")['IS_SCREENER'].mean().reset_index()
df2_map = data.groupby("PATIENT_STATE")['IS_SCREENER'].count().reset_index()
df_map.columns=['state','screening_rate']
df2_map.columns=['state','len']

for col in df_map.columns:
    df_map[col] = df_map[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

df_map['text'] = df_map['state'] + '<br>' + "|" +df2_map['len'].apply(lambda x:str(x))
graph_data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df_map['state'],
        z = df_map['screening_rate'].astype(float),
        locationmode = 'USA-states',
        text = df_map['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Screening Rate")
        ) ]

layout = dict(
        title = 'Screening Rate by State',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),)
    
fig_map = dict( data=graph_data, layout=layout )





app = dash.Dash(name='app7', sharing=True, server=server, url_base_pathname='/app8')

app.layout = html.Div(className='container', children=[
    html.Div(className="row", children=[
            html.H2(
                'Exploratory Data Analysis',
                id='title',
                style={'float': 'left',
                    'margin-top': '20px',
                    'margin-bottom': '0',
                    'margin-left': '7px'}
                
            ),

            html.Img(
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQW0j8jQYgAglxmwxx2mc-XKCuaFZhOo5eVyaNVogSQBctiQW8j",
                style={
                    'height': '100px',
                    'float': 'right'
                }
            )
        ]),
    html.Hr(),
    html.Div(className='two columns', children=[
        dcc.RadioItems(
            id='items',
            options=[
                {'label': '795', 'value': '795'},
                {'label': '86592', 'value': '86592'},
                {'label': 'V22.1', 'value': 'V22.1'},
                {'label': 'V72.31', 'value': 'V72.31'},
                {'label': 'Ethnicity', 'value': 'ETHNICITY'},
                {'label': 'Diagnosis count', 'value': 'DIAGNOSIS_COUNT'},
                {'label': 'Units', 'value': 'UNITS_ADMINISTERED|mean'},
                {'label': 'Activity timedelta', 'value': 'ACTIVITY_timedelta|median'},
                {'label': 'Imp.Feature', 'value': 'importance'},
                {'label': 'Screening-age', 'value': 'screener_rate'},
                {'label': 'Screening-states', 'value': 'outliers'},
                {'label': 'Screen-education', 'value': 'edu'},
                {'label': 'Screen-income', 'value': 'inc'},
                {'label': 'Screen-ethnicity', 'value': 'eth'},
                
            ],
            value='ETHNICITY',
            style={'display': 'block'}
            ),
        html.Hr(),
        dcc.RadioItems(
            id='points',
            options=[
                {'label': 'Display All Points', 'value': 'all'},
                {'label': 'Hide Points', 'value': False},
                {'label': 'Display Outliers', 'value': 'outliers'},
                {'label': 'Display Suspected Outliers', 'value': 'suspectedoutliers'},
            ],
            value='all',
            style={'display': 'block'}
        ),
        html.Hr(),
        html.Label('Jitter'),
        dcc.Slider(
            id='jitter',
            min=0,
            max=1,
            step=0.1,
            value=0.7,
            updatemode='drag'
        )
    ]),
    html.Div(dcc.Graph(id='graph'), className='ten columns')
],style={'backgroundColor': colors['background'],'width':'100%','height':'100%','max-width':50000,'max-height':50000})

@app.callback(
    Output('graph', 'figure'), [
    Input('items', 'value'),
    Input('points', 'value'),
    Input('jitter', 'value')])
def update_graph(value,points,jitter):
    if value in ['ETHNICITY','DIAGNOSIS_COUNT','UNITS_ADMINISTERED|mean','ACTIVITY_timedelta|median']:
        data_fig = []
        for j in range(0,len(pd.unique(df['IS_SCREENER']))):
            trace = {
                "type": 'violin',
                "x": df['IS_SCREENER'][df['IS_SCREENER'] == pd.unique(df['IS_SCREENER'])[j]],
                "y": df[value][df['IS_SCREENER'] == pd.unique(df['IS_SCREENER'])[j]],
                "name": pd.unique(df['IS_SCREENER'])[j],
                "box": {
                    "visible": True
                },
                "meanline": {
                    "visible": True
                }
                }
            data_fig.append(trace)

            
        return {
            'data': data_fig,
            'layout': {
                
                'title': "Violin Plot",
                "yaxis":{'title':'{}'.format(value)},
                "xaxis":{'title':"IS_SCREENER"},
                
            }
        }
    if value=="outliers":
        return fig_map
    if value=="edu":
        return fig_edu
    if value=="inc":
        return fig_inc
    if value=="eth":
        return fig_eth
    if value=="795":
        return fig_795 
    if value=="86592":
        return fig_86592
    if value=="V22.1":
        return fig_v221
    if value=="V72.31":
        return py.iplot(fig_v7231, validate = False)
    
    
    else:
        data=[]
        if value=='importance':
            trace = {
                        "type": 'bar',
                        "y": fid["importance"],
                        "x": fid["description"],
                        
                        "box": {
                            "visible": True
                        },
                        "meanline": {
                            "visible": True
                        }
                    }
            data.append(trace)

                    
            fig = {
                "data": data,
                "layout" : {
                    "title": "Feature Importance",
                    "yaxis": {
                        "title":"Feature score",
                        
                        "zeroline": False,
                        'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
                    },
                    
                }
            }
        else:

            data=[]
            trace = {
                    "type": 'bar',
                    
                    "x": screener_rates.index,
                    "y":screener_rates,
                    
                    "box": {
                        "visible": True
                    },
                    "meanline": {
                        "visible": True
                    }
                }
            data.append(trace)

                
            fig = {
            "data": data,
            "layout" : {
                "title": "Screening rate by age group",
                "yaxis": {
                    'title':'screening rate',
                    "zeroline": False,
                    'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
                },
                "xaxis":{'title':"Age group"},
            }
            }


    return fig
        

# Load external CSS
external_css = [
    "https://github.com/plotly/dash-app-stylesheets/blob/master/dash-uber-ride-demo.css",
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-tsne/master/custom_styles.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css",
    'https://codepen.io/chriddyp/pen/dZVMbK.css'
]

for css in external_css:
    app.css.append_css({"external_url": css})

external_jss=[
    'http://yui.yahooapis.com/3.0.0b1/build/yui/yui-min.js',
    'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    ]
for jss in external_jss:   
    app.scripts.append_script({'external_url': jss})




        

if __name__ == '__main__':
    app.run_server(debug=True)
