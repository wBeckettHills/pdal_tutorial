# Pipeline Required Inputs

TODO: fill in more details on the pipelines...


```
01_burntile.json
readers.las.filename = {input_las}
filters.overlay.datasource  = {burn_file}
filters.overlay.layer = {os.path.basename(burn_file).split(".")[0]}
writers.las.filename = {output_las}

02_sample.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

03_hag.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

04_eigen.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

05_covar.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

06_clip.json
readers.las.filename = {input_las}
filters.overlay.datasource  = {clip_file}
filters.overlay.layer = {os.path.basename(clip_file).split(".")[0]}
writers.las.filename = {output_las}

07_burnTreeSN.json
readers.las.filename = {input_las}
filters.overlay.datasource  = {tree_polys}
filters.overlay.layer = {os.path.basename(tree_polys).split(".")[0]}
writers.las.filename = {output_las}

08_exchangeZ.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

09_idw_chm.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

10_las_csv.json
readers.las.filename = {input_las}
writers.las.filename = {output_las}

```

