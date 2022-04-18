#!/usr/bin/env python
# coding: utf-8

# # Mapping School Locations Script

# ## Import Packages

# In[1]:


import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy.ia import *
import arcgis
from arcgis.gis import GIS
gis = GIS("home")
from arcgis.features import SpatialDataFrame
spatial = SpatialDataFrame


# In[2]:


# Set Data Directories
data_dir = "G:/Work/SDSN/Data/SDG 4"
iiep_worldpop_dir = "G:/Work/SDSN/Data/SDG 4/IIEP_WorldPop/school_age_population"
# Set Output Locations
output_dir = "G:/Work/SDSN/Data/SDG 4/School Locations Temp"


# # Input Data

# ## IIEP/WorldPop School Aged Population Data

# In[3]:


# Set Directory for School Aged Population Folder
arcpy.env.workspace = iiep_worldpop_dir
arcpy.env.workspace


# In[4]:


# Create a list of Country Codes as Identified by the country-specific subfolders within the population data folder
country_list = ["AGO","BDI","BEN","BFA","BWA","CAF","CIV","CMR","COD","COG","COM","CPV","DJI","DZA","EGY","ERI","ES_CN","ESP","ETH","GAB","GHA","GIN","GMB","GNB","GNQ","KEN","LBR","LBY","LSO","MAR","MDG","MLI","MOZ","MRT","MUS","MWI","MYT","NAM","NER","NGA","PRT","PT_30","REU","RWA","SDN","SEN","SLE","SOM","SSD","STP","SWZ","SYC","TCD","TGO","TUN","TZA","UGA","YEM","ZAF","ZMB","ZWE"]


# ### Parse through country subfolders for sex specific datasets to merge into continent-wide images, both primary and secondary aged students. Result: 6 datasets, 3 per student age group

# In[5]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_F_M_PRIMARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_1 = raster
    else:
        af_1 = Merge([af_1,raster])
af_1


# In[6]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_M_PRIMARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_1_m = raster
    else:
        af_1_m = Merge([af_1_m,raster])
af_1_m


# In[7]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_F_PRIMARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_1_f = raster
    else:
        af_1_f = Merge([af_1_f,raster])
af_1_f


# In[8]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_F_M_SECONDARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_2 = raster
    else:
        af_2 = Merge([af_2,raster])
af_2


# In[9]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_M_SECONDARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_2_m = raster
    else:
        af_2_m = Merge([af_2_m,raster])
af_2_m


# In[10]:


blank = []
previous = []
for country in country_list:
    ## Create File Name for Iteration
    cc = country
    file = "_F_SECONDARY_2020_1km.tif"
    slash ="/"
    image = cc+slash+cc+file
    raster = Raster(image)
    ## Merge File into Raster, conditional
    if previous == blank:
        previous = country
        af_2_f = raster
    else:
        af_2_f = Merge([af_2_f,raster])
af_2_f


# ## Walking-time Cost Raster

# In[11]:


# Set Directory for walking time folder
arcpy.env.workspace = data_dir
arcpy.env.workspace


# In[12]:


walk_af = Raster("walking_time_2019_af.tif")
walk_af


# ## OSM School Locations

# In[13]:


# Item Added From Toolbar
# Title: OpenStreetMap Buildings for Africa | Type: Feature Service | Owner: smoore2_osm
item = gis.content.get("bb86721588ea49b6b44b10b7d5d2b0b1")
feature_layer=item.layers[0]
feature_layer


# In[14]:


# query for only buildings listed as schools
query_statement="building='school'"
schools=feature_layer.query(where=query_statement)
schools


# In[15]:


# Convert to Spatial Data Frame for conversion to ArcPy Layer Object
schools_sdf = schools.sdf
schools_sdf


# In[16]:


# Select only columns we need for distance accumulation
columns = ['objectid', 'osm_id2', 'SHAPE']
# Save as shp file
output_schools_shp = output_dir + "/school_locations.shp"
schools_sdf[columns].spatial.to_featureclass(output_schools_shp, overwrite = True)
# Import shp as ArcPy Layer object
schools_loc = arcpy.MakeFeatureLayer_management("School Locations Temp/school_locations.shp")
schools_loc


# # Create Isochrone Raster from School Locations and Cost Raster

# ## Distance Accumulation

# In[17]:


# Run Distance Accumulation tool, select GEODESIC due to the large geographic extent of our data
outDistAcc = DistanceAccumulation(
    in_source_data = schools_loc,
    in_cost_raster = walk_af,
    distance_method = "GEODESIC")
outDistAcc


# ## Create Isochrone Rasters

# In[ ]:




