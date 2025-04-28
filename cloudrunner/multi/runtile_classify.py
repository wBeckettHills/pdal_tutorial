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

    buffer_size = 10.0
    tile_size = 60.0

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

    lidar_basename = os.path.basename(lasfile).split(".laz")[0]
    lidar_output = f"{output_path}/{lidar_basename}"
    copc_output = f"{copc_path}/{lidar_basename}"

    pipeline = pdal.Reader.las(lasfile).pipeline()

    pipeline.execute()

    # MAX MIN VALUES FOR CROP

    zmin, zmax = 0.0, 50.0

    buffer_size = 10.0
    tile_size = 60.0

    arr = pipeline.arrays[0].copy()
    bxmin = arr["X"].min()
    bymax = arr["Y"].max()
    txmin = arr["X"].min() + buffer_size
    tymax = arr["Y"].max() - buffer_size

    print("Values used for cropping:\n")
    print("=" * 50)
    print(f"Z elev min/max : {zmin} {zmax} \n")
    print(f"Buffer Origin  : {bxmin} {bymax} \n")
    print(f"Tile   Origin  : {txmin} {tymax} \n")

    # Use the xy origin coords in the name
    copcname = f"{copc_output}_grnd_hag.copc.laz"
    outname = f"{lidar_output}_grnd_hag.laz"

    print(lasfile)
    print(copcname)

    # GROUND CLASSIFICATION
    ground = pdal.Filter.csf(resolution=0.5)

    # HAG --> Height Above Ground
    hag = pdal.Filter.hag_delaunay(count=25)

    # ALTER Z values to HeightAboveGround
    changeZ = pdal.Filter.ferry(dimensions="Z => Z_UTM, HeightAboveGround => Z")

    # CROP BUFFER to TILE
    crop = pdal.Filter.crop(
        bounds=f"([{txmin},{txmin + tile_size}],[{tymax - tile_size},{tymax}],[{zmin},{zmax}])"
    )

    # Filter negatives to zero
    zero = pdal.Filter.assign(value="Z = 0. WHERE Z < 0.")

    # WRITE OUTPUT
    copc = pdal.Writer.copc(copcname, forward="all", extra_dims="all", threads=1)
    writer = pdal.Writer.las(outname, forward="all", extra_dims="all", minor_version=4)

    # add to Pipeline
    # NOTE : writer includes buffer, copc has it removed
    pipeline |= ground | hag | changeZ | zero | writer | crop | copc

    # Run the pipeline
    pipeline.execute()

    print(f"Pipeline finished : {lidar_basename}")

    # return outname


if __name__ == "__main__":
    runtile_classify()
