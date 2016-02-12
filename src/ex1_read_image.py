#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading and displaying a FITS file
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import matplotlib.pyplot as plt
from astropy.io import fits

def main():
    """
    Reading and displaying a FITS file
    """

    inputFilePath = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    outputFilePath = "/Users/npac09/PycharmProjects/npac09/src/ex1.txt"


    try:
        with fits.open(inputFilePath) as data_blocks:
            data_blocks.info()

            pixels = data_blocks[0].data

            _, pads = plt.subplots()
            pads.imshow(pixels)
            plt.show()

    except IOError:
        print "File not found :", inputFilePath
        return 1

    try:
        with open(outputFilePath, 'w') as outputFile:
            header = data_blocks[0].header
            outputFile.write('cd1_1: %.10f, cd1_2: %.10f, cd2_1: %.10f, cd2_2: %.10f' \
                     % (header['CD1_1'], header['CD1_2'], header['CD2_1'], header['CD2_2']))

    except IOError:
        print "File not found :", outputFilePath
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
