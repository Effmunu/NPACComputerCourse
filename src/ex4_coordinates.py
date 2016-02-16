#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading a FITS file, finding the clusters
 and converting their centroid coordinates to WCS coordinates.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import library
import Cluster
import mylib

def move(event):
    """

    :param event:
    :return:
    """


def main():
    """

    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex4.txt"

    # open file and retrieve data and header
    try:
        with fits.open(input_file_path) as data_blocks:
            pixels = data_blocks[0].data
            header = data_blocks[0].header

    except IOError:
        print "File not found :", input_file_path
        return 1

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

    # We define an array of pixels visited: 1 if visited, 0 elsewise
    pixels_visited = np.zeros_like(pixels)
    # List and dictionary of clusters:
    clusters_list = []
    clusters_dico = {}

    # find the clusters
    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            if pixels_visited[row, col]:
                continue # If pixel visited, g to next pixel (next step of the loop)
            if pixels[row, col] < threshold:
                pixels_visited[row, col] = 1 # visited
            else: # add the new cluster to the list
                pixels_in_cluster = mylib.find_cluster(pixels_visited, pixels, row, col, threshold)
                cluster = Cluster.Cluster(pixels_in_cluster, pixels)
                clusters_list.append(cluster)
                pixels_visited[row, col] = 1 # visited
    print 'test'
    # create a WCS object
    my_wcs = library.WCS(header)
    print 'test'
    # create the dictionnary of clusters
    # in the same time, find the maximum integral
    max_value = 0

    for cluster in clusters_list:
        key = '%f %f' % cluster.centroid
        clusters_dico[key] = cluster
        cluster.centroid_wcs = my_wcs.convert_to_radec(cluster.centroid[0], cluster.centroid[1])
        if cluster.centroid_value > max_value:
            max_value = cluster.centroid_value
            max_value_key = key
        print cluster.centroid_wcs # No cluster with the right coordinates !!!
    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('right ascension: %.10f, declination: %.10f' \
                              % (clusters_dico[max_value_key].centroid_wcs))

    except IOError:
        print "File not found :", output_file_path
        return 2
    print 'test'
    return 0

if __name__ == '__main__':
    sys.exit(main())
