# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:22:07 2018

@author: arlin
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import flask
from win32api import GetSystemMetrics

app = dash.Dash()
server = app.server

#controls
#type_facility_options = [{'label': str(FACILITY_TYPES[facility_type]),
#                      'value': str(facility_type)}
#                     for facility_type in FACILITY_TYPES]


widthScreen = (GetSystemMetrics(0)-20)
heightScreen = (GetSystemMetrics(1)-200)
deel_heightScreen = (heightScreen/3)

dict_links = {'sites': 'maps/all_sites.html',
              'vLearnC':'maps/all_LearnC.html',
              'vWFS':'maps/all_WomenFS.html',
              'vCFS':'maps/all_ChildFS.html',
              'vWASH':'maps/all_WASH.html',
              'vNC':'maps/all_NC.html'}

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
                             children=[html.Div(className="banner", 
                                                children=[html.Div(className='container scalable', 
                                                                   style={'textAlign':'left'}, 
                                                                   children=[html.H2(html.A('Rohingya Refugee Camp Overview',
                                                                                            style={'textAlign': 'left',
                                                                                                   'color': 'white',
                                                                                                   'fontFamily': 'verdana',
                                                                                                   'paddingLeft': 0,
                                                                                                   'paddingTop': 0,
                                                                                                   'paddingRight': 0,
                                                                                                   'marginTop':0}))])]),
                                                         #html.A(html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"))
                                        html.Div(className="body", children=[html.Div(dcc.RadioItems(id='select_maps',
                                                                                                    options=[{'label': 'Campsites ', 'value': 'sites'},
                                                                                                             {'label': 'Learning Centers ', 'value': 'vLearnC'},
                                                                                                             {'label': 'Women Friendly Spaces ', 'value': 'vWFS'},
                                                                                                             {'label': 'Child Friendly Spaces ', 'value': 'vCFS'},
                                                                                                             {'label': 'WASH Infrastructure ', 'value': 'vWASH'},
                                                                                                             {'label': 'Nutrition Centers ', 'value': 'vNC'},
                                                                                                             {'label': 'Health Facilities ', 'value': 'vHF'}],
                                                                                                    value=['sites'],
                                                                                                    labelStyle={'display': 'inline-block'},
                                                                                                    style={'textAlign': 'center',
                                                                                                           'color': 'orange',
                                                                                                           'fontFamily': 'verdana',
                                                                                                           'fontSize': 12}),className="row"),
                                                                            html.Div(children=[
                                                                                        html.Div(children=[
                                                                                                            html.Iframe(id='boxplot',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':deel_heightScreen}),
                                                                                                            html.Iframe(id='circlediagram',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':deel_heightScreen}),
                                                                                                            html.Iframe(id='graph',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':deel_heightScreen})],style={'position':'relative', 'height':heightScreen},className='four columns'),
                                                                                        
                                                                                        html.Div(children=[html.H6('Rohingya Refugee Camp Overview',
                                                                                                                          style={'textAlign': 'left',
                                                                                                                                 'color': 'black',
                                                                                                                                 'fontSize' : 12,
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'paddingLeft': 0,
                                                                                                                                 'paddingTop': 0,
                                                                                                                                 'paddingRight': 0,
                                                                                                                                 'marginTop':0,
                                                                                                                                 'borderSize': 0,
                                                                                                                                 'backgroundColor' : 'white'}),
                                                                                                           html.Iframe(id='map_folium',srcDoc = open('maps/all_sites.html', 'r').read(),style={'border': 'none', 'align': 'center', 'width': '100%', 'height':heightScreen})],
                                                                                        style={'position':'relative', 'height':heightScreen},className='eight columns')],
                                                                            className='row')]
                                                
                                                )
                                        ]
                    )




"""

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1(
        children='Rohingya Refugee Camp Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontFamily': 'verdana'
            
        }
    ),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])
"""

@app.callback(
    Output(component_id='map_folium', component_property='srcDoc'),
    [Input(component_id='select_maps', component_property='value')])
def update_map(select_maps):
    new_src = format(dict_links.get(select_maps))
    return open(new_src, 'r').read()

external_css = [
    # Normalize the CSS
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # Fonts
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    # Base Stylesheet, replace this with your own base-styles.css using Rawgit
    "https://rawgit.com/xhlulu/9a6e89f418ee40d02b637a429a876aa9/raw/f3ea10d53e33ece67eb681025cedc83870c9938d/base-styles.css",
    # Custom Stylesheet, replace this with your own custom-styles.css using Rawgit
    "https://cdn.rawgit.com/plotly/dash-svm/bb031580/custom-styles.css"
]



@server.route('/static/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'static'), path)

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)