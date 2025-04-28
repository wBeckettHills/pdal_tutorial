# Introduction to LiDAR Processing with PDAL for Ecology

## Overview
<img src="https://github.com/wBeckettHills/cloudrunner/blob/main/graphics/CloudRunner-tile-oblique.png?raw=true" align='right' width=40%>

Light Detection and Ranging (LiDAR) has increased the breadth of remote sensing applications for ecological research by providing detailed three-dimensional data on vegetation structure and terrain characteristics. The use of point clouds derived from LiDAR observations has led to fundamental .... such as ..., ..., and ... . For ecologists, LiDAR data enables the quantification of ecosystem structure, which is essential for biodiversity monitoring, conservation, and restoration efforts.

This document introduces the Point Data Abstraction Library (PDAL) for processing LiDAR data in ecological applications, with particular attention to the differences between using pre-processed datasets versus handling raw data collected from drone platforms.

## PDAL: A Foundation for LiDAR Processing

PDAL (Point Data Abstraction Library) provides a format-agnostic, vendor-neutral framework for processing point cloud data. Similar to how GDAL works for 2D raster images, PDAL enables manipulation of 3D point cloud data specifically for geospatial applications. 

PDAL offers several key capabilities that make it particularly useful for ecological applications:

1. **JSON Configuration**: Simple format for building and sharing data pipelines
2. **Format Support**: Handles dozens of data formats including industry-standard LAS/LAZ
3. **Geospatial Reference**: Provides robust coordinate system transformations
4. **Processing Pipeline**: Enables chaining of operations for efficient workflows
5. **Python Integration**: Offers a Python API for integration with other scientific tools

## Pre-processed LiDAR Data vs. Drone-Collected Data
Working with pre-processed LiDAR data (e.g., from government agencies or commercial providers) requires less investment, since many steps have already been performed. While this can save time and funding, as well as create a baseline for assumptions** (expand on this more), the data coverage may be insufficient or unavailable. In many cases, municipalities may only provide leaf-off LiDAR (link to Wisconsin data here), which can significantly reduce levels of inquiry and application for research projects stufying vegetation. 

#### "Own the Data, Own the Problems"
<img src="https://github.com/wBeckettHills/cloudrunner/blob/main/graphics/CloudRunner-raw-outliers.png?raw=true" align='right' width=70%>
Flying aircraft with a LiDAR sensor can offer many benefits for researchers, yet the complexity is increased considerably. Producing repeateable methods and high-quality final geospatial layers of "scientific measurements" requires multiple processing steps within the broader stages of cleaning, normalization, and classification. Being both familiar and comfortable with these steps can increase the fidelity and diversity of input variables for structural canopy metrics.

#### Feedback is a Loop, Not an Arrow
It is important to understand the impact of decisions involved with data acquistions with drones or smaller aircraft, considering that each step is fundamentally linked to the quality of the output: advance planning, site selection, flight logistics, acquisition conditions, mission calibration standards, and final data handling. While all of these are critical to the final results, appropriate processing techniques are best approached as a circular pattern of feedback. The effort of pilots, sensor operators, data processors, and researchers are each critical aspects contributing to the final products. Research programs that rely on drones with senstive payloads like LiDAR must be in control of decisions and workflows at every level, creating robust standards that guide all procedures toward achieveing a project's scientific outcomes.

A data pipeline that incorporates timely feedback can reduce wasted planning and processing resources from failed acquisitions that simply didn't meet the objectives. Therefore, being both knowledgeable and proficient with LiDAR processing steps starting from this fairly ***raw*** format can share the effort, increase responsiblity, and utimately enhance a project's ability to meet promised outcomes. Closing the feedback loop around the acquisition and processing workflows by including timely and informative results creates a tighter connection between researchers and the techniques used to acquire data critical to their questions.

### Using Pre-processed Data

Data available from public sources typically involves:

1. **Data Acquisition**: Downloading already classified point clouds
2. **Minimal Processing**: Using points that already have classifications (ground, vegetation, etc.)
3. **Direct Analysis**: Creating DTMs, DSMs, and other products without extensive pre-processing

The advantage of this approach is simplicity and speed, allowing researchers to focus directly on analysis rather than processing steps.

### Processing Drone-Collected LiDAR Data

Drone-based LiDAR collection requires significant additional processing before analysis can begin:

