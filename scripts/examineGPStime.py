###
# CloudRunner
# Beckett Hills
#
#
#
#

import os
import numpy as np
import matplotlib.pyplot as plt
import laspy
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def examineGPStime(las_file,sd_th,bins,idx_th):

    las = laspy.read(las_file)

    print(f'Las File {las_file}')
    d=[t for t in os.path.basename(las_file).split('_') if t.endswith('2021')][0]
    outdir = os.path.dirname(las_file)

    print(f'Date {d}')

    plt_idx=0

    # Create a plot
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(16,4),sharey=True,sharex=False,dpi=146)#,tight_layout=True)

    # Use the histogram to show tail densities of GPStime
    n, bins, patches = ax1.hist(las.gps_time,density=True, bins=bins)

    # threshold above the median
    tf = n > np.median(n) + (sd_th * np.std(n))

    # identify places this is above the threshold
    idx = np.where(tf==True)[0]
    print(f'idx = {idx}')

    # use some logic statements to get to selected min/max breaks
    try:
        # difference the array
        idx_split = idx[np.where(np.diff(idx) > 10)][0]
        min_slice= bins[1:][idx[idx == idx_split][0]]
        if np.all(np.diff(idx) < idx_th) & (idx[0] < idx_th):
            print(f'Not slicing max, using last index {bins[-1]}')
            max_slice = bins[-1]
        else:
            max_slice = bins[1:][(idx[idx > idx_split][0]) - 1 ]
    except:
        idx_split = 0
        min_slice= bins[0]
        if np.all(np.diff(idx) < idx_th) & (idx[0] < idx_th):
            print(f'Not slicing max, using last index {bins[-1]}')
            max_slice = bins[-1]
        else:
            max_slice = bins[1:][(idx[idx > idx_split][0]) - 1 ]

    # Plot vertical lines at selected min/max breaks
    for xe in [min_slice,max_slice]:
        ax1.axvline(x=xe, color='yellow', linewidth=1, linestyle='dashed')

    # Axis params
    ax1.set_xlim(las.gps_time.min(), las.gps_time.max())
    ax1.set_axis_off()
    ax1.set_title(f'{d} ORIG')

    # Slice Points
    las_taildrop = las[ (las.gps_time > min_slice) & (las.gps_time < max_slice) ]

    # Axis params
    ax2.hist(las_taildrop.gps_time,density=True, bins=100)
    ax2.set_axis_off()
    ax2.set_title(f'{d} NEW')

    # Write new las
    nam = las_file.split('.')[0]
    output_nam = f'{nam}_dt.las'
    las_taildrop.write(output_nam)

    st=plt.suptitle("WisAsp {d} LiDAR\nHistograms of GPStime")
    fig_nam = f'{outdir}/aspens_{d}_gpstime_hist.png'
    fig.tight_layout()
    fig.savefig(fig_nam, bbox_extra_artists=[st], bbox_inches='tight')
    plt.show()

    return output_nam


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Examine GPS time density")
    parser.add_argument("-i", "--input-las", help="Path and filename of input las file")
    parser.add_argument("-s", "--sd-threshold", help="Standard deviation threshold",default=.60)
    parser.add_argument("-n", "--n-bins", help="Number of bins", default=100)
    parser.add_argument("-x", "--idx-threshold", help="Index threshold distance",default=75)

    #read arguments from the command line
    args = parser.parse_args()

    input_las = args.input_las
    sd_th     = args.sd_threshold
    bins      = args.n_bins
    idx_th    = args.idx_threshold

    print("Running examineGPStime()...")

    output_las = examineGPStime(input_las,sd_th,bins,idx_th)

    print("Finished.")
