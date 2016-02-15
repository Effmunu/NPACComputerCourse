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

def main():
    """
    Reading a FITS file and determining the background parameters.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex2.txt"



    # open file and retrieve data
    try:
        with fits.open(input_file_path) as data_blocks:
            data_blocks.info()
            pixels = data_blocks[0].data
            print type(pixels)

    except IOError:
        print "File not found :", input_file_path
        return 1



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
