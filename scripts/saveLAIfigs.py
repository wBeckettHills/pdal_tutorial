#!/usr/bin/python3
'''

Save LAI figs

python saveLAIfigs.py -i ${input_lai} -o ${output_name} -f 'png' -x 15 -n 0

    "-i", "--input-lai", help="Path and filename of LAI"
    "-t", "--title", help="Title of the figure"
    "-o", "--output-name", help="Output path and filename of figure"
    "-f", "--format", help="Graphics format", default='png'
    "-x", "--vmax", help="Plot vertical max", default='15'
    "-n", "--vmin", help="Plot vertical min", default='0'


'''

import os
import sys
import json
import glob
import pdal
import argparse

import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from osgeo import gdal
os.environ['PROJ_LIB'] = '/opt/conda/share/proj'


def saveLAIfigs(input_lai, title, output_name,format='png',vmin=0,vmax=15):

    dslai = gdal.Open(input_lai)
    geo = dslai.GetGeoTransform()
    nodata = dslai.GetRasterBand(1).GetNoDataValue()
    lai = dslai.ReadAsArray()
    dslai = None

    # mask nodata
    #lai = np.ma.masked_values(lai, nodata)

    # calculate extent
    ys, xs = lai.shape
    ulx, xres, _, uly, _, yres = geo
    extent = [ulx, ulx+xres*xs, uly, uly+yres*ys]

    # plot
    fig, ax = plt.subplots(figsize=(5,6), constrained_layout=True, facecolor='w', dpi=86)
    plt.title(title)
    ax.set_axis_off()
    cmap = mpl.colormaps.get_cmap("turbo").copy() # cmap = plt.cm.viridis
    cmap.set_bad('#dddddd')

    im = ax.imshow(lai, extent=extent, cmap=cmap, vmin=vmin, vmax=vmax)
    cb = fig.colorbar(im, shrink=.5)
    cb.set_label('LAI')
    fig.savefig( output_name, format=format)


if __name__ == "__main__":

    '''
    Variables to edit for input
    ToDo - make this a JSON

    '''
    parser = argparse.ArgumentParser(description = "Merge tiles into COPC laz")
    parser.add_argument("-i", "--input-lai", help="Path and filename of LAI")
    parser.add_argument("-t", "--title", help="Title of the figure")
    parser.add_argument("-o", "--output-name", help="Output path and filename of figure")
    parser.add_argument("-f", "--format", help="Graphics format", default='png')
    parser.add_argument("-x", "--vmax", help="Plot vertical max", default='15')
    parser.add_argument("-n", "--vmin", help="Plot vertical min", default='0')

    #read arguments from the command line
    args = parser.parse_args()

    input_lai       = args.input_lai
    title           = args.title
    output_name     = args.output_name
    format          = args.format
    vmax            = args.vmax
    vmin            = args.vmin

    saveLAIfigs(input_lai, title, output_name,format='png',vmin=0,vmax=15)

    print(f'Plot saved : {output_name}')
