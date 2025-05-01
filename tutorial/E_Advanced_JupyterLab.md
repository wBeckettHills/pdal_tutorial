
# Appendix : Advanced Options

## JupyterLab Command line

### Jupyter - START

As an option, Jupyter instance can be run on your local machine from within the environment.

#### 1. Activate 

Activate an environment that contains jupyterlab:

```
conda activate cloudrunner
```

#### 2. Run jupyter lab instance
> NOTES - the default port number 8080 has been changed below to 8090
>       - the `--notebooks` flag opens that path as the working directory

```
jupyter lab --port=8090 --ip "*" --notebooks .

OR 

jupyter lab --port=8090 --ip "*" --notebooks ./pdal_tutorial/

```

#### 3. Open Web Browser 

Navigate to ```127.0.0.1:48001``` or ```localhost:48001```



### Jupyter - STOP 

```
# Use the CTRL + C keys and then answer 'y' to stop the jupyter project
# in a manner that can be picked back up later
# ------------------------------------------------------------
```


### Jupyter - RESTART LATER

Similar to the Jupyter - START section above, to restart the project later you will need to follow these general steps:


#### 1. Working Directory

##### Variable
This example provides a variable for the environment name and path to the correct project directory.

```
conda_env=cloudrunner
base_project_dir=/home/beckett/Desktop/${conda_env}
```

#### 2. Activate Environment

Run ```conda activate``` command to start the environment:
```
conda activate ${conda_env}
```

#### 3. Run jupyter lab instance

Now run the ```jupyter lab``` command to start the local jupyter server in that console window.

Do not close the console window, as this will kill the server.

```
jupyter lab --port=48001 --ip "*" --notebooks ${base_project_dir}
```

#### 4. Open Web Browser 

Navigate to ```127.0.0.1:48001``` or ```localhost:48001```
