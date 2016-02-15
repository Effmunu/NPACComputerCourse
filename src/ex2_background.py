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
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from astropy.io import fits

def gaussian(x, max, mean, sigma):
    """
    compute a gaussian function:
    """
    return max * np.exp(- (x - mean) * (x - mean) / (2 * sigma * sigma))

def main():
    """
    Reading a FITS file and determining the background parameters.
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"
    output_file_path = "/Users/npac09/PycharmProjects/npac09/src/ex2.txt"

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
    bin_lower_boudaries = bin_boundaries[:-1]

    # normalize the distribution for the gaussian fit
    my = np.float(np.max(bin_values))
    normal_y = bin_values/my
    mx = np.float(np.max(bin_boundaries))
    normal_x = bin_lower_boudaries/mx

    # apply the fit
    fit, covariant = curve_fit(gaussian, normal_x, normal_y)

    # get back the un-normalized data
    maxvalue = fit[0] * my
    background = fit[1] * mx
    dispersion = fit[2] * mx

    # visualization of the histogram and the fit
    _, pads = plt.subplots(1,3) # 1: image before bkg removal; 2: image after bkg removal; 3: histogram and fit
    pads[2].plot(bin_lower_boudaries, bin_values, 'b+:', label='data')
    pads[2].plot(bin_lower_boudaries, gaussian(bin_lower_boudaries, maxvalue, background, dispersion), 'r.:', label='fit')
    pads[2].legend()
    pads[2].set_title('Flux distribution')
    pads[2].set_xlabel('Amplitude')
    pads[2].set_ylabel('Frequency')

    # background removal
    mask = pixels >= background + 5 * dispersion # 2D-array of booleans, 'True' if value is above background
    pixels_bkg_sub = mask * pixels

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
