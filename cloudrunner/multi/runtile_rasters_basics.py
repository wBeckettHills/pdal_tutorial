
import os
import pdal
import geopandas as gpd

import warnings
warnings.filterwarnings('ignore')

os.environ['PROJ_LIB'] = '/opt/conda/share/proj'

from multiprocessing import Pool


def runtile_rasters_basics(lasfile):

    # CONSTANTS
    #base_wd  = '/media/beckett/beluga/projects/arb-tools_local/data'
    #basename = 'UW-ARBORETUM_20240517_Longenecker_lidar'
    #lidar_dir = f'{base_wd}/lidar'


    # FILENAMES
    print(f"LAS file {lasfile} \n")
    lidar_dirname = os.path.dirname(os.path.dirname(lasfile))
    output_path = f"{lidar_dirname}/tiles_raster"

    if not os.path.exists(output_path):
        print(f"Doesn't exist ! {output_path} \n") 
        #os.mkdir(output_path)
    else:
        print(f"{output_path} already exists \n")

    name = os.path.basename(lasfile)
    
    if name.endswith(".copc.laz"):
        lidar_basename = name.split('.copc.laz')[0]
    else:
        lidar_basename = name.split('.las')[0]
    
    raster_output  = f"{output_path}/{lidar_basename}"
      
    print(lasfile)
    print(raster_output)
    
    # PIPELINE
    
    pipeline = pdal.Pipeline()

    reader = pdal.Reader.las(lasfile)
    

    # RASTERS

    out_crs="EPSG:32616"
    gdaldriver="ENVI"

    #----------------
    # Zmax raster
    dimension="Z"
    dim="z"
    
    rtype="max"
    resolution=.2
    units="m"
    res="20cm"
    radius=1
    window_size=10

    rasters = []
    
    ras_name = f"{raster_output}_{dim}_{rtype}_{res}"
    rasters.append(ras_name)
    
    zmax          = pdal.Writer.gdal(ras_name,
                         resolution=resolution,
                         radius=radius,
                         dimension=dimension,
                         data_type="float32",
                         gdaldriver=gdaldriver,
                         gdalopts="resampling_method=cubic",
                         output_type=rtype,
                         override_srs=out_crs,
                         window_size=window_size,
                         nodata=-9999)

    #----------------
    # CHM raster
    dimension="Z"
    dim="chm"
    rtype="idw"
    resolution=.2
    units="m"
    res="20cm"
    power=1.5
    radius=3
    window_size=9


    ras_name = f"{raster_output}_{dim}_{rtype}_{res}"
    rasters.append(ras_name)
    
    z             = pdal.Writer.gdal(ras_name,
                         resolution=resolution,
                         dimension=dimension,
                         data_type="float32",
                         gdaldriver=gdaldriver,
                         override_srs=out_crs,
                         gdalopts="resampling_method=cubic",
                         output_type=rtype,
                         radius=radius,
                         power=power,
                         window_size=window_size,
                         nodata=-9999)


    #----------------
    # DSM raster
    dimension="Z_UTM"
    dim="dsm"
    rtype="idw"
    resolution=.2
    units="m"
    res="20cm"
    power=1.5
    radius=3
    window_size=9


    ras_name = f"{raster_output}_{dim}_{rtype}_{res}"
    rasters.append(ras_name)
    
    dsm             = pdal.Writer.gdal(ras_name,
                         resolution=resolution,
                         dimension=dimension,
                         data_type="float32",
                         gdaldriver=gdaldriver,
                         override_srs=out_crs,
                         output_type=rtype,
                         gdalopts="resampling_method=cubic",
                         radius=radius,
                         power=power,
                         window_size=window_size,
                         nodata=-9999)

    
    #----------------
    # Density raster
    dimension="Z"
    dim="density"
    
    rtype="count"
    resolution=1
    units="m"
    res="1m"
    radius=1
    window_size=1

    rasters = []
    
    ras_name = f"{raster_output}_{dim}_{rtype}_{res}"
    rasters.append(ras_name)
    
    density          = pdal.Writer.gdal(ras_name,
                         resolution=resolution,
                         radius=radius,
                         dimension=dimension,
                         data_type="float32",
                         gdaldriver=gdaldriver,
                         output_type=rtype,
                         override_srs=out_crs,
                         window_size=window_size,
                         nodata=-9999)



    #--------------------
    # DTM raster

    
    # FILTER
    #-----------
    # first to use only ground points
    filt = pdal.Filter.range(limits="Classification[2:2]")

    dimension="Z_UTM"
    dim="dtm"
    rtype="mean"
    resolution=1.
    units="m"
    res="1m"
    power=2
    radius=8
    window_size=15


    ras_name = f"{raster_output}_{dim}_{rtype}_{res}"
    rasters.append(ras_name)

    
    dtm          = pdal.Writer.gdal(ras_name,
                         resolution=resolution,
                         binmode=True,
                         radius=radius,
                         dimension=dimension,
                         data_type="float32",
                         gdaldriver=gdaldriver,
                         gdalopts="resampling_method=cubic",
                         output_type=rtype,
                         override_srs=out_crs,
                         window_size=window_size,
                         nodata=-9999)


    
    # add to Pipeline
    pipeline |= reader | zmax | z | dsm | density | filt | dtm

    # Run the pipeline
    pipeline.execute()
    
    print(f"Pipeline finished : {lidar_basename}")
    
    #return outname


if __name__ == '__main__':
    runtile_rasters_basics()