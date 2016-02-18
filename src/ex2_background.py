#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading a FITS file and determining the background parameters.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import mylib


def main():
    """
    Reading a FITS file and determining the background parameters.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex2.txt"

    # open file and retrieve data
    _, pixels = mylib.open_fits(input_file_path)

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

    # visualization of the histogram and the fit
    _, pads = plt.subplots(1, 3)
        # 1: image before bkg removal; # 2: image after bkg removal; 3: histogram and fit
    pads[2].plot(bin_lower_boundaries, bin_values, 'b+:', label='data')
    pads[2].plot(bin_lower_boundaries, \
                 mylib.gaussian(bin_lower_boundaries, maxvalue, background, dispersion), \
                 'r.:', label='fit')
    pads[2].legend()
    pads[2].set_title('Flux distribution')
    pads[2].set_xlabel('Amplitude')
    pads[2].set_ylabel('Frequency')

    # background removal
    mask = pixels >= background + 6.0 * dispersion
        # 2D-array of booleans, 'True' if value is above bkg
    pixels_bkg_sub = mask * (pixels - background)

    # visualization of the image before and after bkg removal
    pads[0].imshow(pixels)
    pads[1].imshow(pixels_bkg_sub)

    plt.show()


    # write result to output file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write('background: %d, dispersion: %d' % (int(background), int(dispersion)))

    except IOError:
        print "File not found :", output_file_path
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
