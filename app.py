# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:22:07 2018

@author: arlin
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os
import flask
from win32api import GetSystemMetrics

app = dash.Dash()
server = app.server

#controls
#type_facility_options = [{'label': str(FACILITY_TYPES[facility_type]),
#                      'value': str(facility_type)}
#                     for facility_type in FACILITY_TYPES]

total_data = pd.read_csv("map_creation/total_data.csv")
total_population = int(total_data["Pop_Prior_Aug_2017"].sum())
total_facilities_LearnC = int(total_data['learning_centers_per_region'].sum())
total_facilities_WomenFS = int(total_data["Women_Friendly_Space_per_region"].sum())
total_facilities_ChildFS = int(total_data["Child_Friendly_Space_per_region"].sum())
total_facilities_WASH = int(total_data["WASH_Infra_per_region"].sum())
total_facilities_NC = int(total_data["nutrition_centers_per_region"].sum())
total_facilities_HF = int(total_data["Health_Facility_per_region"].sum())

widthScreen = (GetSystemMetrics(0)-20)
heightScreen = (GetSystemMetrics(1)-200)
half_heightScreen = (heightScreen/2)
threeeight_heightScreen = (heightScreen/8*3)
twoeight_heightScreen = (heightScreen/8*2)
fifteen_heightScreen = (heightScreen/15)
thirty_heightScreen = (heightScreen/30)
sixth_heightScreen = (heightScreen/6)

dict_links_maps = {'sites': 'maps/all_sites.html',
              'vLearnC':'maps/all_LearnC.html',
              'vWFS':'maps/all_WomenFS.html',
              'vCFS':'maps/all_ChildFS.html',
              'vWASH':'maps/all_WASH.html',
              'vNC':'maps/all_NC.html',
              'vHF':'maps/all_HF.html'}

dict_links_numbers = {'sites': total_population,
              'vLearnC':total_facilities_LearnC,
              'vWFS':total_facilities_WomenFS,
              'vCFS':total_facilities_ChildFS,
              'vWASH':total_facilities_WASH,
              'vNC':total_facilities_NC,
              'vHF':total_facilities_HF}

dict_links_text = {'sites': 'People in Refugee Camps:',
              'vLearnC':'Learning Centers:',
              'vWFS':'Women Friendly Spaces:',
              'vCFS':'Child Friendly Spaces:',
              'vWASH':'WASH Facilities:',
              'vNC':'Nutrition Centers:',
              'vHF':'Health Facilities:'}

dict_links_boxplot = {'sites': 'https://plot.ly/~Eekhoorn234/35.embed',
              'vLearnC':'https://plot.ly/~Eekhoorn234/0.embed',
              'vWFS':'https://plot.ly/~Eekhoorn234/2.embed',
              'vCFS':'https://plot.ly/~Eekhoorn234/4.embed',
              'vWASH':'https://plot.ly/~Eekhoorn234/6.embed',
              'vNC':'https://plot.ly/~Eekhoorn234/8.embed',
              'vHF':'https://plot.ly/~Eekhoorn234/10.embed'}

