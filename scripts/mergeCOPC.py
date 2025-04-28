#!/usr/bin/python3
'''



'''

import os
import sys
import json
import glob
import pdal
import argparse


def mergeCOPC(tile_dir,output_filename,step):
    '''
    Create a COPC laz by merging tiles

    '''
    print("Merging results")
    import glob

    tile_names = glob.glob(os.path.join(tile_dir,"*"+step+".las"))
    filename = os.path.basename(output_filename).split(".")[0]
    pdal_json_merge_file  = tile_dir +'/'+ filename + ".json"
    pdal_vlrs_file = tile_dir +'/'+ filename + "_vlrs.json"

    outputs = ""
    for t in tile_names:
        #n = t.replace('.las','_'+step+'.copc.laz')
        #outputs += '"' + n + '",'
        outputs += '"' + t + '",'

    #Not used yet
    #vlrs = makeVLRS()

    print("Outputs:\n",outputs)
    print("Output Filename:\n",output_filename)
    #print("VLRS :\n",vlrs)

    pdal_json_merge = '[' + outputs + '{"type": "filters.merge"},{"type": "writers.copc", "filename":"' + output_filename + '", "forward": "all", "pipeline":"true" } ]'
    #pdal_json_merge = '[' + outputs + '{"type": "writers.copc", "filename":"' + output_filename + f'", "forward": "all", "pipeline":"true", "vlrs": {vlrs}'+' } ]'
    #pdal_json_merge = '[' + outputs + '{"type": "writers.pcd", "filename":"' + output_name + '","extra_dims": "all"}]'

    print("JSON merge :\n",pdal_json_merge)

    with open(pdal_json_merge_file, "w") as outjson:
        json.dump(pdal_json_merge, outjson,indent=4,skipkeys=True, ensure_ascii = False)

    #j = open(pdal_json_merge_file)
    pipeline = pdal.Pipeline(json.dumps(json.loads(pdal_json_merge)))
    #j.close() # close the file
    #pipeline.loglevel = 8 #really noisy
    count = pipeline.execute() # run the pipeline
    metadata = pipeline.metadata #point cloud info, could be useful for bounding box
    #arrays = pipeline.arrays # for use as numpy arrays
    return output_filename



if __name__ == "__main__":

    '''
    Variables to edit for input
    ToDo - make this a JSON
    '''
    parser = argparse.ArgumentParser(description = "Merge tiles into COPC laz")
    parser.add_argument("-t", "--tile-dir", help="Path to directory of tiles")
    parser.add_argument("-o", "--output-name", help="Output filename")
    parser.add_argument("-s", "--step", help="The calculated step or attribute to glob", default='TreeSN')

    #read arguments from the command line
    args = parser.parse_args()

    tile_dir        = args.tile_dir
    output_filename = args.output_name
    step            = args.step

    print(f'Running Tiles \n  ---> {tile_dir}')

    output_filename = mergeCOPC(tile_dir,output_filename,step)

    print(f'Finished merging: \n {output_filename}')
