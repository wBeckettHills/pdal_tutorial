# Python Tips

## F-strings
F-strings are very convenient way to use python's object-oriented design to enhance readability and efficiency of code by concatenating the string together with variables or other more complex functions.

As an example with variables, they can be passed within `{}` if the string has an `f` prefix (no space!) on the string.

For example, variables can be set up ahead of time inside quotes `""` or `''`:

```
site="Aspens"
sensor="lidar"
date="05312021"

wd = "/long/path/to/working/directory"
```

These can now be used in an `f-string` to create a filename with underscores:

```
basename = f"{site}_{sensor}_{date}"

```

It can also be used to create a complete filepath with slashes and the `.las` suffix.

```
filepath = f"{wd}/{basename}.las"

```


## Using and Importing this Code
Python scripts and functions can be used in many ways. This repo uses a simple approach by keeping scripts with functions within particular relative directories to the notebooks being used.

### Scripts with Functions 
Python functions contained in scripts is a convenient way to use them for code execution in jupyter cell blocks or other stand-alone scripts. This is simply 'a way' to illustrate the ability to modularize and more easily customize code to enhance workflows over time. 

The tutorial directory needs to be structured so the python `.py` files with the functions are located in directories `cloudrunner`, `notebooks`, `scripts`, and `tutorials` relatively located within the main working directory as outlined in the **Tree Diagram** section below. This ensures the notebooks can successfully `import` the python support scripts without issue.

The directories are separated by . with the import function(s) trailing:
```
from cloudrunner.multi.runtile_classify import runtile_classify
```

The imported function can now available to be run:
```
runtile_classify(las_tile_path)
```
#### Tree Diagram
The filetree example below that shows how the directory structure can be used to access the functions within python files.

```
pdal_tutorial/
    ├── cloudrunner
    │   ├── multi
    │   │   ├── runtile_classify.py
    │   │   ├── runtile_clean.py
    │   │   ├── runtile_rasters_basics.py
    │   │   ├── runtile_R-treeseg.R
    │   │   ├── runtile_stats.py
    │   │   └── runtile_treeseg.py
    │   ├── pipelines
    │   │   ├── 00_test_colorize.json
    │   │   ├── 01_burntile.json
    │   │   ├── 02_radialdensity.json
    │   │   ├── 03_hag.json
    │   │   ├── 04_eigen.json
    │   │   ├── 05_covar.json
    │   │   ├── 06_clip.json
    │   │   ├── 07_burnTreeSN.json
    │   │   ├── 08_exchangeZ.json
    │   │   ├── 09_idw_chm.json
    │   │   └── 10_las_csv.json
    │   └── single
    │       └── test_colorize.py
    ├── data
    │   ├── lidar
    │   │   ├── raw
    │   │   └── tiles
    │   ├── shapes
    │   └── tif
    ├── notebooks
    │   ├── 00-CloudRunner-Conda_Jupyter.ipynb
    │   └── 01-CloudRunner-Getting_Started.ipynb
    ├── scripts
    │   ├── aggregateTrees.py
    │   ├── bufferPoints.py
    │   ├── examineGPStime.py
    │   ├── makeCHTCconfig_lidar.py
    │   ├── mergeCOPC.py
    │   └── saveLAIfigs.py
    └── tutorial
```
