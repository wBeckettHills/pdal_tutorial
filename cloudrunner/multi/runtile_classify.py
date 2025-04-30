import os
import pdal
import geopandas as gpd

import warnings

warnings.filterwarnings("ignore")

os.environ["PROJ_LIB"] = "/opt/conda/share/proj"

from multiprocessing import Pool


def runtile_classify(lasfile):
    # reset=False,denoise=True,extract=False):

    # CONSTANTS
    # base_wd  = '/media/beckett/beluga/projects/arb-tools_local/data'
    # basename = 'UW-ARBORETUM_20240517_Longenecker_lidar'
    # lidar_dir = f'{base_wd}/lidar'


    # FILENAMES
    print(f"LAS file {lasfile} \n")
    lidar_dirname = os.path.dirname(os.path.dirname(lasfile))
    output_path = f"{lidar_dirname}/tiles_class"
    copc_path = f"{lidar_dirname}/tiles_copc"

    # if not os.path.exists(output_path):
    #    print(f"Doesn't exits ! {output_path} \n")
    # os.mkdir(output_path)
    # else:
    #    print(f"{output_path} already exists \n")

    lidar_basename = os.path.basename(lasfile).split(".las")[0]
    lidar_output = f"{output_path}/{lidar_basename}"
    copc_output = f"{copc_path}/{lidar_basename}"

    tile_id      = os.path.basename(lasfile).split("_cln.las")[0].split("lidar_")[-1]
    tile_file    = f"{lidar_dirname}/tiles/AARS_DSMGrid_50m_utm16n_union_30m_{tile_id}.geojson"
    polygon      = gpd.read_file(tile_file)
    tile_polygon = polygon[polygon.loc[:,"Buffer"] == 0 ]
    tile_wkt     = tile_polygon.union_all().wkt

    # Use the xy origin coords in the name 
    copcname = f"{copc_output}_grnd_hag.copc.laz"
    outname = f"{lidar_output}_grnd_hag.las"

    print(f"Tile ID {tile_id} \n")
    print(f"LAS out {outname} \n")
    print(f"COPC out {copcname} \n")

    # PDAL Pipeline
    pipeline = pdal.Pipeline()

    reader = pdal.Reader.las(lasfile)

    # GROUND CLASSIFICATION
    ground = pdal.Filter.csf(resolution=0.5, returns = "first, last, intermediate, only")

    # HAG --> Height Above Ground
    hag = pdal.Filter.hag_delaunay(count=25)

    # ALTER Z values to HeightAboveGround
    changeZ = pdal.Filter.ferry(dimensions="Z => Z_UTM, HeightAboveGround => Z")

    # CROP BUFFER to TILE
    crop = pdal.Filter.crop(polygon=tile_wkt)
    #crop = pdal.Filter.crop(
    #    bounds=f"([{txmin},{txmin + tile_size}],[{tymax - tile_size},{tymax}],[{zmin},{zmax}])"
    #)

    # Filter negatives to zero
    zero = pdal.Filter.assign(value="Z = 0. WHERE Z < 0.")

    # WRITE OUTPUT
    copc = pdal.Writer.copc(copcname, forward="all", extra_dims="all", threads=1)
    writer = pdal.Writer.las(outname, forward="all", extra_dims="all", minor_version=4)

    # add to Pipeline
    # NOTE : writer includes buffer, copc has it removed
    pipeline |= reader | ground | hag | changeZ | zero | writer | crop | copc

    # Run the pipeline
    pipeline.execute()

    print(f"Pipeline finished : {lidar_basename}")

    # return outname


if __name__ == "__main__":
    runtile_classify()
