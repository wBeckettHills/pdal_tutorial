# First time setup

It is important to use conda environments to manage the packages and dependencies. If you already have this installed, skip to step 2.

## 1. Install Miniconda or Anaconda

First, download and install Miniconda / Anaconda if you haven't already. There are two options:

### 1. Conda website
Follow instructions for your operating system [on this page](https://www.anaconda.com/docs/getting-started/miniconda/install).

### 2. Command line for Linux
If you are comfortable with command line options, the bash cell block provides a starting point for a Linux installation. 

```
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

# Install Miniconda
bash miniconda.sh -b -p $HOME/miniconda

# Add conda to path
eval "$($HOME/miniconda/bin/conda shell.bash hook)"

# Initialize conda
conda init
```

## 2. Restart consonle

<p align="right">
  
</p>

Restart the console or bash terminal. It should now begin with ```(base)``` to left of your user@device name, similar to what is shown in the images below. If you see ```(base)```, proceed to the next steps.

```(base) username@laptop:~$```

If you don't see ```(base)```, something happened that may require troubleshooting, or reinstalling, the miniconda installation.

<p align="center">
  <img src="https://github.com/wBeckettHills/pdal_tutorial/blob/development/graphics/CloudRunner-console-windows-conda.png?raw=true" width=45%>
  <img src="https://github.com/wBeckettHills/pdal_tutorial/blob/development/graphics/CloudRunner-console-windows-gitbash.png?raw=true" width=45%>
</p>


## ```Jupyter Notebooks```

There are multiple options for using jupyter. If you are familiar with and already have an established way to use them, then proceed to the next notebook. 

To use jupyter notebooks, there are two good (free) options:
1. ```VS Code```  - [Visual Studio Code](https://code.visualstudio.com/download)
    - This is not an endorsement!
    - That said, VSCode handles different file types and has extensions for various languages and utilities (python, R, bash, markdown, JSON, CSV, jupyter notebooks), making it a bit easier to have one software that does it all
1. ```Jupyterlab```
    - this is a very simple, lightweight version for notebooks
    - it can be installed and run within a conda environment to make package loading easy. 
        Generic usage example (it is best installed after primary packages, but this is the very basic use):
        ```
        conda activate my_environment
        conda install jupyter jupyterlab
        jupyterlab
        ```

Now, you should be ready to create conda environments, install packages, and open and run notebooks on your local machine. 

