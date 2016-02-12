#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading and displaying a FITS file
"""

import sys
import matplotlib.pyplot as plt
from astropy.io import fits

if __name__ == '__main__':
    inputFilePath = "/Users/npac09/PycharmProjects/npac09/data/common.fits"
    try:
        data_blocks = fits.open(inputFilePath)

    except IOError:
#        pixels = None
        print "File not found :", inputFilePath
        sys.exit(1)

    data_blocks.info()
    header, data = data_blocks[0], data_blocks[1]

    print type(data)


    sys.exit(0)
