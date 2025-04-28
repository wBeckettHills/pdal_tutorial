# -*- coding: utf-8 -*-
'''
Created on Thu Nov  4 17:23:39 2021

@author: whills
'''
import json

# Path & Name Variables
root_path   = f'/home'
config_dir  = f'{home}/configs'

# Create a config dictionary
config_dict = {}

# Project config
config_dict['project']                                          = 'aspens'
config_dict['date']                                             = '05112021'
config_dict['subset_name']                                      = "DefoliationDates"
config_dict['session_name']                                     = f'{config_dict['project']}_{config_dict['date']}'
config_dict['root_dir']                                          = '/home/'
config_dict['dem_name']                                         = None
config_dict['dsm_border']                                       = f'{config_dir}/AARS_DSMClip_utm16n.geojson'
config_dict['cutline_border']                                   = f'{config_dir}/AARS_BorderClip_utm16n.geojson'
config_dict['tree_points']                                      = f'{config_dir}/AARS_TreePoints_utm16n.geojson'
config_dict['tree_polys']                                       = f'{config_dir}/AARS_TreePolys_{date}_utm16n.geojson'
config_dict['tile_grid']                                        = f'{config_dir}/AARS_DSMGrid_50m_utm16n.geojson'


# LiDAR
config_dict['raw_lidar']                                        = {}
config_dict['raw_lidar']['las_dir']                             = '/staging/whills/data/raw/wisasp/raw_lidar'
config_dict['raw_lidar']['las_name']                            = f'{site}_{date}_lidar{sfx}.las'

config_dict['raw_lidar']['tiles']                               = {}
config_dict['raw_lidar']['tiles']['path']                       = []
config_dict['raw_lidar']['tiles']['names']                      = []

# Multispectral
config_dict['multispectral']                                    = {}
config_dict['multispectral']['point_cloud']                     = {}
config_dict['multispectral']['rgb_image']                       = {}
config_dict['multispectral']['spectral_bands']                  = {}

# AROSICS configs
config_dict['arosics']                                          = {}
config_dict['arosics']['run']                                   = True
config_dict['arosics']['st_indx']                               = '03'
config_dict['arosics']['pairs']                                 = [['3','2'],['2sh','1'],['3','4'],['4sh','5'],['5sh','6']]
config_dict['arosics']['uav_ortho']                             = ['HRS_20200807_K_Potatoes_multiband_hh_sr_c.tif']






## ENVIRONMENT
# Some need to become args

# COPIED FROM cloudrunner.py

date_run_name = "DefoliationDates" #"AllDates" "TrowbridgeSampleDates

project = 'raw'
date    = d
site    = 'aspens'

root    = '/home/jovyan'
wd      = f'{root}/data/{project}_lidar'

prefix  = f'{site}_{date}'

output_dir = f'{root}/output'
las_dir    = f'{wd}/{date}'
config_dir = f'{root}/data/configs'
tile_dir   = f'{las_dir}/tiles'
temp_dir   = f'{las_dir}/tmp'

las_name   = f'{prefix}_lidar_dt.las'
las_file   = f'{las_dir}/{las_name}'













# WORKED on below
```
# root =  ${PWD}

```


root = '/home/jovyan'
wd = f'{root}/data'
configs = f'{wd}/configs'
tables = f'{root}/output/tables'
graphics = f'{root}/output/graphics'

date_run_name = "DefoliationDates" #"AllDates" "TrowbridgeSampleDates

# las file -> read it for first stage
raw_las = f'/home/jovyan/data/raw_lidar/{d}/aspens_{d}_lidar.las'
las = laspy.read(raw_las)

# Tree Crown Points
tree_points_fn = f'{configs}/AARS_TreePoints_utm16n.geojson'
tree_polys_fn = f'{configs}/AARS_TreePolys_{d}_utm16n.geojson'

# Create a GeoPandas GeoDataFrame of the polygons
tree_polys = gpd.read_file(tree_polys_fn)


# Plotting constants for GPStime density histograms
sd_th = .60
bins = 100
idx_th=75

# Dates for the Project
config_dict['dates']          = ["05112021", "05172021", "05262021", "05292021", "06022021", "06052021", "06092021", "06112021", "06132021", "06162021", "07062021", "07102021", "08052021", "08222021", "09062021", "09292021"]
config_dict['sample_trees']   = [ 50, 51, 70, 136, 215, 327, 434, 592, 607, 650, 669, 724, 763, 781, 785, 928, 934, 987, 997, 1018, 1150, 1177, 1210, 1217, 1238, 1245, 1249, 1250, 1258, 1308, 1332, 1355, 1359, 1363, 1367, 1416, 1432, 1510, 1531, 1533, 1549]


## Dask Configurations
config_dict['dask']                                 = {}
config_dict['dask']["config"]                       = {}
config_dict['dask']["config"]["n_workers"]          = 14
config_dict['dask']["config"]["threads_per_worker"] = 1
config_dict['dask']["config"]["dashboard_address"]  = ":42002"
config_dict['dask']["config"]["memory_limit"]       = "22GiB"

# View Dask Configurations:
cfg.get("distributed.client")
cfg.get("distributed.scheduler.worker-ttl")
cfg.get("distributed.worker.lifetime.duration")
cfg.get("distributed.admin.tick.limit")

# Set Alternative Configurations:
cfg.set({"distributed.client.heartbeat" : "2800s"})
cfg.set({"distributed.scheduler.worker-ttl": "6000s"})
cfg.set({"distributed.worker.lifetime.duration":"6000"})
cfg.set({"distributed.admin.tick.limit": "60s"})




## Create Dask Cluster
cluster = LocalCluster(n_workers=14,threads_per_worker=1, dashboard_address=':42002', memory_limit="22GiB")
client = Client(cluster)
client
































config_file = root_path+r'\chtc_config_'+config_dict['project'] + '_' + config_dict['date']+'.json'

with open(config_file, 'w') as outfile:
    # Serializing json
    json.dump(config_dict,outfile,indent=4)
