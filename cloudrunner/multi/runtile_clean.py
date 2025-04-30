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

    # FILENAMES
    print(f"LAS file {lasfile} \n")
    lidar_dirname = os.path.dirname(os.path.dirname(lasfile))
    output_path = f"{lidar_dirname}/tiles_clean"

    if not os.path.exists(output_path):
        print(f"Doesn't exits ! {output_path} \n")
        # os.mkdir(output_path)
    else:
        print(f"{output_path} already exists \n")

    lidar_basename = os.path.basename(lasfile).split(".las")[0]
    lidar_output = f"{output_path}/{lidar_basename}"

    pipeline = pdal.Pipeline()

    reader = pdal.Reader.las(lasfile)

    # Use the xy origin coords in the name
    outname = f"{lidar_output}_cln.las"

    print(f"LAS output {outname} \n")

    # OUTLIER IDENTIFICATION
    outlier = pdal.Filter.outlier(method="statistical", multiplier=2.2, mean_k=8)

    # OUTLIER REMOVAL
    rng = pdal.Filter.expression(
        expression=f"(Classification != 7)"
    )

    # WRITE OUTPUT
    writer = pdal.Writer.las(outname, forward="all", extra_dims="all", minor_version=4)

    # add to Pipeline
    pipeline |= reader | outlier | rng | writer

    # Run the pipeline
    pipeline.execute()

    print(f"Pipeline finished : {lidar_basename}")

    # return outname


if __name__ == "__main__":
    runtile_clean()
