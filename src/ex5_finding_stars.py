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

# TODO : possible upgrade : only display the rectangle when the mouse is
# over it, meaning we should connect to mpl in the event handler
def event_handler(fig, header, pixels, cluster_list, cluster_dico):
    """
    Event handler
    :param fig: the canvas to draw into
    :param my_wcs: The conversion tool for coordinates
    :param pixels: The image to display
    :return:
    """
    # create a WCS object to make unit conversions
    my_wcs = library.WCS(header)

    def on_click(event):
        if event.xdata >= len(pixels) or event.xdata < 0 \
                or event.ydata >= len(pixels) or event.ydata < 0:
            # if outside the image
            return

        pads = event.inaxes     # get the current pad

        centroid_to_query = -1, -1
        for cluster in cluster_list:
#            if (event.xdata, event.ydata) in cluster.pixel_list:
            if event.xdata >= cluster.box_xmin and \
                            event.xdata <= cluster.box_xmax and \
                            event.ydata >= cluster.box_ymin and \
                            event.ydata <= cluster.box_ymax:
                centroid_to_query = '%f %f' % (cluster.centroid[0], cluster.centroid[1])
                break   # found the cluster clicked on
        # if we didn't click on a cluster box, just redraw the picture
        if centroid_to_query[0] < 0:
            event.canvas.draw()
            return

        text_id = pads.text(event.xdata, event.ydata, "%f, %f \n%s"
                            % (my_wcs.convert_to_radec(event.xdata, event.ydata)[0],
                               my_wcs.convert_to_radec(event.xdata, event.ydata)[1],
                               cluster_dico[centroid_to_query][1]),
                            fontsize=14, color='white')
        event.canvas.draw()
        text_id.remove()

    fig.canvas.mpl_connect('button_press_event', on_click)


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

    # apply the fit (no need for the amplitude (first parameter))
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    # define an accetance radius around a given position to get the name from Simbad
    radius = 0.003
    cluster_list, cluster_dico = mylib.find_clusters(header, pixels, threshold, radius)

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

    # find the maximum-integral cluster
    max_integral_key = mylib.find_max_integral_cluster(cluster_list)

    # call the event handler
    event_handler(fig, header, pixels, cluster_list, cluster_dico)

    plt.show()

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('celestial object: %s' % cluster_dico[max_integral_key][1])

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
