

# CONDA Environments

There are multiple ways to create conda environments and install packages. To keep it simple, using `conda install` from the command line is the primary tested option recommended for use with this repo. 

In preparation for future guides, there are *Advanced* methods also shown below. These may not work as expected due to the rapid developments of this project over time. They are best viewed as examples to start with as a template.


## 1. Create an Environment

```
conda create -n lidar_env "python=3.13"
```

## 2. Activate Environment

```
conda activate lidar_env
```

## 3. Install Packages

For the purposes of this tutorial, `conda` is the ideal way to install the packages. Installing `GDAL` into packages can sometimes be problematic with `pip`, so while `conda` is much slower for installing, when building new environments it helps to stay consistent with `conda` or `pip` as the primary way to install. This is a nuanced topic with many caveats and reasonable scenarios where conda, pip, and custom makefiles or git repo installs can all be carefully installed and used within one environment. 

### `conda install`

Building an environment with geospatial libraries such as `GDAL` can benefit from installing them in groups, starting with the base dependencies and finishing with extra libaries for plotting or `ipython` notebook widgets.

The install lines below are separated into suggested groups, which provides the option to install line-by-line for better control over possible errors that may pop up.

```
# Install packages
conda install -c conda-forge -y setuptools wheel scipy numpy proj pyproj geos
conda install -c conda-forge -y gdal libgdal rasterio
conda install -c conda-forge -y pdal python-pdal
conda install -c conda-forge -y geopandas geojson jupyter jupyterlab
conda install -c conda-forge -y ipykernel ipywidgets matplotlib ipympl
```
  
If all the packages installed without returning errors, then you should have everything inside the environment needed to proceed with the rest of the tutorial.