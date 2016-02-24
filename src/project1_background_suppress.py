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
# the 'update' function MUST have the 'event' argument

def event_handler(pixels, background, dispersion):
    """
    Event handler
    :param pads: the pad to draw into
    :param pixels: The image to display
    :param thresh_slider: threshold slider
    :return:
    """

    # plot zone
    fig, pads = plt.subplots()

    # Add margins to gain space for the slider
    plt.subplots_adjust(left=0.25, bottom=0.25)

    # Plot the image a first time with no threshold (0)
    pads.imshow(mylib.remove_background(pixels, background, 0))

    # pad containing the slider : left, bot, width, height
    pad_slider = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg='white')

    # Default value for slider: 0
    # Minimal value: 0
    # Maximal value: max value in 'pixels' - background
    thresh_slider = widg.Slider(pad_slider, "Threshold", 0,
                                np.max(pixels) - background, valinit=0)

    def update(event):
        """
        Action on slider change
        :param event: the event
        :return:
        """
        # clear the previous image
        pads.cla()
        # Display the number of sigmas above threshold selected with the slider
        plt.title("pixels above background + %d sigma" \
                  % (thresh_slider.val / dispersion))
        # Display the image with selected background removed
        # (we remove 'thresh_slider.val', with a threshold = 'thresh_slider.val - background'
        pads.imshow(mylib.remove_background(pixels,
                                            background,
                                            thresh_slider.val))
        # Draw the image
        fig.canvas.draw()

    thresh_slider.on_changed(update)

def main():
    """
    Display the FITS image with a slider controlling the background level to be removed
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"

    # open file and retrieve data
    _, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)

    # apply the fit
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)

    # Call the event handler
    event_handler(pixels, background, dispersion)

    # display
    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
