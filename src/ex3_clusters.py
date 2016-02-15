#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import mylib


class Cluster:
    """

    """
    def __init__(self):


def main():
    """
    Reading a FITS file and finding the clusters in the image, after background removal.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex3.txt"

    # open file and retrieve data
    try:
        with fits.open(input_file_path) as data_blocks:
            pixels = data_blocks[0].data

    except IOError:
        print "File not found :", input_file_path
        return 1

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)
    bin_lower_boundaries = bin_boundaries[:-1]

    # apply the fit
    fit, _, m_x, m_y = mylib.fit(mylib.gaussian, bin_lower_boundaries, bin_values)

    # get back the un-normalized data
    maxvalue = fit[0] * m_y
    background = fit[1] * m_x
    dispersion = fit[2] * m_x

    #
    threshold = background + (6.0 * dispersion)

    pixels_visited = np.zeros_like(pixels)

    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            pixels_visited[row, col] = 1    # pixel visited
            # On en est à là : is it below the threshold? (a value is considered if greater or equal to threshold)

    cluster = Cluster()




    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('number of clusters: %d, greatest integral: %d' \
                              % (len(reg.clusters), max_integral))

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
