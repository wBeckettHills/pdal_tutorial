import os
import json
import pdal
import numpy as np
import geopandas as gpd


def dirCheck(directory):
    if not os.path.exists(directory):
        print("Making new directory: ", directory)
        os.mkdir(directory)
    else: 
        print("Using existing directory: ", directory)

def runTile(pdalJSON,output_tile_name):
    print("Running tile using input JSON: \n      -> ", pdalJSON)
    # Begin PDAL pipeline for the calculation step
    j = open(pdalJSON)
    c2t_pipeline = pdal.Pipeline(json.dumps(json.load(j)))
    #c2t_pipeline.validate()
    #pipeline.loglevel = 8 #really noisy
    count = c2t_pipeline.execute() # run the pipeline
    j.close() # close the file
    #metadata = c2t_pipeline.metadata #point cloud info, could be useful for bounding box
    return output_tile_name

def makeBufferedTiles(input_poly, output_dir, field="id", buffer=30):
    '''
     -> returns a list of filepaths for tile polygons
    '''
    from osgeo import ogr
    import os
    
    file_name = os.path.basename(input_poly).split(".")[0]
    file_type = input_poly.split(".")[1]
    
    print("File Type :",file_type)
    if file_type == "shp":
        file_driver = 'ESRI Shapefile'
    if file_type == "geojson":
        file_driver = 'GeoJSON'
    else:
        print("Unrecognized format")
    
    poly_lyr = gpd.read_file(input_poly,driver=file_driver)
    poly_lyr.set_index(field)
    
    tile_polys = []
    for index,feature in poly_lyr.iterrows():
        fid = feature[field]
    
        # Create Output Tile
        tile_ftr = os.path.join(output_dir, file_name +'_buff_'+ str(0) +'_'+ field +'_'+ str(fid)  +'.'+ file_type)
        print(" -> Output Tile Feature Path : ",tile_ftr)
        tile_feature = gpd.GeoDataFrame([{field:2,'Buffer': 0,'geometry': feature["geometry"]}])
        tile_feature.to_file(tile_ftr,driver='GeoJSON')
            
        # Create Output Buffer Tile
        out_buff_ftr = os.path.join(output_dir, file_name +'_buff_'+ str(buffer) +'_'+ field +'_'+ str(fid)  +'.'+ file_type)
        print(" -> Output Buffer Feature Path : ",out_buff_ftr)
        buff_feature = gpd.GeoDataFrame([{field:1,'Buffer': 1,'geometry': feature["geometry"].buffer(buffer)}])
        buff_feature.to_file(out_buff_ftr,driver='GeoJSON')
    
        # Create Output Union Tile
        out_union_ftr = os.path.join(output_dir, file_name +'_union_'+ str(buffer) +'m_'+field +'_'+ str(fid)  +'.'+ file_type)
        print(" -> Output Union Feature Path : ",out_union_ftr)
        
        new_feature = tile_feature.overlay(buff_feature,how='union')
        new_feature.at[1,field+"_1"] = 1
        new_feature[field] = new_feature[field+"_1"]
        new_feature.at[0,"Buffer"] = int(0)
        new_feature.at[1,"Buffer"] = int(1)
        del new_feature[field+"_1"]
        del new_feature[field+"_2"]
        del new_feature["Buffer_1"]
        del new_feature["Buffer_2"]
        new_feature.to_file(out_union_ftr,driver='GeoJSON')
        tile_polys.append(out_union_ftr)
    return tile_polys
        

def makeJSON_burntile(input_las, output_las, outputJSON, burn_file, min_Z, max_Z, attribute="Buffer"):
    import os
    pdal_json_burntile = [
        {
            "type": "readers.las",
            "filename": input_las
        },
        {
            "type" : "filters.range",
            "limits" : "Z[{0}:{1}]".format(min_Z,max_Z)
        },
        {
            "type": "filters.ferry",
            "dimensions": "=>"+attribute
        },
        {
            "type":"filters.assign",
            "value": attribute+" = 3"
        },
        {
            "type":"filters.assign",
            "value": "Classification = 0"
        },
        {
            "column": attribute,
            "datasource": burn_file,
            "dimension": attribute,
            "layer": os.path.basename(burn_file).split(".")[0],
            "type": "filters.overlay"
        },
        {
            "type":"filters.assign",
            "value":
            [
                "Classification = 18 WHERE "+attribute+" > 1",
                "Classification = 12 WHERE "+attribute+" == 1"
            ]  
        },
        {
            "type":"filters.range",
            "limits": attribute+"[:1]"
        },
        {
            "type": "writers.las",
            "filename": output_las,
            "extra_dims": attribute+"=int16",
            "minor_version": "4",
            "forward": "all"
        }
    ]
    with open(outputJSON, "w") as outjson:
        json.dump(pdal_json_burntile, outjson,indent=4,skipkeys=True, ensure_ascii = False)
        
    return outputJSON


def cloud2Tiles(las_file, input_poly, tile_dir, config_dir, zlims, step="burntile", poly_field="id", subtractBuffer=0.0, burn=None):
    '''
     -> input_poly should contain feature geometries that represent the desired tile output
         such as a grid/fishnet or group of polygons for parallel processing
     -> it is assumed there is a buffer to be applied, 0.0 will indicate no buffer
     -> a "Buffer" attribute field will be added with 1 to indicate the buffered area
     -> returns a list of filepaths for las point cloud tiles
    '''
    print("Creating Tiles")
    
    min_Z, max_Z = zlims
    
    dirCheck(tile_dir)
    
    poly_tiles = makeBufferedTiles(input_poly, output_dir=tile_dir, field=poly_field, buffer=30)
    
    tiles = []
    for tile in poly_tiles:
        tile_number = os.path.basename(tile).split("_" + poly_field + "_")[1].split(".")[0]
        print("Working on tile number : ", str(tile_number))
        tile_id = poly_field + "_"+ str(tile_number)

        #Create names and filepaths
        file_name = os.path.basename(las_file).split(".")[0]
        output_name = tile_dir +'/'+ file_name + "_" + tile_id + ".las"
        pdal_json_file  = config_dir +'/'+ file_name + "_" + step + "_" + tile_id + ".json"
                
        # Create JSON file
        print("  -> Input Las   : ", las_file)
        print("  -> Output Name : ", output_name)
        print("  -> Burn File   : ", tile)
        burntileJSON = makeJSON_burntile(input_las=las_file, output_las=output_name, outputJSON=pdal_json_file, burn_file=tile, min_Z=min_Z, max_Z=max_Z, attribute="Buffer")

        tile_name = runTile(burntileJSON, output_name)
        tiles.append(tile_name)
    return tiles
