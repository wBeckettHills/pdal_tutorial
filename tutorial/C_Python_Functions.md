# Functions


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

This format is frequently used in the repo notebooks to help guide the steps being presented.


## Importing

A note on functions and re-using these scripts:

### "A WAY to do it"
Using functions contained in scripts  is a powerful way to leverage code execution in stand-alone scripts or in jupyter cell blocks. This can be done in many different ways. This is simply 'a way' to illustrate the ability to modularize and more easily customize code to enhance workflows over time. If moved or reused elsewhere, the tutorial directory needs to be structured like below so the relative paths for `cloudrunner`, `notebooks`, `scripts`, and `tutorials` are located in the correct place to ensure the notebooks can effectively locate and `import` the python support scripts without issue.


```
pdal_tutorial/
├── cloudrunner
│   ├── __init__.py
│   ├── multi
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── runtile_classify.py
│   │   ├── runtile_clean.py
│   │   ├── runtile_rasters_basics.py
│   │   ├── runtile_R-treeseg.R
│   │   ├── runtile_stats.py
│   │   └── runtile_treeseg.py
│   ├── pipelines
│   │   ├── 01_burntile.json
│   │   ├── 02_radialdensity.json
│   │   ├── 03_hag.json
│   │   ├── 04_eigen.json
│   │   ├── 05_covar.json
│   │   ├── 06_clip.json
│   │   ├── 07_burnTreeSN.json
│   │   ├── 08_exchangeZ.json
│   │   ├── 09_idw_chm.json
│   │   ├── 10_las_csv.json
│   │   ├── __init__.py
│   │   ├── pipelines.tar.gz
│   │   ├── README.md
│   │   └── test_colorize.json
│   └── single
│       ├── README.md
│       └── test_colorize.py
├── notebooks
│   ├── 00-CloudRunner-Conda_Jupyter.ipynb
│   └── 01-CloudRunner-Getting_Started.ipynb
├── scripts
│   ├── aggregateTrees.py
│   ├── bufferPoints.py
│   ├── examineGPStime.py
│   ├── makeCHTCconfig_lidar.py
│   ├── mergeCOPC.py
│   ├── README.md
│   └── saveLAIfigs.py
└── tutorials
    ├── 00_Lecture_Outline.md
    ├── 01_Intro_PDAL_Pipelines_for_Ecology.md
    ├── A_First_Time_Setup.md
    ├── B_Create_Start_Stop_Environments.md
    ├── C_Python_Functions.md
    └── README.md


```

### Better way: Code library
The above method is for simplicity, modularity, and repeatability, however, it is more complicated for versioning, maintaining, or quickly adapting to other situations. Creating a code library that can be imported would be the next step toward creating modular code that is also more adaptable.

Future steps will include how to use and install this library as a standalone package.

```import cloudrunner```

