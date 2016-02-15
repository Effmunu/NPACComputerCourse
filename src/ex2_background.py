#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading a FITS file and determining the background parameters.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import mylib
import library
from astropy.io import fits
import numpy as np

def main():
    """
    Reading a FITS file and determining the background parameters.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex2.txt"

    # open file and retrieve data
    try:
        with fits.open(input_file_path) as data_blocks:
            pixels = data_blocks[0].data

    except IOError:
        print "File not found :", input_file_path
        return 1

    # creating the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)
    print bin_values, bin_boundaries

    # write result to output file
#    try:
#        with open(output_file_path, 'w') as output_file:
#            output_file.write('background: %d, dispersion: %d' % (int(background), int(dispersion)))

#    except IOError:
#        print "File not found :", output_file_path
#        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