1. **Data Management**: 
   - Handling large, unclassified point clouds
   - Splitting data into manageable tiles
   - Adding processing buffers to avoid edge effects
   - Removing outliers
   - Coregistering flight lines

2. **Ground Classification**: 
   - Identifying which points represent the ground surface
   - Considering algorithmic approaches for terrain and structural complexity
   - Often computationally intensive

3. **Height Normalization**: 
   - Creating digital terrain models (DTMs)
   - Calculating height above ground for all points
   - Essential for vegetation structure analysis

4. **Advanced Processing**:
   - Calculating neighborhood statistics for ecological metrics
   - Generating derived products like canopy density models
   - Classifying vegetation structure

These processing steps are crucial for generating geospatial data products of ecosystem height, cover, and complexity that can be used in ecology, conservation, restoration, and biodiversity monitoring.

## CloudRunner Processing Workflow

The CloudRunner processing pipeline implements a workflow specifically designed for ecological applications of LiDAR data. This workflow follows these key steps:

### 1. Preparation
- Cut large sites into a grid of manageable tiles
- Add processing buffers to avoid edge effects in analysis
- Tag points with buffer attributes for later removal

### 2. Main Processing
- **GROUND**   : Classify ground points using PDAL algorithms (ground=2)
- **CANOPY**   : Normalize vegetation heights using the ground classification
- **SURFACES** : Create digital terrain and surface models from classified points

### 3. Ancillary Processing
- Add attributes: Classify veg height using Z-value thresholds (low,med,high)
- Generate point cloud statistics (density, verticality, eigenvalues)
- Compute ecological metrics for vegetation structure
- Burn computed values back into the point cloud as attributes

### 4. Post-Processing
- Remove buffer regions used for processing
- Clip data to the final study area boundaries
- Merge tiles as needed for final products

### 5. Research Applications
- Extract values within plot or tree polygons
- Calculate Leaf Area Index (LAI) and other ecological metrics
- Aggregate values for statistical analysis
- Generate visualization products

## Processing Challenges with Drone LiDAR

Drone-collected LiDAR presents several unique challenges compared to using pre-processed data:

1. **Data Volume**: Processing LiDAR data can be computationally intensive, especially for ground classification algorithms that may require significant RAM (8-16GB+) and processor resources.

2. **Classification Quality**: Drone LiDAR often has lower point density than airborne systems, making ground classification more challenging in areas with dense vegetation.

3. **Registration Issues**: Multiple flight paths may require co-registration to ensure consistent point clouds.

4. **Edge Effects**: Processing individual tiles requires handling edge effects, often through the creation of buffered processing regions that are later removed.

5. **Outlier Removal**: Identifying errors in point returns such as birds or other outliers has a bit of art in the science, ranging from basic statistical thresholds to more adaptive neighborhood cleaning.

## PDAL Pipelines for Ecological Applications

PDAL utilizes a pipeline concept to chain together processing steps. A typical PDAL pipeline is defined in JSON format and can be executed through command-line tools. The CloudRunner workflow builds on this approach to create standardized processing steps for ecological applications.

Example pipeline components might include:

Pseudo-code
```
- read input
- classify ground (pmf algorithm)
- calculate height above ground (hag)
- write output
```

Actual pipeline with those elements:

```json
[
    {
        "type": "readers.las",
        "filename": "input.las"
    },
    {
        "type": "filters.classify",
        "algorithm": "pmf"
    },
    {
        "type": "filters.hag",
        "count": 4
    },
    {
        "type": "writers.las",
        "filename": "output.las"
    }
]
```

## Conclusion

While using pre-processed LiDAR data offers a simpler path to analysis, drone-collected LiDAR provides greater customization and up-to-date information but requires significantly more processing steps. The CloudRunner workflow addresses these challenges by implementing a standardized PDAL-based processing pipeline specifically for ecological applications, handling the technical complexities of LiDAR processing while enabling researchers to focus on ecological questions.

## References

1. Butler, H., et al. (2020). PDAL: An open source library for the processing and analysis of point clouds. *ScienceDirect*.

2. Lefsky, M. A., Cohen, W. B., Parker, G. G., & Harding, D. J. (2002). Lidar remote sensing for ecosystem studies: Lidar, an emerging remote sensing technology that directly measures the three-dimensional distribution of plant canopies, can accurately estimate vegetation structural attributes and should be of particular interest to forest, landscape, and global ecologists. *BioScience*, 52(1), 19-30.

... TODO ... add links, more content, supporting citations