import os
import pdal
import geopandas as gpd

import warnings

warnings.filterwarnings("ignore")

os.environ["PROJ_LIB"] = "/opt/conda/share/proj"

from multiprocessing import Pool


def runtile_stats(lasfile):
    # reset=False,denoise=True,extract=False):

    # CONSTANTS

    # base_wd  = '/media/beckett/beluga/projects/arb-tools_local/data'
    # basename = 'UW-ARBORETUM_20240517_Longenecker_lidar'
    # lidar_dir = f'{base_wd}/lidar'

    buffer_size = 10.0
    tile_size = 60.0
    calc_covar = False

    # FILENAMES
    print(f"LAS file {lasfile} \n")
    lidar_dirname = os.path.dirname(os.path.dirname(lasfile))
    output_path = f"{lidar_dirname}/tiles_stats"
    copc_path = f"{lidar_dirname}/tiles_copc"

    if not os.path.exists(output_path):
        print(f"Making {output_path} \n")
        os.mkdir(output_path)
    else:
        print(f"{output_path} already exists \n")

    lidar_basename = os.path.basename(lasfile).split(".laz")[0]
    lidar_output = f"{output_path}/{lidar_basename}"
    copc_output = f"{copc_path}/{lidar_basename}"

    pipeline = pdal.Reader.las(lasfile).pipeline()

    pipeline.execute()

    # MAX MIN VALUES FOR CROP

    zmin, zmax = 0.0, 65.0

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
    copcname = f"{copc_output}_stats.copc.laz"
    outname = f"{lidar_output}_stats.laz"

    print(lasfile)
    print(outname)
    print(copcname)

    # STATS
    optKNN = pdal.Filter.optimalneighborhood(min_k=8, max_k=250)
    eigen = pdal.Filter.eigenvalues(knn=50, normalize=True)
    covar = pdal.Filter.covariancefeatures(
        knn=50, threads=1, optimized=True, feature_set="all", mode="Normalized"
    )
    normals = pdal.Filter.normal(knn=8, refine=True)
    radials = pdal.Filter.radialdensity(radius=0.5)  # 2

    # CROP BUFFER to TILE
    crop = pdal.Filter.crop(
        bounds=f"([{txmin},{txmin + tile_size}],[{tymax - tile_size},{tymax}],[{zmin},{zmax}])"
    )

    # WRITE OUTPUT
    copc = pdal.Writer.copc(copcname, forward="all", extra_dims="all", threads=1)
    writer = pdal.Writer.las(outname, forward="all", extra_dims="all", minor_version=4)

    # add to Pipeline
    # write is before crop to keep buffer on laz tile output for covar calculation
    pipeline |= optKNN | eigen | normals | radials | writer | crop | copc

    # Run the pipeline
    pipeline.execute()

    print(
        f"Pipeline |= optKNN | eigen | normals | radials | writer | crop | copc  \n  Finished : {lidar_basename}"
    )

    if calc_covar == True:
        # Covariance Features
        # -----------------------
        # "Anisotropy,Density,DemantkeVerticality,Eigenentropy,Omnivariance,EigenvalueSum"
        # "Linearity,Planarity,Scattering,SurfaceVariation,Verticality"
        # -------------------------------------------------------------------- #
        print(f"Calculating Covariance Features = {calc_covar}")
        covar_copcname = f"{copcname.split('.copc.laz')[0]}_covar.copc.laz"
        covar_outname = f"{outname.split('.laz')[0]}_covar.laz"

        print(covar_copcname)
        print(covar_outname)

        # Create a reader for the file
        covar_reader = pdal.Reader.las(outname).pipeline()

        # Calculate Covariance Features
        covar = pdal.Filter.covariancefeatures(
            knn=8, threads=1, optimized=True, feature_set="DemantkeVerticality"
        )

        # CROP BUFFER to TILE
        covar_crop = pdal.Filter.crop(
            bounds=f"([{txmin},{txmin + tile_size}],[{tymax - tile_size},{tymax}],[{zmin},{zmax}])"
        )

        # WRITE OUTPUT
        covar_copc = pdal.Writer.copc(
            covar_copcname, forward="all", extra_dims="all", threads=1
        )
        covar_writer = pdal.Writer.las(
            covar_outname, forward="all", extra_dims="all", minor_version=4
        )

        # Build the pipeline
        # write is before crop to keep buffer on laz tile output for later calculation
        covar_pipeline = covar_reader | covar | covar_writer | covar_crop | covar_copc

        # Run the pipeline
        covar_pipeline.execute()

        print(
            f"covar_pipeline = covar_reader | covar | covar_writer | covar_crop | covar_copc  \n  Finished : {lidar_basename}"
        )

        # Consider removing the outname file

    # return outname


if __name__ == "__main__":
    runtile_stats()
