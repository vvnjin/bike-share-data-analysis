#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import json
from shapely.geometry import Point, Polygon


# In[3]:


# load in .shp files 
street_map = gpd.read_file('zoning-districts-and-labels.shp')
parks_map = gpd.read_file('parks.shp')
shoreline_map = gpd.read_file('shoreline-2002.shp')

# test out a plot
fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax=ax)


# In[5]:


# read json data into a pandas DataFrame
df = pd.read_json('stations.json', orient='stations')
df = pd.json_normalize(df['stations'])
df


# In[7]:


# all stations
pd.set_option('display.max_rows', None)
df['station_id']


# In[11]:


# store total count in variable
total_num_stations = df.count()
total_num_stations


# In[12]:


# create coordinates from lat/lon
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
crs={'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
geo_df.head()


# In[13]:


# plot all stations on map
fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax)
geo_df.plot(ax=ax, markersize=20, color='white', marker='o', label = 'Point')


# In[108]:


# plot stations and parks on map

fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax=ax)
geo_df.plot(ax=ax, markersize=20, color='black', marker='o', label = 'Station')
parks_map.plot(ax=ax, markersize=20, color='red', marker='o', label = 'Park')
ax.legend()


# In[18]:


# thought I would need lat/lon for park locations to calculate distances
parks_df = pd.DataFrame(parks_map)
parks_df['lat'] = [point.y for point in parks_df['geometry']]
parks_df['lon'] = [point.x for point in parks_df['geometry']]


# In[20]:


# stations that are within 200m of a park

count = 0
geo_df.to_crs(epsg=3310,inplace=True)
parks_map.to_crs(epsg=3310,inplace=True)
for index, row in geo_df.iterrows():
    for index2, row2 in parks_map.iterrows():
        dist = row2['geometry'].distance(row['geometry'])
        if dist < 200:
            count += 1
count


# In[22]:


# % of stations that are within 200m of a park
count/total_num_stations * 100


# In[24]:


# plot stations on shoreline map
fig, ax = plt.subplots(figsize = (15,15))
crs={'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
shoreline_map.plot(ax=ax)
geo_df.plot(ax=ax, markersize=20, color='blue', marker='o', label = 'Station')


# In[25]:


# stations that are within 200m of the shoreline
count = 0
geo_df.to_crs(epsg=3310,inplace=True)
shoreline_map.to_crs(epsg=3310,inplace=True)
for index, row in geo_df.iterrows():
    for index2, row2 in shoreline_map.iterrows():
        dist = row2['geometry'].distance(row['geometry'])
        if dist < 200:
            count += 1
count


# In[26]:


# % of stations that are within 200m of the shoreline
count/total_num_stations * 100


# In[27]:


# manually filter for top 5 departure stations (found by SQL querying)
crs={'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
top_5_departure = geo_df[geo_df["station_id"].isin(['0209', '0105', '0102', '0066', '0036'])]
top_5_departure.head()


# In[28]:


# manually filter for top 5 return stations (found by SQL querying)
top_5_return = geo_df[geo_df["station_id"].isin(['0209', '0028', '0102', '0066', '0083'])]
top_5_return.head()


# In[29]:


# manually filter for bottom 5 return and departure stations (found by SQL querying)
bottom_5_return = geo_df[geo_df["station_id"].isin(['0129', '0221', '0165', '0227', '0066'])]
bottom_5_return.head()

bottom_5_departure = geo_df[geo_df["station_id"].isin(['0221', '0066', '0129', '0165', '0052'])]
bottom_5_departure.head()


# In[30]:


# plot all points (ended up with 6 for each category due to overlap between return and departure stations)
fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax)
top_5_return.plot(ax=ax, markersize=20, color='black', marker='o', label = 'Most Popular')
top_5_departure.plot(ax=ax, markersize=20, color='black', marker='o')
bottom_5_return.plot(ax=ax, markersize=20, color='red', marker='o', label = 'Least Popular')
bottom_5_departure.plot(ax=ax, markersize=20, color='red', marker='o')
ax.legend()


# In[ ]:




