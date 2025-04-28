#!/usr/bin/python3
'''

Aggregate Trees




'''


import os
import sys
import json
import glob
import pdal
import argparse
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from rasterstats import zonal_stats

from osgeo import gdal
os.environ['PROJ_LIB'] = '/opt/conda/share/proj'


def saveAggregateCSV(tree_polys_gdf, output_name, drop=True):
    if drop:
        tree_polys_gdfd = dropAttributes(tree_polys_gdf)
    else:
        tree_polys_gdfd = tree_polys_gdf

    tree_polys_gdfd.to_csv(output_name)

    print(f'Saved to file : {output_name}')



def dropAttributes(tree_polys_gdf, drop_list="default"):

    if drop_list == "default":
        drop_list = ['Intensity','ReturnNumber', 'NumberOfReturns', 'ScanDirectionFlag', 'EdgeOfFlightLine', 'Classification', 'ScanAngleRank', 'UserData', 'PointSourceId', 'GpsTime', 'ScanChannel', 'ClassFlags','OptimalKNN', 'OptimalRadius','Buffer']

        #drop_list = ['Intensity','ReturnNumber', 'NumberOfReturns', 'ScanDirectionFlag', 'EdgeOfFlightLine', 'Classification', 'ScanAngleRank', 'UserData', 'PointSourceId', 'GpsTime', 'ScanChannel', 'ClassFlags', 'Red', 'Green', 'Blue', 'Infrared','OptimalKNN', 'OptimalRadius','Buffer']

    tree_polys_gdfd = tree_polys_gdf.drop(columns=drop_list)

    return tree_polys_gdfd


def plotAttributes(tree_polys_fn, output_filename, sample_trees=None, attributes="default", zlims=None, format='png'):

    if attributes == "default":
        plot_columns = [ 'LAI' , 'HeightAboveGround' , 'DemantkeVerticality']
        zlims = [(0,10) , (0,15) , (0,.7) ]

    z=0
    for pc in plot_columns:
        print(f'Working on column {pc}')
        i=0
        f, ax = plt.subplots(nrows=1,ncols=7,figsize=(20,12),dpi=138)

        vmin = zlims[z][0]
        vmax = zlims[z][1]

        print(f'Plotting:')
        print(f'     --> using zlims {vmin} - {vmax}')

        # Tree Polygons
        tree_polys_new = gpd.read_file(tree_polys_fn)
        column = tree_polys_new[pc].astype('float32')

        # Create Plot
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("bottom", size="5%", pad=0.2)
        tree_polys_new.plot(column=column,ax=ax[i], cax=cax, cmap='turbo', vmin=vmin, vmax=vmax, legend=True, legend_kwds={'orientation': "horizontal"})

        if sample_trees:
            sample_trees.plot(ax=ax[i], facecolor="none", edgecolor='black',lw=1.8, alpha=.65)
            ax[i].set_axis_off()
            ax[i].set_title(f'{pc}')

        output_file = f'{output_filename.split(format)[0]}_{pc}_{output_filename.split(format)[1]}'
        f.savefig( output_file, format=format)
        plt.show()
        z+=1

def aggregateTrees(input_polys, out_polys, lai_file, stats_json, csv_file, agg_csv):

    # LiDAR summaries
    csv = pd.read_csv(csv_file)

    # Tree polys
    tree_polys = gpd.read_file(input_polys)

    # Zonal Stats
    rs = zonal_stats(input_polys, lai_file,stats="count min mean max median",nodata=-9999,geojson_out=True,categorical=True)

    # GeoJSON
    with open(stats_json, "w") as outjson:
        json.dump(rs, outjson,indent=4,skipkeys=True, ensure_ascii = False)

    # Create dataframe
    lai_gdf = gpd.GeoDataFrame(columns=['LAI'],index=tree_polys.TreeSN.sort_values(),dtype='float32')
    csvm = csv.groupby('TreeSN').mean()

    # Add mean to dataframe
    for ii in range(len(rs)):
        lai_gdf.loc[rs[ii]['properties']['TreeSN']].LAI = rs[ii]['properties']['mean']
        #lai_gdf.loc[rs[ii]['properties']['TreeSN']].LAI_md = rs[ii]['properties']['median']

    # Drop by index
    #new_csv = csvm.drop(index=[0, 9999]).join(lai_gdf)
    new_csv = csvm[1:3000].join(lai_gdf)

    tree_polys_sort = tree_polys.sort_values('TreeSN')
    tree_polys_sort = tree_polys_sort.set_index('TreeSN')

    tree_polys_new = tree_polys_sort.join(new_csv)

    tree_polys_new.to_file(out_polys, driver='GeoJSON')

    saveAggregateCSV(tree_polys_new, agg_csv, drop=True)


if __name__ == "__main__":

    '''
    Variables to edit for input
    ToDo - make this a JSON

    '''
    parser = argparse.ArgumentParser(description = "Merge tiles into COPC laz")
    parser.add_argument("-i", "--input-polys", help="Input tree polygons")
    parser.add_argument("-o", "--out-polys", help="Output polygons with raster stats")
    parser.add_argument("-l", "--lai-file", help="Input path and filename of LAI layer")
    parser.add_argument("-s", "--stats-json", help="Output Raster Stats JSON filename + path")
    parser.add_argument("-c", "--csv-file", help="Input CSV filename + path of all LAS points & fields")
    parser.add_argument("-g", "--agg-csv", help="Output CSV filename + path with aggregated values")
    parser.add_argument("-a", "--attr-list", help="List of attributes to plot", default="default")
    parser.add_argument("-p", "--attr-plotname", help="Output filename + path for figures")
    parser.add_argument("-m", "--method", help="Aggregation method", default="mean")

    #read arguments from the command line
    args = parser.parse_args()

    input_polys     = args.input_polys
    out_polys       = args.out_polys
    lai_file        = args.lai_file
    stats_json      = args.stats_json
    csv_file        = args.csv_file
    agg_csv         = args.agg_csv
    method          = args.method
    output_filename = args.attr_plotname

    print("1 - Aggregating Trees\n\n")
    aggregateTrees(input_polys, out_polys, lai_file, stats_json, csv_file, agg_csv)


    print("2- Plotting Attributes\n")
    plotAttributes(out_polys, output_filename, sample_trees=None, attributes="default", zlims=None, format='png')

    print(f'Script finished. \nTrees aggregated and saved : {agg_csv}')


