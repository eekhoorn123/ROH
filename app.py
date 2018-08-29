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
threeeight_heightScreen = (heightScreen/8*3)
twoeight_heightScreen = (heightScreen/8*2)
fifteen_heightScreen = (heightScreen/15)
thirty_heightScreen = (heightScreen/30)

dict_links_maps = {'sites': 'maps/all_sites.html',
              'vLearnC':'maps/all_LearnC.html',
              'vWFS':'maps/all_WomenFS.html',
              'vCFS':'maps/all_ChildFS.html',
              'vWASH':'maps/all_WASH.html',
              'vNC':'maps/all_NC.html',
              'vHF':'maps/all_HF.html'}

dict_links_numbers = {'sites': '0',
              'vLearnC':'1',
              'vWFS':'2',
              'vCFS':'3',
              'vWASH':'4',
              'vNC':'5',
              'vHF':'6'}

dict_links_text = {'sites': 'People in Refugee Camps',
              'vLearnC':'Learning Centers',
              'vWFS':'Women Friendly Spaces',
              'vCFS':'Child Friendly Spaces',
              'vWASH':'WASH Facilities',
              'vNC':'Nutrition Centers',
              'vHF':'Health Facilities'}

dict_links_boxplot = {'sites': 'https://plot.ly/~Eekhoorn234/15.embed',
              'vLearnC':'https://plot.ly/~Eekhoorn234/0.embed',
              'vWFS':'https://plot.ly/~Eekhoorn234/2.embed',
              'vCFS':'https://plot.ly/~Eekhoorn234/4.embed',
              'vWASH':'https://plot.ly/~Eekhoorn234/6.embed',
              'vNC':'https://plot.ly/~Eekhoorn234/8.embed',
              'vHF':'https://plot.ly/~Eekhoorn234/10.embed'}

dict_links_colours = {'sites': 'black',
              'vLearnC':'orange',
              'vWFS':'pink',
              'vCFS':'lightblue',
              'vWASH':'blue',
              'vNC':'lightorange',
              'vHF':'red'}

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
                                                                                                    options=[{'label': 'Campsites___', 'value': 'sites'},
                                                                                                             {'label': 'Learning Centers___', 'value': 'vLearnC'},
                                                                                                             {'label': 'Women Friendly Spaces___ ', 'value': 'vWFS'},
                                                                                                             {'label': 'Child Friendly Spaces___ ', 'value': 'vCFS'},
                                                                                                             {'label': 'WASH Infrastructure___ ', 'value': 'vWASH'},
                                                                                                             {'label': 'Nutrition Centers___ ', 'value': 'vNC'},
                                                                                                             {'label': 'Health Facilities___', 'value': 'vHF'}],
                                                                                                    value=['sites'],
                                                                                                    labelStyle={'display': 'inline-block'},
                                                                                                    style={'textAlign': 'center',
                                                                                                           'color': 'black',
                                                                                                           'fontFamily': 'verdana',
                                                                                                           'fontSize': 12}),className="row"),
                                                                            html.Div(children=[
                                                                                        html.Div(children=[
                                                                                                            html.Div(children=[
                                                                                                            html.H2(children=format(dict_links_numbers.get('sites')),
                                                                                                                    id='number',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': 'fc8600',
                                                                                                                                 'fontSize' : 50,
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': fifteen_heightScreen}),
                                                                                                             html.H3(children=format(dict_links_text.get('sites')),
                                                                                                                    id='text',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': 'fc8600',
                                                                                                                                 'fontSize' : 20,
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': 0})],
                                                                                                        style={'border': 'none', 'align': 'center', 'width': '100%', 'height':twoeight_heightScreen}),
                                                                                                           # html.Iframe(id='number',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':deel_heightScreen}),
                                                                                                            html.Iframe(id='boxplot',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':threeeight_heightScreen}),
                                                                                                            html.Iframe(id='graph',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':threeeight_heightScreen})],style={'position':'relative', 'height':heightScreen},className='four columns'),
                                                                                        
                                                                                        html.Div(children=[
                                                                                                           html.Iframe(id='map_folium',srcDoc = open('maps/all_sites.html', 'r').read(),style={'border': 'none', 'align': 'center', 'width': '100%', 'height':heightScreen})],
                                                                                        style={'position':'relative', 'height':heightScreen},className='eight columns')],
                                                                            className='row')]
                                                
                                                )
                                        ]
                    )



@app.callback(
    Output(component_id='map_folium', component_property='srcDoc'),
    [Input(component_id='select_maps', component_property='value')])
def update_map(select_maps):
    new_src = format(dict_links_maps.get(select_maps))
    return open(new_src, 'r').read()

@app.callback(
    Output(component_id='number', component_property='children'),
    [Input(component_id='select_maps', component_property='value')])
def update_numbers(select_maps):
    new_no = format(dict_links_numbers.get(select_maps))
    return new_no

@app.callback(
    Output(component_id='text', component_property='children'),
    [Input(component_id='select_maps', component_property='value')])
def update_text(select_maps):
    new_text = format(dict_links_text.get(select_maps))
    return new_text

@app.callback(
    Output(component_id='boxplot', component_property='src'),
    [Input(component_id='select_maps', component_property='value')])
def update_boxplot(select_maps):
    new_src = format(dict_links_boxplot.get(select_maps))
    return new_src




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