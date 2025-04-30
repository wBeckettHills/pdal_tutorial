# CloudRunner

<img src="https://github.com/wBeckettHills/pdal_tutorial/blob/development/graphics/CloudRunnner-oblique.png?raw=true" align='right' width=55%>

<br>

A toolkit of LIDAR processing pipelines and workflows using ```PDAL``` and ```GDAL``` for research applications, especially those interested in remote sensing of plants and trees. Primarily meant to provide an approach for customizable templates to achieve advanced outcomes with (often rather messy) raw point clouds.

<br>

*Future development efforts are focused on more efficient data handling, hyperspectral imagery integration, and the use of GPU hardware for calculations.*


## OVERVIEW

The ```cloudrunner``` toolset has a few **major** goals:

1. *REPEATABLE* --> Provide a general set of processing steps for LiDAR as a backbone for reproducible results.

1. *TEACHABLE* --> Quickly get up and running with PDAL [tutorials](tutorials/), [pipelines](cloudrunner/pipelines/), and [support scripts](scripts/) that illustrate how to scale from processing LIDAR in ```las``` or ```laz``` format as a [single](cloudrunner/pipelines/single) tile, [multicore processing](cloudrunner/pipelines/multi) across CPUs, or using [high throughput systems](chtc/) to distribute tiles across compute nodes.

1. *EXTENDABLE* --> Support advanced pipelines and workflows for remote sensing datasets that enable efficient sharing of processing chains targeting these areas:

    1. **Plant research**
        1. canopy stucture
        1. canopy change
    1.  **High throughput (HTC)** or **high performance computing (HPC)** computing environments
        ***(TODO : add link to UW CHTC)***

## HOW TO USE

To present LiDAR processing, the tutorials start with a single tile as a basis for scaling this understanding toward the design of larger, chainable workflows using lightweight ```JSON``` files. 

### Copy, Choose, Create

The workflows can provide templates to *copy* and *choose* from in order to understand the key elements it takes to *create* new workflows to be applied in in across various sensors, sites, and datasets:

- **Filtering decisions**       - coarse vs. fine + flagging vs. removal
- **Tiling & multiprocessing**  - optimizing a buffered cookie cutter
- **Tunable parameters**        - defining what matters between datasets
- **Configuration file input**  - remembering and reapplying the details

### Processing Units

The basic unit of processing for this library is a tile of LiDAR points, which should be sized based on a blend of computation power, patience, and the understanding of how point density and quantity can impact the ability for a machine to perform adequately.

#### Single Tile

Starting with a single tile can help identify important characteristics and provide a rough way to estimate input decisions.

#### Multiprocessing Batches

Extending this to processing large batches of hundreds of tiles is possible with a few small changes.


## Processing STEPS
To accomplish this, this toolset uses the PDAL stages as a way to build and step through a workflow:

1. PREP
    1. Grid site into tiles
    1. Buffer tiles
        1. Burn values as attribute: Buffer=1 (buffer area) / Buffer=0 (main tile)
1. MAIN
    1. CLEAN     - Outlier removal / add error flags
    1. GROUND    - Filter and classify ground points
    1. CANOPY    - Normalize height with DTM ```HeightAboveGround```
    1. ANCILLARY - generate cloud and neighborhood stats
        1. Density, Verticality, Eigen...
        1. Burn values into cloud as additional attributes
    1. CLEAN-UP  - finalize point cloud outputs
        1. Remove buffers
        1. Clip to final polygon border
        1. Merge & Export as COPC
        1. IDW, Max, Mean raster surfaces (DTM, DEM, CHM)
1. RESEARCH
    1. CALCULATE
        1. Voxels
        1. Percentiles
        1. LAI
        1. Defoliation
    1. EXTRACT
        1. Use "plot" or "tree" polygons to burn in attributes
        1. Combine rasters and point cloud to extract values within polygons
        1. Aggregate values (currently, the "mean" value is hard-coded)
    1. EXPORT
        1. write tables to CSV
    1. PLOT
        1. Create figures of important variables
        1. Verify results across datasets
        1. Quicklooks
        1. Metrics

## SETUP

The tutorials [README](tutorial/README.md) page contains detailed instructions on getting started.

## Jupyter Notebooks

These notebooks are provided as a way to work through datasets from start to finish, using a single tile to get started, then advancing to multiprocessing workflow.

 * [01 CloudRunner - Getting Started with LiDAR and Python](notebooks/01-CloudRunner-Getting_Started.ipynb)
 * [02 CloudRunner - Working with a Single LiDAR Tile](notebooks/02-CloudRunner-Single_Tile.ipynb)
 * [03 CloudRunner - Using PDAL for a Reproducible Multiprocessing Workflow](notebooks/03-CloudRunner-PDAL_Multiprocessing.ipynb)