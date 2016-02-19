#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Personal functions
"""

from astropy.io import fits
from scipy.optimize import curve_fit
import numpy as np
import library
import Cluster

##########
### For exercice 1
##########
def open_fits(input_file_path):
    """
    Open a FITS file and retrieve the header and the data of the first block.
    :param input_file_path: FITS file path to be opened
    :return: header, data of the first block [0]
    """
    try:
        with fits.open(input_file_path) as data_blocks:
            data_blocks.info()
            return data_blocks[0].header, data_blocks[0].data

    except IOError:
        print "File not found :", input_file_path
        return 1

##########
### For exercice 2
##########
def gaussian(x, amplitude, mean, sigma):
    """
    compute a gaussian function:
    """
    return amplitude * np.exp(- (x - mean) * (x - mean) / (2 * sigma * sigma))

def gaussian_fit(xdata, ydata):
    """
    Fit a set of data with a gaussian function.
    :param xdata: bin boundaries values
    :param ydata: bin contents (values)
    :return:    The fit parameters array 'fit_param',
                and the covariant matrix 'covariant'.
    """

    # normalization parameters
    m_x = np.float(np.max(xdata))
    m_y = np.float(np.max(ydata))

    # apply the fit, normalize the data to help the fitting program (no need for covariant matrix)
    fit_param, _ = curve_fit(gaussian, \
                       xdata / m_x, \
                       ydata / m_y)

    # get back the un-normalized parameters
    amplitude = fit_param[0] * m_y
    background = fit_param[1] * m_x
    dispersion = fit_param[2] * m_x

    return amplitude, background, dispersion

##########
### For exercice 3
##########
def explore_cluster(pixels_visited, pixels, row, col, threshold):
    """
    The image is assumed to be a matrix
    with first coordinate going from top to bottom
    and second coordinate going from right to left

    :param pixels_visited: boolean matrix of visited pixels (1 = visited)
    :param pixels: original image matrix
    :param row: x coordinate of the seed to begin the search
    :param col: y coordinate of the seed to begin the search
    :param threshold: detection threshold, usually "mean + 6*sigma"
    :return: the list of pixels in the cluster
    """

    # boundary conditions
    if row < 0 or row >= len(pixels) \
            or col < 0 or col >= len(pixels[0]):
        return []
    # if already tested
    elif pixels_visited[row, col]:
        return []
    elif pixels[row, col] < threshold:
        pixels_visited[row, col] = 1  # this pixel has been tested
        return []
    else:
        pixels_visited[row, col] = 1  # this pixel has been tested
        return [(row, col)] + explore_cluster(pixels_visited, pixels, row, col-1, threshold) + \
               explore_cluster(pixels_visited, pixels, row+1, col, threshold) + \
               explore_cluster(pixels_visited, pixels, row, col+1, threshold) + \
               explore_cluster(pixels_visited, pixels, row-1, col, threshold) # right, top, left, bottom

def find_clusters(pixels, threshold):
    # We define an array of pixels visited: 1 if visited, 0 elsewise
    pixels_visited = np.zeros_like(pixels)
    clusters_list = []

    # WARNING : pixels[row, col]: row corresponds to x and col to y
    for row in range(len(pixels[0])):
        for col in range(len(pixels)):
            if pixels_visited[row, col]:
                continue # If pixel visited, go to next pixel (next step of the loop)
            if pixels[row, col] < threshold:
                pixels_visited[row, col] = 1 # visited
            else: # add the new cluster to the list
                cluster = Cluster.Cluster(explore_cluster(
                    pixels_visited, pixels, row, col, threshold), pixels)
                clusters_list.append(cluster)
                pixels_visited[row, col] = 1 # visited

    return clusters_list

##########
### For exercice 4
##########
def event_handler(fig, my_wcs, pixels):
    """
    Event handler
    :param fig: the canvas to draw into
    :param my_wcs: The conversion tool for coordinates
    :param pixels: The image to display
    :return:
    """
    def move(event):
        """
        Action on mouse movement
        :param event: the event
        :return:
        """
        if event.xdata >= len(pixels) or event.xdata < 0 \
                or event.ydata >= len(pixels) or event.ydata < 0:
            return
        pads = event.inaxes     #event.inaxes renvoie le pad courant
        text_id = pads.text(event.xdata, event.ydata,
                            "%f, %f" % my_wcs.convert_to_radec(event.xdata, event.ydata),
                            fontsize=14, color='white')
        event.canvas.draw()
        text_id.remove()

    fig.canvas.mpl_connect('motion_notify_event', move)


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
