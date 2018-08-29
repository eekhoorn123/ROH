# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:42:44 2018

@author: arlin
"""

import pandas as pd

import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame

import urllib

import json
import geojson

from shapely.geometry import Point

import numpy as np

import pyproj

import shapely.wkt

import requests

import fiona

import seaborn as sns

import osmnx as ox

import contextily as ctx

import matplotlib.pyplot as plt
import mplleaflet
from mpl_toolkits.basemap import Basemap

import folium
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import HeatMap

import plotly.plotly as ply
from plotly import offline
import plotly
import plotly.graph_objs as go
import plotly.dashboard_objs as dashboard
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *


import IPython.display
from IPython.display import Image

import re

#Get dataset with polygons, so we van calculate areas
link = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Rohingya_Refugee_Camps_Sites_Outline_May_18/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryPolygon&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
request = requests.get(link)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    data_polygons = gpd.GeoDataFrame.from_features(f, crs=crs)

    
#Give both datasets the same name
data_polygons = data_polygons.rename(columns={'New_Camp_N': 'New_Camp_Name'})

#Get dataset with populations
link = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_Location_Masterlist_June_2018/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
request = requests.get(link)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    data_pop = gpd.GeoDataFrame.from_features(f, crs=crs)
    
link = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_Location_Masterlist_June_2018/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
request = requests.get(link)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    data_pop = gpd.GeoDataFrame.from_features(f, crs=crs)

#make dataset
total_data = gpd.sjoin(data_polygons, data_pop, how="inner", op='contains')
#print(len(total_data), total_data.head(2))

#set geometry for the dataset
total_data["area"] = total_data['geometry'].area#/ 10**6
#total_data.head()

#a list with al the link data
all_links = []

#one by one we get de data
Link_Location_Camps = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_Location_Masterlist_June_2018/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Location_Camps)
request = requests.get(Link_Location_Camps)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Location_Camps = gpd.GeoDataFrame.from_features(f, crs=crs)

LC = folium.FeatureGroup(name='Location Camps')
for lat,lon,name in zip(Location_Camps['Latitude'],Location_Camps['Longitude'],Location_Camps['New_Camp_Name']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='green')).add_to(LC)

Link_Latest_CiC_Offices = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_CiC_Office/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Latest_CiC_Offices)
request = requests.get(Link_Latest_CiC_Offices)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Latest_CiC_Offices = gpd.GeoDataFrame.from_features(f, crs=crs)

CIC = folium.FeatureGroup(name='Latest CiC Offices')
for lat,lon,name in zip(Latest_CiC_Offices['Latitude'],Latest_CiC_Offices['Longitude'],Latest_CiC_Offices['Name']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='green')).add_to(CIC)

Link_Learning_Center = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Learning_Center_(Round_4)/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Learning_Center)
request = requests.get(Link_Learning_Center)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Learning_Center = gpd.GeoDataFrame.from_features(f, crs=crs)

LearnC = folium.FeatureGroup(name='Learning Center')
for lat,lon,name in zip(Learning_Center['Latitude'],Learning_Center['Longitude'],Learning_Center['school_name']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='orange')).add_to(LearnC)
   
Link_Women_Friendly_Space = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Women_Friendly_Space/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Women_Friendly_Space)
request = requests.get(Link_Women_Friendly_Space)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Women_Friendly_Space = gpd.GeoDataFrame.from_features(f, crs=crs)

WomenFS = folium.FeatureGroup(name='Women Friendly Space')
for lat,lon,name in zip(Women_Friendly_Space['Latitude'],Women_Friendly_Space['Longitude'],Women_Friendly_Space['Facility']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='pink')).add_to(WomenFS)

Link_Child_Friendly_Space = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Child_Friendly_Space/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Child_Friendly_Space)
request = requests.get(Link_Child_Friendly_Space)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Child_Friendly_Space = gpd.GeoDataFrame.from_features(f, crs=crs)

ChildFS = folium.FeatureGroup(name='Child Friendly Space')
for lat,lon,name in zip(Child_Friendly_Space['Latitude'],Child_Friendly_Space['Longitude'],Child_Friendly_Space['Facility']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='blue')).add_to(ChildFS)
    
Link_WASH_Infra = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Updated_WASH_infrastructure_Round_7/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_WASH_Infra)
request = requests.get(Link_WASH_Infra)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    WASH_Infra = gpd.GeoDataFrame.from_features(f, crs=crs)

WASHI = folium.FeatureGroup(name='WASH Infrastructure')
for lat,lon,name in zip(WASH_Infra['Latitude'],WASH_Infra['Longitude'],WASH_Infra['Str_sub_type']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='lightblue')).add_to(WASHI)
   
Link_Mosque_Infra = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Updated_mosque_madrasa_infrastructures/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Mosque_Infra)
request = requests.get(Link_Mosque_Infra)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Mosque_Infra = gpd.GeoDataFrame.from_features(f, crs=crs)

MosqueI = folium.FeatureGroup(name='Mosque Infrastructure')
for lat,lon,name in zip(Mosque_Infra['Latitude'],Mosque_Infra['Longitude'],Mosque_Infra['SSID']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='purple')).add_to(MosqueI)
   
Link_Nutrition_Center = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Nutrition_Center_April_18/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Nutrition_Center)
request = requests.get(Link_Nutrition_Center)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Nutrition_Center = gpd.GeoDataFrame.from_features(f, crs=crs)

NC = folium.FeatureGroup(name='Nutrition Centers')
for lat,lon,name in zip(Nutrition_Center['Latitude'],Nutrition_Center['Longitude'],Nutrition_Center['Site_name']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='beige')).add_to(NC)
    
Link_Health_Facility = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Health_Facility_(Round_4)/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Health_Facility)
request = requests.get(Link_Health_Facility)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Health_Facility = gpd.GeoDataFrame.from_features(f, crs=crs)

HF = folium.FeatureGroup(name='Health Facility')
for lat,lon,name in zip(Health_Facility['Lat'],Health_Facility['Long'],Health_Facility['Type']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='red')).add_to(HF)
   
Link_Bridges = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_Bridges_May_2018/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Bridges)
request = requests.get(Link_Bridges)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Bridges = gpd.GeoDataFrame.from_features(f, crs=crs)
    
Br = folium.FeatureGroup(name='Bridges')
    
Link_Road_Network = 'https://services5.arcgis.com/QYf5PkPqzJKVzrmF/arcgis/rest/services/Latest_Road_Network_NYPLEDA_July_2018/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token='
all_links.append(Link_Road_Network)
request = requests.get(Link_Road_Network)
b = bytes(request.content)
with fiona.BytesCollection(b) as f:
    crs = f.crs
    Road_Network = gpd.GeoDataFrame.from_features(f, crs=crs)

Roads = folium.FeatureGroup(name='Road Network')

#generating heatmaps for each dataset
geodata_Location_Camps=[[row['Latitude'],row['Longitude']] for index, row in Location_Camps.iterrows()]
HMLC = folium.FeatureGroup(name='Location Camps Heatmap')
HeatMap(geodata_Location_Camps).add_to(HMLC)

geodata_Latest_CiC_Offices=[[row['Latitude'],row['Longitude']] for index, row in Latest_CiC_Offices.iterrows()]
HMCIC = folium.FeatureGroup(name='Latest CiC Offices Heatmap')
HeatMap(geodata_Latest_CiC_Offices).add_to(HMCIC)

geodata_Learning_Center=[[row['Latitude'],row['Longitude']] for index, row in Learning_Center.iterrows()]
HMLearnC = folium.FeatureGroup(name='Learning Center Heatmap')
HeatMap(geodata_Learning_Center).add_to(HMLearnC)

geodata_Women_Friendly_Space=[[row['Latitude'],row['Longitude']] for index, row in Women_Friendly_Space.iterrows()]
HMWomenFS = folium.FeatureGroup(name='Women Friendly Space Heatmap')
HeatMap(geodata_Women_Friendly_Space).add_to(HMWomenFS)

geodata_Child_Friendly_Space=[[row['Latitude'],row['Longitude']] for index, row in Child_Friendly_Space.iterrows()]
HMChildFS = folium.FeatureGroup(name='Child Friendly Space Heatmap')
HeatMap(geodata_Child_Friendly_Space).add_to(HMChildFS)

geodata_WASH_Infra=[[row['Latitude'],row['Longitude']] for index, row in WASH_Infra.iterrows()]
HMWASHI = folium.FeatureGroup(name='WASH Infrastructure Heatmap')
HeatMap(geodata_WASH_Infra).add_to(HMWASHI)

geodata_Mosque_Infra=[[row['Latitude'],row['Longitude']] for index, row in Mosque_Infra.iterrows()]
HMMosqueI = folium.FeatureGroup(name='Mosque Infrastructure Heatmap')
HeatMap(geodata_Mosque_Infra).add_to(HMMosqueI)

geodata_Nutrition_Center=[[row['Latitude'],row['Longitude']] for index, row in Nutrition_Center.iterrows()]
HMNC = folium.FeatureGroup(name='Nutrition Centers Heatmap')
HeatMap(geodata_Nutrition_Center).add_to(HMNC)

geodata_Health_Facility=[[row['Lat'],row['Long']] for index, row in Health_Facility.iterrows()]
HMHF = folium.FeatureGroup(name='Health Facility Heatmap')
HeatMap(geodata_Health_Facility).add_to(HMHF)


HMBr = folium.FeatureGroup(name='Bridges Heatmap')
HMRoads = folium.FeatureGroup(name='Road Network Heatmap')

DensLearnC = folium.FeatureGroup(name='Density Learning Centers')

#calculate distances to certain spots

DistWASHI = folium.FeatureGroup(name='Areas wit a >5 min walking distance to a WASH Facility')
for index, row in WASH_Infra.iterrows():
    folium.Circle([row['Latitude'], row['Longitude']],
                        radius=420,
                        popup=row['Str_sub_type'],
                        fill_color="#3db7e4"
                       ).add_to(DistWASHI)
    
DistNC = folium.FeatureGroup(name='Areas wit a >5 min walking distance to a Nutrition Center')
for index, row in Nutrition_Center.iterrows():
    folium.Circle([row['Latitude'], row['Longitude']],
                        radius=420,
                        popup=row['EA_Number'],
                        fill_color="#3db7e4"
                       ).add_to(DistNC)

#calculate density per region
total_data['density'] = total_data["Pop_Prior_Aug_2017"] / total_data["area"]

#plot density per campsite
DensPop = folium.FeatureGroup(name='Density Population')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['density']) >= 0) & ((feature['properties']['density']) < (total_data['density'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['density']) >= (total_data['density'].quantile(q=0.25))) & ((feature['properties']['density']) < (total_data['density'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['density']) >= (total_data['density'].quantile(q=0.5))) & ((feature['properties']['density']) < (total_data['density'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.5,
        'dashArray': '1, 1'
    }).add_to(DensPop)

    #calculate number of learning centers per person per region
#set geometry for the geo-dataframe
geometry = Learning_Center.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(Learning_Center)):
        b = (Learning_Center.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
learning_centers_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    learning_centers_per_region = pd.concat([learning_centers_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['learning_centers_per_region'] = learning_centers_per_region['Facilities']
total_data['learning_centers_per_region'] = total_data['learning_centers_per_region'].replace({0:np.nan})
total_data['learning_centers_per_region'].fillna(0, inplace=True)
total_data['persons_per_learning_centers_per_region'] = total_data['Curr_Total_Pop']/total_data['learning_centers_per_region']
total_data['persons_per_learning_centers_per_region'] = total_data['persons_per_learning_centers_per_region'].replace({np.inf:np.nan})
total_data['persons_per_learning_centers_per_region'].fillna(0, inplace=True)
#plot number of facilities per region (the darker the more)
#total_data.plot(column='nutrition_centers_per_region', cmap='OrRd', scheme='quantiles')#pr, scheme='fisher_jenks')

#plot density per campsite
DensLC = folium.FeatureGroup(name='Density Learning Centers')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_learning_centers_per_region']) >= 0) & ((feature['properties']['persons_per_learning_centers_per_region']) < (total_data['persons_per_learning_centers_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_learning_centers_per_region']) >= (total_data['persons_per_learning_centers_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_learning_centers_per_region']) < (total_data['persons_per_learning_centers_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_learning_centers_per_region']) >= (total_data['persons_per_learning_centers_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_learning_centers_per_region']) < (total_data['persons_per_learning_centers_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensLC)
    
#calculate number of Women Friendly Spaces per person per region
#set geometry for the geo-dataframe
geometry = Women_Friendly_Space.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(Women_Friendly_Space)):
        b = (Women_Friendly_Space.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
Women_Friendly_Space_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    Women_Friendly_Space_per_region = pd.concat([Women_Friendly_Space_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['Women_Friendly_Space_per_region'] = Women_Friendly_Space_per_region['Facilities']
total_data['Women_Friendly_Space_per_region'] = total_data['Women_Friendly_Space_per_region'].replace({0:np.nan})
total_data['Women_Friendly_Space_per_region'].fillna(0, inplace=True)
total_data['persons_per_Women_Friendly_Space_per_region'] = total_data['Curr_Total_Pop']/total_data['Women_Friendly_Space_per_region']
total_data['persons_per_Women_Friendly_Space_per_region'] = total_data['persons_per_Women_Friendly_Space_per_region'].replace({np.inf:np.nan})
total_data['persons_per_Women_Friendly_Space_per_region'].fillna(0, inplace=True)
#plot density per campsite
DensWFS = folium.FeatureGroup(name='Density Women Friendly Spaces')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) >= 0) & ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) < (total_data['persons_per_Women_Friendly_Space_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) >= (total_data['persons_per_Women_Friendly_Space_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) < (total_data['persons_per_Women_Friendly_Space_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) >= (total_data['persons_per_Women_Friendly_Space_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_Women_Friendly_Space_per_region']) < (total_data['persons_per_Women_Friendly_Space_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensWFS)
    
#calculate number of child friendly spaces per person per region
#set geometry for the geo-dataframe
geometry = Child_Friendly_Space.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(Child_Friendly_Space)):
        b = (Child_Friendly_Space.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
Child_Friendly_Space_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    Child_Friendly_Space_per_region = pd.concat([Child_Friendly_Space_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['Child_Friendly_Space_per_region'] = learning_centers_per_region['Facilities']
total_data['Child_Friendly_Space_per_region'] = total_data['Child_Friendly_Space_per_region'].replace({0:np.nan})
total_data['Child_Friendly_Space_per_region'].fillna(0, inplace=True)
total_data['persons_per_Child_Friendly_Space_per_region'] = total_data['Curr_Total_Pop']/total_data['Child_Friendly_Space_per_region']
total_data['persons_per_Child_Friendly_Space_per_region'] = total_data['persons_per_Child_Friendly_Space_per_region'].replace({np.inf:np.nan})
total_data['persons_per_Child_Friendly_Space_per_region'].fillna(0, inplace=True)
#plot number of facilities per region (the darker the more)
#total_data.plot(column='nutrition_centers_per_region', cmap='OrRd', scheme='quantiles')#pr, scheme='fisher_jenks')

#plot density per campsite
DensCFS = folium.FeatureGroup(name='Density Child_Friendly_Space')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) >= 0) & ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) < (total_data['persons_per_Child_Friendly_Space_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) >= (total_data['persons_per_Child_Friendly_Space_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) < (total_data['persons_per_Child_Friendly_Space_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) >= (total_data['persons_per_Child_Friendly_Space_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_Child_Friendly_Space_per_region']) < (total_data['persons_per_Child_Friendly_Space_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensCFS)
    
#calculate number of WASH Infra per person per region
#set geometry for the geo-dataframe
geometry = WASH_Infra.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(WASH_Infra)):
        b = (WASH_Infra.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
WASH_Infra_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    WASH_Infra_per_region = pd.concat([WASH_Infra_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['WASH_Infra_per_region'] = learning_centers_per_region['Facilities']
total_data['WASH_Infra_per_region'] = total_data['WASH_Infra_per_region'].replace({0:np.nan})
total_data['WASH_Infra_per_region'].fillna(0, inplace=True)
total_data['persons_per_WASH_Infra_per_region'] = total_data['Curr_Total_Pop']/total_data['WASH_Infra_per_region']
total_data['persons_per_WASH_Infra_per_region'] = total_data['persons_per_WASH_Infra_per_region'].replace({np.inf:np.nan})
total_data['persons_per_WASH_Infra_per_region'].fillna(0, inplace=True)

#plot number of facilities per region (the darker the more)
#total_data.plot(column='nutrition_centers_per_region', cmap='OrRd', scheme='quantiles')#pr, scheme='fisher_jenks')

#plot density per campsite
DensWASH = folium.FeatureGroup(name='Density WASH Infra')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_WASH_Infra_per_region']) >= 0) & ((feature['properties']['persons_per_WASH_Infra_per_region']) < (total_data['persons_per_WASH_Infra_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_WASH_Infra_per_region']) >= (total_data['persons_per_WASH_Infra_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_WASH_Infra_per_region']) < (total_data['persons_per_WASH_Infra_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_WASH_Infra_per_region']) >= (total_data['persons_per_WASH_Infra_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_WASH_Infra_per_region']) < (total_data['persons_per_WASH_Infra_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensWASH)
    
#calculate number of nutrition centers per person per region
#set geometry for the geo-dataframe
geometry = Nutrition_Center.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(Nutrition_Center)):
        b = (Nutrition_Center.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
nutrition_centers_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    nutrition_centers_per_region = pd.concat([nutrition_centers_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['nutrition_centers_per_region'] = nutrition_centers_per_region['Facilities']
total_data['nutrition_centers_per_region'] = total_data['nutrition_centers_per_region'].replace({0:np.nan})
total_data['nutrition_centers_per_region'].fillna(0, inplace=True)
total_data['persons_per_nutrition_centers_per_region'] = total_data['Curr_Total_Pop']/total_data['nutrition_centers_per_region']
total_data['persons_per_nutrition_centers_per_region'] = total_data['persons_per_nutrition_centers_per_region'].replace({np.inf:np.nan})
total_data['persons_per_nutrition_centers_per_region'].fillna(0, inplace=True)
#plot number of facilities per region (the darker the more)
#total_data.plot(column='nutrition_centers_per_region', cmap='OrRd', scheme='quantiles')#pr, scheme='fisher_jenks')

#plot density per campsite
DensNC = folium.FeatureGroup(name='Density Nutrition Centers')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_nutrition_centers_per_region']) >= 0) & ((feature['properties']['persons_per_nutrition_centers_per_region']) < (total_data['persons_per_nutrition_centers_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_nutrition_centers_per_region']) >= (total_data['persons_per_nutrition_centers_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_nutrition_centers_per_region']) < (total_data['persons_per_nutrition_centers_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_nutrition_centers_per_region']) >= (total_data['persons_per_nutrition_centers_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_nutrition_centers_per_region']) < (total_data['persons_per_nutrition_centers_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensNC)
    
#calculate number of Health_Facility per person per region
#set geometry for the geo-dataframe
geometry = Health_Facility.set_geometry('geometry')

#we'll check whether all facilities are located in a certain region
table_inpolygon = pd.DataFrame({'Polygons':[],'Points':[],'Results':[]}) #new dataframe with 3 columns
for i in range(len(total_data)):
    for j in range(len(Health_Facility)):
        b = (Health_Facility.iloc[j].geometry.within(total_data.iloc[i].geometry))
        row_dict = {'Polygons':[i],'Points':[j],'Results':[b]}
        row_df = pd.DataFrame(data=row_dict)
        table_inpolygon = pd.concat([table_inpolygon,row_df], ignore_index=True)
        
#we subset the data with only rows that contain a matching facility with the region in which that facility is located
all_points_in_polygons = table_inpolygon.loc[table_inpolygon['Results'] == 1]
#all_points_in_polygons.head(10)

total_rows = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == 2])
#print(total_rows)

#for each region, we'll check how many facilities there are in that region
Health_Facility_per_region = pd.DataFrame({'Polygon':[],'Facilities':[]}) #new dataframe with 2 columns
for l in range(1,33):
    a = len(all_points_in_polygons.loc[table_inpolygon['Polygons'] == l]) 
    row_dict = {'Polygon':[l],'Facilities':[a]}
    row_df = pd.DataFrame(data=row_dict)
    Health_Facility_per_region = pd.concat([Health_Facility_per_region,row_df], ignore_index=True)

#add new data as column to total_data dataframe
total_data['Health_Facility_per_region'] = learning_centers_per_region['Facilities']
total_data['Health_Facility_per_region'] = total_data['Health_Facility_per_region'].replace({0:np.nan})
total_data['Health_Facility_per_region'].fillna(0, inplace=True)
total_data['persons_per_Health_Facility_per_region'] = total_data['Curr_Total_Pop']/total_data['Health_Facility_per_region']
total_data['persons_per_Health_Facility_per_region'] = total_data['persons_per_Health_Facility_per_region'].replace({np.inf:np.nan})
total_data['persons_per_Health_Facility_per_region'].fillna(0, inplace=True)

#plot number of facilities per region (the darker the more)
#total_data.plot(column='nutrition_centers_per_region', cmap='OrRd', scheme='quantiles')#pr, scheme='fisher_jenks')

#plot density per campsite
DensHF = folium.FeatureGroup(name='Density Health_Facility')

folium.GeoJson(total_data,
    style_function=lambda feature: {
        'fillColor': 
        'green' if ((feature['properties']['persons_per_Health_Facility_per_region']) >= 0) & ((feature['properties']['persons_per_Health_Facility_per_region']) < (total_data['persons_per_Health_Facility_per_region'].quantile(q=0.25)))
                      else 'yellow' if ((feature['properties']['persons_per_Health_Facility_per_region']) >= (total_data['persons_per_Health_Facility_per_region'].quantile(q=0.25))) & ((feature['properties']['persons_per_Health_Facility_per_region']) < (total_data['persons_per_Health_Facility_per_region'].quantile(q=0.5)))
                      else 'darkorange' if ((feature['properties']['persons_per_Health_Facility_per_region']) >= (total_data['persons_per_Health_Facility_per_region'].quantile(q=0.5))) & ((feature['properties']['persons_per_Health_Facility_per_region']) < (total_data['persons_per_Health_Facility_per_region'].quantile(q=0.75)))
                      else 'red',
        'color': 'black',
        'weight': 0.0,
        'dashArray': '1, 1'
    }).add_to(DensHF)
    
#add campsites to map
sites = folium.FeatureGroup(name='Camp Sites')

for lat,lon,name in zip(total_data['Latitude'],total_data['Longitude'],total_data['New_Camp_Name_left']):
    folium.Marker(location=[lat,lon],popup=(folium.Popup(name)),icon=folium.Icon(color='orange',icon_color='white')).add_to(sites)

folium.GeoJson(total_data,
               name='Camp Sites',
    style_function=lambda feature: {
        'fillColor': 'lightgrey',
        'opacity': 0.5,
        'color': 'black',
        'weight': 0.5,
        'dashArray': '2, 2'
   }).add_to(sites)

#initiate map
map=folium.Map(location=[total_data['Latitude'].mean(),total_data['Longitude'].mean()],zoom_start=12)

'''choose which additional layers to add to the map'''
sites.add_to(map)
#LC.add_to(map)
#CIC.add_to(map)
#LearnC.add_to(map)
#WomenFS.add_to(map)
#ChildFS.add_to(map)
#WASHI.add_to(map)
#MosqueI.add_to(map)
#NC.add_to(map)    
#HF.add_to(map)

#HMLC.add_to(map)
#HMCIC.add_to(map) 
#HMLearnC.add_to(map)
#HMWomenFS.add_to(map)
#HMChildFS.add_to(map)
#HMWASHI.add_to(map)
#HMMosqueI.add_to(map)
#HMNC.add_to(map)  
#HMHF.add_to(map) 

#DistWASHI.add_to(map) 
#DistNC.add_to(map)  

DensPop.add_to(map)
#DensLC.add_to(map)
#DensWFS.add_to(map)
#DensCFS.add_to(map)
#DensWASH.add_to(map)
#DensNC.add_to(map)
#DensHF.add_to(map)

LayerControl().add_to(map)
map.save(outfile='all_sites.html')