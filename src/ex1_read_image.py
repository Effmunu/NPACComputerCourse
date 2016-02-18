#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading and displaying a FITS file
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import matplotlib.pyplot as plt
import mylib

def main():
    """
    Reading and displaying a FITS file
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex1.txt"

    # open file and retrieve data
    header, pixels = mylib.open_fits(input_file_path)

    # plot
    _, pads = plt.subplots()
    pads.imshow(pixels)
    plt.show()

    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('cd1_1: %.10f, cd1_2: %.10f, cd2_1: %.10f, cd2_2: %.10f' \
                     % (header['CD1_1'], header['CD1_2'], header['CD2_1'], header['CD2_2']))

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
