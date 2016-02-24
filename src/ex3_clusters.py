#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read a FITS image, then find the clusters of pixels above a threshold in an FITS image,
after background removal.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
import mylib

# pylint: disable=E1101
# 'numpy' has indeed an 'histogram' member, this error is not relevant

def main():
    """
    Reading a FITS file and finding the clusters in the image, after background removal.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex3.txt"

    # open file and retrieve data
    header, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)

    # apply the fit (no need for the amplitude (first parameter))
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    # find the clusters.
    cluster_list = mylib.find_clusters(header, pixels, threshold)
    cluster_dico = mylib.build_cluster_dico(cluster_list)

    # find the maximum-integral cluster
    max_integral_key = mylib.find_max_integral_cluster(cluster_list)

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('number of clusters: %2d, greatest integral: %7d, '
                              'centroid x: %4.1f, centroid y: %4.1f'
                              % (len(cluster_list),
                                 cluster_dico[max_integral_key][0].integral,
                                 cluster_dico[max_integral_key][0].centroid[0],
                                 cluster_dico[max_integral_key][0].centroid[1]))

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
