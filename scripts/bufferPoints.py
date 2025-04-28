
'''

ROUGH draft of function from ipython notebook

'''



import os
import json
import pdal
import geopandas as gpd

def bufferPoints(point_file, bufferDist=1.25, geojson=True, gpd=True):

    # Buffer Tree Points to create tree crown polygons
    # and GeoPandasDataframe output object
    tree_points_fn = f'{configs}/AARS_TreePoints_utm16n.geojson'
    tree_polys_fn = f'{configs}/AARS_TreePolys_{d}_utm16n.geojson'

    tree_points = gpd.read_file(tree_points_fn)

    tree_polys = tree_points.copy()
    tree_polys.geometry = tree_polys['geometry'].buffer(bufferDist)

    tree_polys.to_file(tree_polys_fn)

    #tree_polys = gpd.read_file(tree_polys_fn)
