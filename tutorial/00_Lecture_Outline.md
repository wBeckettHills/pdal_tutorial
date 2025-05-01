# An Intro to LiDAR processing for Ecological Metrics using PDAL and Python
*Beckett Hills, 2025*

## Learning Outcome
Provide an experiential introduction to the beginning stages of LiDAR processing, such as cleaning and classifying, typically necessary to work with data acquired with a UAS. 

## The Problem
Most publicly available datasets have reduced point cloud densities (2-5 points / m^2) and already have many processing steps completed. There are few tools supporting these processing stages beyond a basic toy dataset level, and often what's available will lack methods suitable for very dense datasets (150-500+ points / m^2) common to acquisitions with UAS payloads.

Dense point clouds often need to be broken down into tiles and processed using a parallelized approach in order to effectively handle the multiple preliminary cleaning, classification, and normalization stages. Scientific measurements with sensor payloads need an extra layer of transparency and reproducibilty in the form of configuration settings, workflow templates, and accurate metadata for file processing steps.


## Teaching Objectives

To address this need, this collection of teaching resources and code-based tutorials is designed around these objectives in order to provide a comprehensive series on using python to work with dense, raw point clouds.

### Overall
The primary *teaching* objectives:
1. Intro to specifics of UAS-based lidar data collections
1. Intro to python functions, scripts, and relevant skills needed for LiDAR

The primary *processing* objectives:
1. Copy, slightly modify, and run existing code
1. Use ```PDAL``` library to process lidar tiles 
1. Use ```Multiprocessing``` library to parallel process tiles across computer cores / threads

### Tutorial 
Experiential outcomes to help achieve overall outcomes:
1. Introduce a way to use python functions from a personal repo ```cloudrunner``` 
1. Inspect cloud attributes to assess processing
1. Processing experience:
    - Viewing a single tile and assessing processing loads
    - Using a multiprocessing / parallel approach requiring tiling and buffering steps
    - Creating output surfaces: DTM, DSM, CHM
    - Creating summary output metrics relevant for ecology studies
    - Optional:
        - Creating additional output surfaces: LAI ...
        - Colorization of point cloud with multispectral data


## Prep

### SETUP
1. Install conda (or miniconda) and jupyter notebooks (or VScode)
1. Get data downloaded and staged to define `wd`
1. Intro to background material on PDAL and LiDAR processing

## Lecture 1

### Plan:
1. Short lecture (slides)
    - show github repo
    - show LiDAR tile (QGIS, mention CloudCompare)
    - relevant LiDAR notes
        - cleaning
        - classifying
    - relevant Python notes
        - functions
        - scripts
        - dunder methods
    - relevant jupyter notebook notes
        - cell magic: time, bash, writefile
        - markdown cells
        - table of contents
1. Code-Along (jupyter notebook)
    - walk-through all necessary loading and processing steps needed for 2nd homework
        - list tiles
        - load functions with ```import```
        - run functions with ```multiprocessing```
        - (quick mention of use on other machines, e.g., a server)
1. Go over processing homework assignment for lecture 2
    - the assignment will have individuals working on different dates
    - their submissions will be used to create final dataset for lecture 2
    - background reading topics to cover:
        - discrete vs. full waveform
        - voxels
        - LiDAR metrics:
            - Leaf Area Density
            - Leaf Area Index

### Notes:
- Include office hour times



## Lecture 2

### Plan:
1. Short lecture (slides)
    - show student results
    - talk about metrics
1. Code-Along (jupyter notebook)
    - walk-through making some metrics
        - ```geopandas```
        - writing ```geoJSON``` and ```CSV``` files
    - create visulizations:
        - canopy cross-sections / profiles
        - defoliation through the season
1. Summarize learning
    - How / why is UAS-based processing different?
    - Python functions can easily be used and reused
    - LiDAR processing with a digital footprint for workflows:
        - PDAL config files
        - output config files
    - Food for thought:
        - Why is a feedback loop important for researchers actively working with or acquiring raw remote sensing products?

### Notes:
- Discuss field visits
