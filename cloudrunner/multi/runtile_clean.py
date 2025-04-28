import os
import pdal
import geopandas as gpd

import warnings

warnings.filterwarnings("ignore")

os.environ["PROJ_LIB"] = "/opt/conda/share/proj"

from multiprocessing import Pool


def runtile_clean(lasfile):
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
    output_path = f"{lidar_dirname}/tiles_clean"

    if not os.path.exists(output_path):
        print(f"Doesn't exits ! {output_path} \n")
        # os.mkdir(output_path)
    else:
        print(f"{output_path} already exists \n")

    lidar_basename = os.path.basename(lasfile).split(".laz")[0]
    lidar_output = f"{output_path}/{lidar_basename}"

    pipeline = pdal.Reader.las(lasfile).pipeline()

    pipeline.execute()

    # MAX MIN VALUES FOR CROP

    zmin, zmax = 160, 370

    buffer_size = 10.0
    tile_size = 60.0

    arr = pipeline.arrays[0].copy()
    bxmin = arr["X"].min()
    bymax = arr["Y"].max()
    txmin = arr["X"].min() + buffer_size
    tymax = arr["Y"].max() - buffer_size

    print("Values:\n")
    print("=" * 50)
    print(f"Z elev min/max : {zmin} {zmax} \n")
    print(f"Buffer Origin  : {bxmin} {bymax} \n")
    print(f"Tile   Origin  : {txmin} {tymax} \n")

    # Use the xy origin coords in the name
    outname = f"{lidar_output}_{int(txmin)}_{int(tymax)}_cln.laz"

    print(lasfile)
    print(outname)

    # OUTLIER IDENTIFICATION
    outlier = pdal.Filter.outlier(method="statistical", multiplier=3, mean_k=8)

    # OUTLIER REMOVAL
    rng = pdal.Filter.expression(
        expression=f"(Classification != 7) && (Z >= {zmin} && Z <= {zmax})"
    )

    # WRITE OUTPUT
    writer = pdal.Writer.las(outname, forward="all", extra_dims="all", minor_version=4)

    # add to Pipeline
    pipeline |= outlier | rng | writer

    # Run the pipeline
    pipeline.execute()

    print(f"Pipeline finished : {lidar_basename}")

    # return outname


if __name__ == "__main__":
    runtile_clean()
