#!/usr/bin/env python
# #-*- coding:utf-8 -*-

"""
This module defines the cluster class
"""

import library

class Cluster:
    """
    This class is used to gather basic information on a cluster found :
    :attribute pixel_list: the list of pixels (doublet of integers)
    :attribute centroid: the position of the centroid (doublet of floats)
    :attribute centroid_wcs: the position of the centroid in WCS coordinates (doublet of floats)
    :attribute integral: total luminosity of the cluster
    :attributes xmin, xmax, ymin, ymax: coordinates of the cluster's bounding box (floats)
    """

    def __init__(self, pixel_list, pixels, header):
        """
        standard constructor of a cluster
        :param pixel_list: list of pixel in the cluster
        :param pixels: original image to look in
        """
        self.pixel_list = []
        self.integral = 0.
        # Initialization of the coordinates (centroid and bounding box)
        # with the first pixel (WARNING : we get (x,y) by taking (row, col))
        self.box_ymin, self.box_xmin = pixel_list[0]
        self.box_ymax, self.box_xmax = pixel_list[0]
        self.centroid = pixel_list[0]

        # WARNING : again, row corresponds to x, col to y
        for (row, col) in pixel_list:
            self.pixel_list.append((row, col))  # deep copy
            self.integral += pixels[row, col]   # compute the integral of the cluster
            # Check if the new pixel enlarges the bounding box
            if col > self.box_xmax:
                self.box_xmax = col
            elif col < self.box_xmin:
                self.box_xmin = col
            if row > self.box_ymax:
                self.box_ymax = row
            elif row < self.box_ymin:
                self.box_ymin = row

        # find the centroid
        self.centroid = (self.box_xmax + self.box_xmin) / 2., \
                        (self.box_ymax + self.box_ymin) / 2.

        # create a WCS object
        my_wcs = library.WCS(header)
        # convert to WCS coordinates
        self.centroid_wcs = my_wcs.convert_to_radec(self.centroid[0], self.centroid[1])
