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

    inputFilePath = "/Users/npac09/PycharmProjects/npac09/data/common.fits"

    try:
        with fits.open(inputFilePath) as data_blocks:
            data_blocks.info()

            pixels = data_blocks[0].data

            fig, pads = plt.subplots()
            imgplot = pads.imshow(pixels)
            plt.show()

            return 0

    except IOError:
        print "File not found :", inputFilePath
        return 1

if __name__ == '__main__':
    sys.exit(main())