dict_links_piechart = {'sites': 'https://plot.ly/~Eekhoorn234/43.embed',
              'vLearnC':'https://plot.ly/~Eekhoorn234/39.embed',
              'vWFS':'https://plot.ly/~Eekhoorn234/2.embed',
              'vCFS':'https://plot.ly/~Eekhoorn234/4.embed',
              'vWASH':'https://plot.ly/~Eekhoorn234/6.embed',
              'vNC':'https://plot.ly/~Eekhoorn234/41.embed',
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

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
        html.Div(className="banner",children=[
                html.Div(className='container scalable', style={'textAlign':'center', 'marginTop': 25,'marginBottom':0},children=[
                        html.H1(
                                html.A('Rohingya Refugee Camp Overview',
                                                                                            style={'textAlign': 'center',
                                                                                                   'color': '#1EAEDB',
                                                                                                   'fontFamily': 'verdana',
                                                                                                   'paddingLeft': 0,
                                                                                                   'paddingTop': 0,
                                                                                                   'paddingRight': 0,
                                                                                                   'marginTop':0,
                                                                                                   'marginBottom':0}), style={'marginBottom':0})])],
                                                            style = {'backgroundColor': '#FFFFFF', 'height': 70,'marginBottom':0}),
                                                               #html.A(html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"))      
                        html.Div(className="body",children=[
                                html.Div(children=[
                                        html.Div(children=[
                                                html.Div(
                                                        dcc.RadioItems(id='select_maps',
                                                                                                    options=[{'label': 'Campsites', 'value': 'sites'},
                                                                                                             {'label': 'Learning Centers', 'value': 'vLearnC'},
                                                                                                             #{'label': 'Women Friendly Spaces___ ', 'value': 'vWFS'},
                                                                                                             {'label': 'Child Friendly Spaces ', 'value': 'vCFS'},
                                                                                                             {'label': 'WASH Infrastructure', 'value': 'vWASH'},
                                                                                                             {'label': 'Nutrition Centers', 'value': 'vNC'},
                                                                                                             {'label': 'Health Facilities', 'value': 'vHF'}],
                                                                                                    value=['sites'],
                                                                                                    labelStyle={'display': 'inline-block'},
                                                                                                    style={'textAlign': 'center',
                                                                                                           'color': 'black',
                                                                                                           'fontFamily': 'verdana',
                                                                                                           'fontSize': '1.2rem'}))]),
                                        html.Div(children=[
                                        html.Div(children=[
                                                html.Div(children=[

                                                        html.H3(children=format(dict_links_text.get('sites')),
                                                                                                                    id='text',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': '#666666',
                                                                                                                                 'fontSize' : '1.8rem',
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': thirty_heightScreen}),
                                                        html.H2(format(dict_links_numbers.get('sites')),id='number',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': '#444444',
                                                                                                                                 'fontSize' : '3.5rem',
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': 0,
                                                                                                                                 'paddingBottom': thirty_heightScreen}),
]),
                                                         html.Div(html.Iframe(id='boxplot',src = 'https://plot.ly/~Eekhoorn234/35.embed',style={'border': 0, 'align': 'center', 'width': '100%', 'height':twoeight_heightScreen})),
                                                         html.Div(html.Iframe(id='piechart',src = 'https://plot.ly/~Eekhoorn234/43.embed',style={'border': 0, 'align': 'center', 'width': '100%', 'height':half_heightScreen}))],style={'position':'relative', 'height':heightScreen, 'align': 'center'},className='four columns'),
                                        html.Div(children=[
                                                html.Iframe(id='map_folium',srcDoc = open(format(dict_links_maps.get('sites')), 'r').read(),style={'border': 'none', 'align': 'center', 'width': '100%', 'height':heightScreen})],style={'position':'relative', 'height':heightScreen, 'align': 'center'},className='eight columns')],
                                        style={'position':'relative', 'height':heightScreen, 'align': 'center'},className='row')])])])
                                                
                                                
"""                                                
                                                className="body", children=[html.Div(
                                                                            html.Div(children=[
                                                                                        html.Div(children=[
                                                                                                html.Div(children=[html.Iframe(id='boxplot',src = 'https://plot.ly/~Eekhoorn234/35.embed',style={'border': 0, 'align': 'center', 'width': '100%', 'height':twoeight_heightScreen})],className='four columns',style={'padding': 20}),
                                                                                                html.Div(children=[
                                                                                                            html.H2(children=format(dict_links_numbers.get('sites')),
                                                                                                                    id='number',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': '#444444',
                                                                                                                                 'fontSize' : '3.5rem',
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': fifteen_heightScreen}),
                                                                                                             html.H3(children=format(dict_links_text.get('sites')),
                                                                                                                    id='text',
                                                                                                                    style={'textAlign': 'center',
                                                                                                                                 'color': '#666666',
                                                                                                                                 'fontSize' : '2rem',
                                                                                                                                 'fontFamily': 'verdana',
                                                                                                                                 'backgroundColor' : 'white',
                                                                                                                                 'border': 'none',
                                                                                                                                 'paddingTop': 0})],
                                                                                                        style={'borderTop': 10, 'align': 'center',  'height':twoeight_heightScreen, 'marginLeft': 0},className='four columns'),
                                                                                                           # html.Iframe(id='number',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 'none', 'align': 'center', 'width': '100%', 'height':deel_heightScreen}),
                                                                                                            
                                                                                                html.Div(children=[html.Iframe(id='piechart2',src = 'https://plot.ly/~Eekhoorn234/10.embed',style={'border': 0, 'align': 'center', 'width': '100%', 'height':twoeight_heightScreen})],className='four columns',style={'padding': 20})
                                                                                                            ]),

                                                                                        html.Div(children=[
                                                                                                html.Div(children=[
                                                                                                        html.Iframe(id='piechart',src = 'https://plot.ly/~Eekhoorn234/43.embed',style={'border': 0, 'align': 'center', 'width': '100%', 'height':half_heightScreen})],className='four columns',style={'padding': 20}),
                                                                                                html.Div(children=[html.Iframe(id='map_folium',srcDoc = open(format(dict_links_maps.get('sites')), 'r').read(),style={'border': 'none', 'align': 'center', 'width': '100%', 'height':heightScreen})],style={'position':'relative', 'height':heightScreen, 'align': 'center'},className='eight columns')
                                                                                                #html.Iframe(id='map_foliumsites',srcDoc = open(format(dict_links_maps.get('sites')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none', 'padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumLearnC',srcDoc = open(format(dict_links_maps.get('vLearnC')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none','padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumWomenFS',srcDoc = open(format(dict_links_maps.get('vWFS')), 'r').read(),style={'border': 'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumChildFS',srcDoc = open(format(dict_links_maps.get('vCFS')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none','padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumWASH',srcDoc = open(format(dict_links_maps.get('vWASH')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none','padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumNC',srcDoc = open(format(dict_links_maps.get('vNC')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none','padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                #html.Iframe(id='map_foliumHF',srcDoc = open(format(dict_links_maps.get('vHF')), 'r').read(),style={'lineHeight': 0,'margin': 'none','border': 'none','padding':'none', 'align': 'center', 'width': '100%'}),
                                                                                                           ],

                                                                                        style={'position':'relative', 'height':heightScreen, 'align': 'center'},className='row')
                                                                                    
                                                                                        ],
                                                                            )]
                                                
                                                )
                                        ]
                    )

#"""
#"""
@app.callback(
    Output(component_id='map_folium', component_property='srcDoc'),
    [Input(component_id='select_maps', component_property='value')])
