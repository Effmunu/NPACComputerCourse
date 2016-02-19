#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
We read a FITS file, find the clusters,
and convert their centroid coordinates to WCS coordinates.
Then we display the WCS coordinates on the image,
following the mouse movement.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import library
import mylib

# pylint: disable=E1101
# 'numpy' has indeed an 'histogram' member, this error is not relevant


def main():
    """
    We read a FITS file, find the clusters,
    and convert their centroid coordinates to WCS coordinates.
    Then we display the WCS coordinates on the image,
    following the mouse movement.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex4.txt"

    # open file and retrieve data and header
    header, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)
    bin_lower_boundaries = bin_boundaries[:-1]

    # apply the fit (no need for the amplitude (first parameter))
    _, background, dispersion = mylib.gaussian_fit(bin_lower_boundaries, bin_values)

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    # create a WCS object
    my_wcs = library.WCS(header)

    # plot
    fig, pads = plt.subplots()

    # background removal on the image
    mask = pixels >= background + threshold
        # 2D-array of booleans, 'True' if value is above bkg
    pixels_bkg_sub = mask * (pixels - background)
    # visualization of the image before and after bkg removal
    pads.imshow(pixels_bkg_sub)

    # Display the corners coordinates
    pads.text(0, 0, '%f %f' % my_wcs.convert_to_radec(0, 0), \
              color='white', fontsize=14)
    pads.text(0, len(pixels[0]), '%f %f' \
              % my_wcs.convert_to_radec(0, len(pixels[0])), \
              color='white', fontsize=14)
    pads.text(len(pixels), 0, '%f %f' \
              % my_wcs.convert_to_radec(len(pixels), 0), \
              color='white', fontsize=14)
    pads.text(len(pixels), len(pixels[0]), '%f %f' \
              % my_wcs.convert_to_radec(len(pixels), len(pixels[0])), \
              color='white', fontsize=14)

    # find the clusters.
    clusters_list, clusters_dico = mylib.find_clusters(pixels, threshold)

    # find the maximum-integral cluster
    max_integral_key = mylib.find_max_integral_cluster(clusters_list)

    #
    for cluster in clusters_list:
        cluster.centroid_wcs = my_wcs.convert_to_radec(cluster.centroid[0], \
                                                       cluster.centroid[1])
            # local attribute
 #       pads.text(cluster.centroid[1], cluster.centroid[0], '%f %f' % cluster.centroid_wcs, \
 #                 color='white', fontsize=14) # display centroid coordinates

    mylib.event_handler(fig, my_wcs, pixels)
    # display
    plt.show()

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('right ascension: %.3f, declination: %.3f' \
                              % (clusters_dico[max_integral_key].centroid_wcs))

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
