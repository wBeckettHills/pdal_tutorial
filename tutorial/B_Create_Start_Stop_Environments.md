

# CREATE Environment

There are multiple ways to create an environment and install packages. To keep it simple, using `conda install` is the primary option recommended for using anything in this repo. 

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

For repeatable environments, a `environment.yml` file can be used for `conda` (`requirements.txt` for `pip`) and the actual package version number "pinned" to create exact rebuilds. This is a great practice beyond the scope of this intro, however, see the supporting files provided with advanced examples you can use to practice.

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

If all the packages installed without returning errors, then you should have everything inside the environment needed to proceed perform the steps of the tutorial.


--------

# Appendix : Advanced Options

This is only provided for future development or as a template for more advanced use.

## YAML File
```
# Make a new conda environment
conda env create -y --file conda_env_cloudrunner.yaml
```

# JupyterLab Command line

## Jupyter - START

As an option, Jupyter instance can be run on your local machine from within the environment.

### 1. Activate 

Activate an environment that contains jupyterlab:

```
conda activate cloudrunner
```

### 2. Run jupyter lab instance
> NOTES - the default port number 8080 has been changed below to 8090
>       - the `--notebooks` flag opens that path as the working directory

```
jupyter lab --port=8090 --ip "*" --notebooks ./pdal_tutorial/
```

### 3. Open Web Browser 

Navigate to ```127.0.0.1:48001``` or ```localhost:48001```



## Jupyter - STOP 

```
# Use the CTRL + C keys and then answer 'y' to stop the jupyter project
# in a manner that can be picked back up later
# ------------------------------------------------------------
```


## Jupyter - RESTART LATER

Similar to the Jupyter - START section above, to restart the project later you will need to follow these general steps:


### 1. Working Directory

#### Variable
This example provides a variable for the environment name and path to the correct project directory.

```
conda_env=cloudrunner
base_project_dir=/home/beckett/Desktop/${conda_env}
```

### 2. Activate Environment

Run ```conda activate``` command to start the environment:
```
conda activate ${conda_env}
```

### 3. Run jupyter lab instance

Now run the ```jupyter lab``` command to start the local jupyter server in that console window.

Do not close the console window, as this will kill the server.

```
jupyter lab --port=48001 --ip "*" --notebooks ${base_project_dir}
```

### 4. Open Web Browser 

Navigate to ```127.0.0.1:48001``` or ```localhost:48001```

