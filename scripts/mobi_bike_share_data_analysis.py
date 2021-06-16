#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import json
from shapely.geometry import Point, Polygon


# In[34]:


street_map = gpd.read_file('zoning-districts-and-labels.shp')
parks_map = gpd.read_file('parks.shp')
shoreline_map = gpd.read_file('shoreline-2002.shp')

fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax=ax)


# In[35]:


df = pd.read_json('stations.json', orient='stations')
df = pd.json_normalize(data['stations'])
df


# In[105]:


# all stations
pd.set_option('display.max_rows', None)
geo_df['station_id']

#geo_df.count - 202


# In[37]:


# create coordinates from lat/lon
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
crs={'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
geo_df.head()


# In[109]:


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


# In[144]:


# thought I would need lat/lon for park locations to calculate distances
parks_df = pd.DataFrame(parks_map)
parks_df['lat'] = [point.y for point in parks_df['geometry']]
parks_df['lon'] = [point.x for point in parks_df['geometry']]
parks_df


# In[170]:


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


# In[104]:


# plot stations on shoreline map
fig, ax = plt.subplots(figsize = (15,15))
shoreline_map.plot(ax=ax)
geo_df.plot(ax=ax, markersize=20, color='blue', marker='o', label = 'Station')


# In[171]:


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


# In[81]:


top_5_departure = geo_df[geo_df["station_id"].isin(['0209', '0105', '0102', '0066', '0036'])]
top_5_departure.head()


# In[82]:


top_5_return = geo_df[geo_df["station_id"].isin(['0209', '0028', '0102', '0066', '0083'])]
top_5_return.head()


# In[78]:


bottom_5_return = geo_df[geo_df["station_id"].isin(['0129', '0221', '0165', '0227', '0066'])]
bottom_5_return.head()

bottom_5_departure = geo_df[geo_df["station_id"].isin(['0221', '0066', '0129', '0165', '0052'])]
bottom_5_departure.head()


# In[116]:


fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax)
top_5_return.plot(ax=ax, markersize=20, color='black', marker='o', label = 'Most Popular')
top_5_departure.plot(ax=ax, markersize=20, color='black', marker='o')
bottom_5_return.plot(ax=ax, markersize=20, color='red', marker='o', label = 'Least Popular')
bottom_5_departure.plot(ax=ax, markersize=20, color='red', marker='o')
ax.legend()


# In[ ]:




