#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Personal functions
"""

# pylint: disable=E1101
# 'numpy' has indeed an 'exp' member, this error is not relevant

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

def remove_background(pixels, background, threshold):
    """
    :param pixels: original image matrix
    :param background: mean value of the gaussian fit on the pixel distribution
    :param threshold:
    :return: an image, similar to 'pixels', with the background removed
    """
    mask = pixels >= background + threshold
    # mask is a 2D-array of booleans, 'True' if value is above bkg
    return mask * (pixels - background)

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
        return [(row, col)] + \
               explore_cluster(pixels_visited, pixels, row, col-1, threshold) + \
               explore_cluster(pixels_visited, pixels, row+1, col, threshold) + \
               explore_cluster(pixels_visited, pixels, row, col+1, threshold) + \
               explore_cluster(pixels_visited, pixels, row-1, col, threshold)

def find_clusters(header, pixels, threshold):
    """
    Find all the clusters in a FITS image, given a threshold
    :param header: header of the FITS image
    :param pixels: original image matrix
    :param threshold:
    :return: list of clusters in the image, dictionary of clusters indexed by centroid coordinates
    """
    # We define an array of pixels visited: 1 if visited, 0 elsewise
    pixels_visited = np.zeros_like(pixels)
    cluster_list = []
    cluster_dico = {}

    # WARNING : pixels[row, col]: row corresponds to x and col to y
    for row in range(len(pixels[0])):
        for col in range(len(pixels)):
            if pixels_visited[row, col]:
                continue # If pixel visited, go to next pixel (next step of the loop)
            if pixels[row, col] < threshold:
                pixels_visited[row, col] = 1 # visited
            else: # add the new cluster to the list and to the dictionary
                cluster = Cluster.Cluster(explore_cluster(
                    pixels_visited, pixels, row, col, threshold), pixels, header)
                cluster_list.append(cluster)
                cluster_dico['%f %f' % cluster.centroid] = cluster
                pixels_visited[row, col] = 1 # visited

    return cluster_list, cluster_dico

def find_max_integral_cluster(cluster_list):
    """
    :param cluster_list: list of cluster objects
    :return: the dictionary key of the cluster with maximal integral
            (string with coordinates of the centroid)
    """
    max_integral = 0
    max_integral_key = ''
    for cluster in cluster_list:
        if cluster.integral > max_integral:
            max_integral = cluster.integral
            max_integral_key = '%f %f' % cluster.centroid
    return max_integral_key

##########
### For exercice 4
##########

# TODO possible upgrade : also display the info 'on_click'

def event_handler(fig, header, pixels):
    """
    Event handler
    :param fig: the canvas to draw into
    :param my_wcs: The conversion tool for coordinates
    :param pixels: The image to display
    :return:
    """
    # create a WCS object to make unit conversions
    my_wcs = library.WCS(header)

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

##########
### For exercice 5
##########

# TODO : possible upgrade : only display the rectangle when the mouse is
# over it, meaning we should connect to mpl in the event handler

def event_handler2(fig, header, pixels, cluster_list, cluster_name_dico):
    """
    Event handler
    :param fig: the canvas to draw into
    :param my_wcs: The conversion tool for coordinates
    :param pixels: The image to display
    :return:
    """
    # create a WCS object to make unit conversions
    my_wcs = library.WCS(header)

    def on_click(event):
        if event.xdata >= len(pixels) or event.xdata < 0 \
                or event.ydata >= len(pixels) or event.ydata < 0:
            # if outside the image
            return

        pads = event.inaxes     # get the current pad

        centroid_to_query = -1, -1
        for cluster in cluster_list:
#            if (event.xdata, event.ydata) in cluster.pixel_list:
            if event.xdata >= cluster.box_xmin and \
                            event.xdata <= cluster.box_xmax and \
                            event.ydata >= cluster.box_ymin and \
                            event.ydata <= cluster.box_ymax:
                centroid_to_query = '%f %f' % (cluster.centroid[0], cluster.centroid[1])
                break   # found the cluster clicked on
        # if we didn't click on a cluster box, just redraw the picture
        if centroid_to_query[0] < 0:
            event.canvas.draw()
            return

        text_id = pads.text(event.xdata, event.ydata, "%f, %f \n%s"
                            % (my_wcs.convert_to_radec(event.xdata, event.ydata)[0],
                               my_wcs.convert_to_radec(event.xdata, event.ydata)[1],
                               cluster_name_dico[centroid_to_query]),
                            fontsize=14, color='white')
        event.canvas.draw()
        text_id.remove()

    fig.canvas.mpl_connect('button_press_event', on_click)
