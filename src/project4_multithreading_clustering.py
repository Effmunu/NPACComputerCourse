#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import mylib
import threading

# pylint: disable=E1101
# 'numpy' has indeed an 'histogram' member, this error is not relevant

class ClusterFactory(threading.Thread):
    """

    """
    def __init__(self):
        """

        :return:
        """

    def run(self):
        """

        :return:
        """
        ... = mylib.explore_cluster(...)

class LockContext(threading.Lock):
    """

    """
    def __init__(self):
        """

        :return:
        """



def main():
    """

    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/specific.fits"

    # open file and retrieve data
    header, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)

    # apply the fit (no need for the amplitude (first parameter))
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)

    # We define the threshold at 6 standard deviations above the mean bkg value
    threshold = background + (6.0 * dispersion)

    



    return 0

if __name__ == '__main__':
    sys.exit(main())