def update_map(select_maps):
    new_src = format(dict_links_maps.get(select_maps))
    return open(new_src, 'r').read()
#"""
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

@app.callback(
    Output(component_id='piechart', component_property='src'),
    [Input(component_id='select_maps', component_property='value')])
def update_piechart(select_maps):
    new_src = format(dict_links_piechart.get(select_maps))
    return new_src
"""
@app.callback(
    Output(component_id='map_foliumsites', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapsites(select_maps):
    if select_maps == 'sites':
        return heightScreen
    elif select_maps == 'vLearnC':
        return 0
    elif select_maps == 'vCFS':
        return 0
    elif select_maps == 'vWASH':
        return 0
    elif select_maps == 'vNC':
        return 0
    elif select_maps == 'vHF':
        return 0
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumLearnC', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapLearnC(select_maps):
    if select_maps == 'vLearnC':
        return heightScreen
    elif select_maps == 'sites':
        return 0
    elif select_maps == 'vCFS':
        return 0
    elif select_maps == 'vWASH':
        return 0
    elif select_maps == 'vNC':
        return 0
    elif select_maps == 'vHF':
        return 0
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumChildFS', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapChildFS(select_maps):
    if select_maps == 'vCFS':
        return heightScreen
    elif select_maps == 'vLearnC':
        return 0
    elif select_maps == 'sites':
        return 0
    elif select_maps == 'vWASH':
        return 0
    elif select_maps == 'vNC':
        return 0
    elif select_maps == 'vHF':
        return 0
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumWASH', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapWASH(select_maps):
    if select_maps == 'vWASH':
        return heightScreen
    elif select_maps == 'vLearnC':
        return 0
    elif select_maps == 'vCFS':
        return 0
    elif select_maps == 'sites':
        return 0
    elif select_maps == 'vNC':
        return 0
    elif select_maps == 'vHF':
        return 0
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumNC', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapNC(select_maps):
    if select_maps == 'vNC':
        return heightScreen
    elif select_maps == 'vLearnC':
        return 0
    elif select_maps == 'vCFS':
        return 0
    elif select_maps == 'vWASH':
        return 0
    elif select_maps == 'sites':
        return 0
    elif select_maps == 'vHF':
        return 0
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumHF', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapHF(select_maps):
    if select_maps == 'vHF':
        return heightScreen
    elif select_maps == 'vLearnC':
        return 0
    elif select_maps == 'vCFS':
        return 0
    elif select_maps == 'vWASH':
        return 0
    elif select_maps == 'vNC':
        return 0
    elif select_maps == 'sites':
        return 0
    else:
        return 0
"""

  
"""
@app.callback(
    Output(component_id='map_foliumLearnC', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapLearnC(select_maps):
    if select_maps == 'vLearnC':
        return heightScreen
    else:
        return 0
"""
"""
@app.callback(
    Output(component_id='map_foliumWomenFS', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapWomenFS(select_maps):
    if select_maps == 'vWFS':
        return heightScreen
    else:
        return 0
"""
"""
@app.callback(
    Output(component_id='map_foliumChildFS', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapsChildFS(select_maps):
    if select_maps == 'vCFS':
        return heightScreen
    else:
        return 0

@app.callback(
    Output(component_id='map_foliumWASH', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapsWASH(select_maps):
    if select_maps == 'vWASH':
        return heightScreen
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumNC', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapsNC(select_maps):
    if select_maps == 'vNC':
        return heightScreen
    else:
        return 0
    
@app.callback(
    Output(component_id='map_foliumHF', component_property='height'),
    [Input(component_id='select_maps', component_property='value')])
def update_mapsHF(select_maps):
    if select_maps == 'vHF':
        return heightScreen
    else:
        return 0
"""




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