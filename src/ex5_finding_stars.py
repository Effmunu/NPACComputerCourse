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

    # apply the fit (no need for the amplitude (first parameter))
    _, background, dispersion = mylib.gaussian_fit(bin_lower_boundaries, bin_values)

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    # find the clusters.
    clusters_list, clusters_dico = mylib.find_clusters(pixels, threshold)

    # find the maximum-integral cluster
    max_integral_key = mylib.find_max_integral_cluster(clusters_list)

    # plot
    fig, pads = plt.subplots()

    pads.imshow(mylib.remove_background(pixels, background, threshold))



    radius = 0.003
    max_integral_object = ''
    # Get the object name for each cluster. Also, find the max_integral object name
    for cluster_key in clusters_dico.keys():
        celestial_objects = library.get_objects(clusters_dico[cluster_key].centroid_wcs[0], \
                                                clusters_dico[cluster_key].centroid_wcs[1],
                                                radius)
        if not celestial_objects: # empty dictionary = False
            continue
        first_key = celestial_objects.keys()[0] # initialize
        for key in celestial_objects.keys():
            if celestial_objects[key] == 'Unknown':
                continue
            if key < first_key: # if before in alphabetic order
                first_key = key
        pads.text(clusters_dico[cluster_key].centroid[0], clusters_dico[cluster_key].centroid[1], \
                  '.%s' % first_key, color='white', fontsize=14)
        if cluster_key == max_integral_key: # If the current cluster is the max integral one
            max_integral_object = first_key

    plt.show()



    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('celestial object: %s' % max_integral_object)

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
