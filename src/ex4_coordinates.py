#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading a FITS file, finding the clusters,
 and converting their centroid coordinates to WCS coordinates.
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
    Reading a FITS file, finding the clusters,
    and converting their centroid coordinates to WCS coordinates.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex4.txt"

    # open file and retrieve data and header
    header, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)
    bin_lower_boundaries = bin_boundaries[:-1]

    # apply the fit
    fit, _, m_x, _ = mylib.fit(mylib.gaussian, bin_lower_boundaries, bin_values)

    # get back the un-normalized data
#    maxvalue = fit[0] * m_y
    background = fit[1] * m_x
    dispersion = fit[2] * m_x

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    # find the clusters.
    clusters_list = mylib.find_clusters(pixels, threshold)
    clusters_dico = {}

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
    pads.text(0, len(pixels), '%f %f' \
              % my_wcs.convert_to_radec(0, len(pixels)), \
              color='white', fontsize=14)
    pads.text(len(pixels[0]), 0, '%f %f' \
              % my_wcs.convert_to_radec(len(pixels[0]), 0), \
              color='white', fontsize=14)
    pads.text(len(pixels[0]), len(pixels), '%f %f' \
              % my_wcs.convert_to_radec(len(pixels[0]), len(pixels)), \
              color='white', fontsize=14)

    # create the dictionnary of clusters
    # in the same time, find the maximum integral luminosity cluster
    max_integral = 0
    max_integral_key = ''
    for cluster in clusters_list:
        key = '%f %f' % cluster.centroid
        clusters_dico[key] = cluster
        cluster.centroid_wcs = my_wcs.convert_to_radec(cluster.centroid[1], \
                                                       cluster.centroid[0])
        # local attribute # c'est inversé apparemment
 #       pads.text(cluster.centroid[1], cluster.centroid[0], '%f %f' % cluster.centroid_wcs, \
 #                 color='white', fontsize=14) # display centroid coordinates
        if cluster.integral > max_integral:
            max_integral = cluster.integral
            max_integral_key = key

    mylib.event_handler(fig, my_wcs, pixels)
    # display
    plt.show()




    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('right ascension: %.10f, declination: %.10f' \
                              % (clusters_dico[max_integral_key].centroid_wcs))

    except IOError:
        print "File not found :", output_file_path
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
