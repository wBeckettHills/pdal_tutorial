# Appendix : Advanced Options

## Reproducile Environments

For easily replicating environments, files can be used to control this more carefully. An `environment.yml` file can be used for `conda` while for `pip` it is a `requirements.txt` file. For both methods, the actual package version number can be "pinned" to create exact rebuilds. This is a great practice beyond the scope of the intro, however, notes are included as well as an example `YAML` file (`conda_env_cloudrunner.yaml`) is provided with this repo in order to encourage best practices.

## YAML File
```
conda env create -y --file conda_env_cloudrunner.yaml
```
