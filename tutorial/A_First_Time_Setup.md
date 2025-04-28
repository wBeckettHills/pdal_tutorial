# First time setup

It is important to use conda environments to manage the packages and dependencies. If you already have this installed, skip to step 2.

## 1. Install Miniconda or Anaconda

First, download and install Miniconda / Anaconda if you haven't already. There are two options:

### A. Conda website
Follow instructions for your operating system [on this page](https://www.anaconda.com/docs/getting-started/miniconda/install).

### B. Command line for Linux
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

## 2. Restart console

<img src="https://github.com/wBeckettHills/pdal_tutorial/blob/development/graphics/CloudRunner-console-windows-conda.png?raw=true" align="right" width=55%>


Restart the console or bash terminal. It should now begin with ```(base)``` to left of your user@device name, similar to the examples in the images to the right. If you see ```(base)```, proceed to the next steps.


```(base) username@laptop:~$```

If you don't see ```(base)```, something happened that may require troubleshooting, or reinstalling, the miniconda installation.

<br>
<br/>
<img src="https://github.com/wBeckettHills/pdal_tutorial/blob/development/graphics/CloudRunner-console-windows-gitbash.png?raw=true" align="right" width=55%>

<br>
<br/>

## ```Jupyter Notebooks```

There are multiple options for using jupyter. If you are familiar with and already have an established way to use them, then proceed to the next notebook. This has not been tested in Google Collab environments and may not work as expected.

To use jupyter notebooks, there are two good (free) options:
1. ```VS Code```  - [Visual Studio Code](https://code.visualstudio.com/download)
    - This is not an endorsement!
    - That said, VSCode handles different file types and has extensions for various languages and utilities (python, R, bash, markdown, JSON, CSV, jupyter notebooks), making it a bit easier to have one software that does it all
2. ```Jupyterlab```
    - this is a very simple, lightweight, portable version for using notebooks
    - it can be installed and run within a conda environment to make package loading easy. 
        Generic usage example (it is best installed after primary packages, but this is the very basic use):
        ```
        conda activate my_environment
        conda install jupyter jupyterlab
        jupyterlab
        ```

Now, you should be ready to create conda environments, install packages, and open and run notebooks on your local machine. 

