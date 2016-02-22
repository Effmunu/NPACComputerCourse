#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reads a FITS image
Display it with a slider controlling the background level to be removed
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
import matplotlib.widgets as widg
import matplotlib.pyplot as plt
import mylib

# pylint: disable=E1101
# 'numpy' has indeed an 'histogram' member, this error is not relevant

# pylint: disable=W0613
# 'update' has to have 'event' as an argument

def event_handler(pads, pixels, thresh_slider, dispersion):
    """
    Event handler
    :param pads: the pad to draw into
    :param pixels: The image to display
    :param thresh_slider: threshold slider
    :return:
    """

    def update(event):
        """
        Action on slider change
        :param event: the event
        :return:
        """
        pads.cla()
        mask = pixels >= thresh_slider.val
#        text_id = pads.text(50, 50,
#                            "%d sigma" % (thresh_slider.val / dispersion),
#                            fontsize=14, color='white')
        pads.imshow(pixels * mask)
#        text_id.remove()

    thresh_slider.on_changed(update)

def main():
    """
    Display it with a slider controlling the background level to be removed
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"

    # open file and retrieve data
    _, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)

    # apply the fit
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)
    threshold = 6.0 * dispersion # may remove this line, not needed : just help for next exo

    # plot
    _, pads = plt.subplots()
    # Add margins to gain space for the slider
    plt.subplots_adjust(left=0.25, bottom=0.25)
    pads.imshow(pixels)
    # pad containing the slider : left, bot, width, height
    pad_slider = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg='white')
    # Default value for slider: bkg + thr = bkg + 6 sigma
    thr_slider = widg.Slider(pad_slider, "Threshold", 0, np.max(pixels), valinit=background + threshold)

    event_handler(pads, pixels, thr_slider, dispersion)

    # display
    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
