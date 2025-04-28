import os
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

import warnings

warnings.filterwarnings("ignore")

os.environ["PROJ_LIB"] = "/opt/conda/share/proj"


def runtile_treeseg(lasfile):
    # Run R
    script = "./code/runtile_R-treeseg.R"

    r = robjects.r
    r["source"](script)  # Loading the function defined in R
    tree_seg_r = robjects.globalenv["tree_seg"]

    lastile, ttops, chm = tree_seg_r(lasfile)

    # old way - needs to be deprecated out
    # return lastile


if __name__ == "__main__":
    runtile_treeseg()
