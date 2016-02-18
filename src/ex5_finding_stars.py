#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
We read a FITS file, find the clusters,
and convert their centroid coordinates to WCS coordinates.
Then we display the celestial objects names on the image,
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
    Then we display the celestial objects names on the image,
    following the mouse movement.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex5.txt"

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

    radius = 0.003
    celestial_objects = library.get_objects(clusters_dico[max_integral_key].centroid_wcs[0], \
                                            clusters_dico[max_integral_key].centroid_wcs[1],
                                            radius)

    first_key = celestial_objects.keys()[0] # initialize
    for key in celestial_objects.keys():
        if celestial_objects[key] == 'Unknown':
            continue
        if key < first_key: # if before in alphabetic order
            first_key = key

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('celestial object: %s' % first_key)

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
