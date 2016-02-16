#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Personal functions
"""

from astropy.io import fits
from scipy.optimize import curve_fit
import numpy as np
import library

##########
### For exercice 2
##########
def gaussian(x, amplitude, mean, sigma):
    """
    compute a gaussian function:
    """
    return amplitude * np.exp(- (x - mean) * (x - mean) / (2 * sigma * sigma))

def fit(fitting_function, xdata, ydata):
    """
    Fit a set of data with a function f.
    :param f: fitting function
    :param xdata: bin boundaries values
    :param ydata: bin contents (values)
    :return:    The fit parameters array 'fit_param',
                the covariant matrix 'covariant',
                and the normalization parameters 'm_x' and 'm_y'.
    """

    m_x = np.float(np.max(xdata))
    m_y = np.float(np.max(ydata))

    # apply the fit, we normalize the data to help the fitting program
    fit_param, covariant = curve_fit(fitting_function, \
                       xdata / m_x, \
                       ydata / m_y)

    return fit_param, covariant, m_x, m_y

##########
### For exercice 3
##########
def find_cluster(pixels_visited, pixels, x, y, threshold):
    """
    The image is assumed to be a matrix
    with first coordinate going from top to bottom
    and second coordinate going from right to left

    :param pixels_visited: boolean matrix of visited pixels (1 = visited)
    :param pixels: original image matrix
    :param x: x coordinate of the seed to begin the search
    :param y: y coordinate of the seed to begin the search
    :param threshold: detection threshold, usually "mean + 6*sigma"
    :return: the list of pixels in the cluster
    """

    # boundary conditions
    if x < 0 or x >= len(pixels) \
            or y < 0 or y >= len(pixels[0]):
        return []
    # if already tested
    elif pixels_visited[x, y]:
        return []
    elif pixels[x, y] < threshold:
        pixels_visited[x, y] = 1  # this pixel has been tested
        return []
    else:
        pixels_visited[x, y] = 1  # this pixel has been tested
        return [(x, y)] + find_cluster(pixels_visited, pixels, x, y+1, threshold) + \
               find_cluster(pixels_visited, pixels, x-1, y, threshold) + \
               find_cluster(pixels_visited, pixels, x, y-1, threshold) + \
               find_cluster(pixels_visited, pixels, x+1, y, threshold)


if __name__ == '__main__':

    # test_Simbad
    objects = library.get_objects(1.0, 1.0, 0.1)
    for object in objects:
        print '%s (%s)' % (object, objects[object])
    if len(objects) != 14:
        print 'error'

    # test_WCS

    header = None
    try:
        with fits.open('../data/dss.19.59.54.3+09.59.20.9 10x10.fits') as data_fits:
            try:
                data_fits.verify('silentfix')
                header = data_fits[0].header
            except ValueError as err:
                logging.error('Error: %s', err)
    except EnvironmentError as err:
        logging.error('Cannot open the data fits file. - %s', err)

    w = library.WCS(header)
    ra, dec = w.convert_to_radec(0, 0)

    print ra, dec

    if abs(ra - 300.060983768) > 1e-5:
        print 'error'

    if abs(dec - 9.90624639801) > 1e5:
        print 'error'
