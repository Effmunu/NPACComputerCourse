#!/usr/bin/env python
# #-*- coding:utf-8 -*-

"""
This module defines the cluster class
"""

class Cluster:
    """
    This class is used to gather basic information on a cluster found :
    :attribute pixel_list: the list of pixels (doublet of integers)
    :attribute centroid: the position of the centroid (doublet of floats)
    :attribute centroid_value: the pixel value at of the centroid pixel (float)
    :attribute integral: total luminosity of the cluster
    """

    def __init__(self, pixel_list, pixels):
        """
        standard constructor of a cluster
        :param pixel_list: list of pixel in the cluster
        :param pixels: original image to look in
        """
        self.pixel_list = []
        self.integral = 0.
        # Initialization of the coordinates (centroid and bounding box)
        # with the first pixel
        self.box_xmin, self.box_ymin = pixel_list[0]
        self.box_xmax, self.box_ymax = pixel_list[0]
        self.centroid = pixel_list[0]

        for (x, y) in pixel_list:
            self.pixel_list.append((x, y))  # deep copy of the input pixel list in the object pixel list
            self.integral += pixels[x, y]   # compute the integral of the cluster
            # Check if the new pixel enlarges the bounding box
            if x > self.box_xmax:
                self.box_xmax = x
            elif x < self.box_xmin:
                self.box_xmin = x
            if y > self.box_ymax:
                self.box_ymax = y
            elif y < self.box_ymin:
                self.box_ymin = y

        # find the centroid
        self.centroid = (self.box_xmax + self.box_xmin) / 2., \
                        (self.box_ymax + self.box_ymin) / 2.
