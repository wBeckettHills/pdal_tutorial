#! /usr/bin/Rscript

library(lidR)
library(sf)
library(tictoc)
library(viridis)
library(terra)

lidR::set_lidr_threads(1)

tree_seg <- function(tilename){
    base_dir          = paste0(dirname(dirname(tilename)),"/tiles_trees")
    las_file_name     = basename(tilename)
    base_name         = unlist(strsplit(las_file_name,".laz"))

    tile_size = 60.0
    
    xmin=as.numeric(unlist(strsplit(las_file_name,"_"))[7])
    xmax=as.numeric(xmin+tile_size)
    
    ymax=as.numeric(unlist(strsplit(las_file_name,"_"))[8])
    ymin=as.numeric(ymax-tile_size)

    bbox = c(xmin = xmin, ymin = ymin, xmax = xmax, ymax = ymax)

    print(tilename)
    print(base_name)

    # VARIABLES
    plot              = FALSE
    res_cm            = 25
    res_m             = res_cm / 100.0
    las_output_type   = "laz"

    las_file_suffix   = "tree-seg-w"
    #las_file          = paste0(base_dir,'/',las_file_name)
    las_outfile       = paste0(base_dir,'/',base_name,'_',las_file_suffix,'.',las_output_type)

    ttops_file_suffix = "trees"
    ttops_file_ext    = "geojson"
    ttops_layer_name  = paste0(base_name,"_",ttops_file_suffix,".",ttops_file_ext)
    ttops_file_name   = paste0(base_dir,'/',ttops_layer_name)

    chm_file_suffix   = "chm"
    chm_file_type     = "ENVI"
    chm_file_name     = paste0(base_dir,'/',paste0(base_name,"_",chm_file_suffix))


    # READ FILE
    las <- readLAS(tilename)#, filter = "-drop_z_below 0 -drop_z_above 45")
    print(las@header)

    # TREE WINDOW SIZE FUNCTION
    print("Locating Trees")
    tic()
    ttops = list()
    f <- function(x) {
        y <- 3.75 * (-(exp(-0.08*(x-2)) - 1)) + 3.15
        y[x < 1.75] <- 3
        y[x > 20] <- 6
        return(y)
        }
    heights <- seq(-5,30,.25)
    ws <- f(heights)
    toc()


    if(plot==TRUE){
        #png("", width=6, height=5, units="in", res=1200)
        dev.new(width=10, height=10, unit="in")
        plot(heights, ws, type = "l",  ylim = c(0,6))
        #dev.off()
        }

    # TREES
    tic()
    ttops = list()
    ttops <- locate_trees(las, lmf(ws = f))
    toc()

    # CHM
    print("Making CHM")
    tic()
    chm <- rasterize_canopy(las, res = res_m, pitfree(thresholds = c(0, 1, 2, 4, 5, 8, 12, 20), max_edge = c(0, .1)))
    toc()

    # SEGMENT
    print("Segmenting Trees")
    las   <- segment_trees(las, watershed(chm, th_tree = 1, tol = 1, ext = 2),attribute = "TreeIDw")

    # PLOT
    if (plot==TRUE) {
        dev.new(width=10, height=10, unit="in")
        options(repr.plot.width = 4, repr.plot.height = 4, repr.plot.res = 300)
        plot(chm, col=turbo(100),zlim=c(0,35))
        plot(sf::st_geometry(ttops), add=TRUE, pch = 19, cex= .8, col="red")
        title(main="Variable Window Size",
            sub=paste0("Tree / Shrub Count = ",nrow(ttops)),
            adj = 0.4
            )
        }


    # CREATE OUPUTS

    ## POINT FILE
    print("Converting point format ...")
    ## - convert to dataframe
    ttops_df <- sfheaders::sf_to_df(ttops, fill = TRUE)
    ## - add Z & M columns
    #ttops_df$z <- rnorm(nrow(ttops_df))
    ## - convert back to 'sf' object
    ttops_sf <- sfheaders::sf_point(
        obj = ttops_df,
        x = "x",
        y = "y",
        z = "Z",
        keep = T
    )

    ## - write point file
    print("Writing tree tops file ...")
    ttops_sf = sf::st_set_crs(ttops_sf,32616)
    ttops_sfc = sf::st_crop(ttops_sf,bbox)
    sf::st_write(ttops_sfc, dsn = ttops_file_name, layer = ttops_layer_name, delete_dsn=TRUE)

    ## LAS FILE
    print("Writing las file ...")
    las$TreeIDw = as.integer(las$TreeIDw)
    las$TreeIDw[is.na(las$TreeIDw)] = 0
    las@header@VLR$Extra_Bytes$`Extra Bytes Description`$TreeIDw$data_type <- 1L
    las_write = filter_poi(las, Classification != 2L)
    writeLAS(las_write,las_outfile,index=TRUE)

    ## RASTER FILE
    print("Writing raster ...")
    writeRaster(chm, chm_file_name, overwrite=TRUE, NAflag=-9999.0,filetype = chm_file_type)
    
    # SCRIPT OUPUT
    print("Finished script... writing to output stream")
    #output = paste(las_outfile,ttops_file_name,chm_file_name,sep=",")
    output = list(las_outfile,ttops_file_name,chm_file_name)
    return(output)
}
