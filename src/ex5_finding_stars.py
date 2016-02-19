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
import matplotlib.patches as patches
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
    cluster_list, cluster_dico = mylib.find_clusters(header, pixels, threshold)

    # find the maximum-integral cluster
    max_integral_key = mylib.find_max_integral_cluster(cluster_list)

    # plot
    fig, pads = plt.subplots()
    # Display the image without background
    pads.imshow(mylib.remove_background(pixels, background, threshold))

    # Display the boxes around clusters
    for cluster in cluster_list:
        pads.add_patch(patches.Rectangle((cluster.box_xmin, cluster.box_ymin),
                                         cluster.box_xmax - cluster.box_xmin,
                                         cluster.box_ymax - cluster.box_ymin,
                                         fill=False, color='white'))

    # define an accetance radius around a given position
    radius = 0.003
    # Get the object name for each cluster.
    # Also, find the max_integral object name
    max_integral_object_name = ''
    # I create a name dico, so that we won't have to query for them every time
    cluster_name_dico = {}  # associate a centriod value (string) to the name
    for cluster_key in cluster_dico.keys():
        celestial_objects = library.get_objects(cluster_dico[cluster_key].centroid_wcs[0], \
                                                cluster_dico[cluster_key].centroid_wcs[1],
                                                radius)
        if not celestial_objects: # empty dictionary = False
            cluster_name_dico[cluster_key] = 'NO OBJECT FOUND'
            continue
        # now, there is at least one name available
        # find the first name in alphabetical order, skipping the 'Unknown'
        first_key = celestial_objects.keys()[0] # initialize
        for key in celestial_objects.keys():
            if celestial_objects[key] == 'Unknown':
                continue
            if key < first_key: # if before in alphabetic order
                first_key = key
        cluster_name_dico[cluster_key] = first_key
        if cluster_key == max_integral_key: # If the current cluster is the max integral one
            max_integral_object_name = first_key

    # call the event handler
    mylib.event_handler2(fig, header, pixels, cluster_list, cluster_name_dico)

    plt.show()

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('celestial object: %s' % max_integral_object_name)

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
