#!/usr/bin/env python
# #-*- coding:utf-8 -*-

"""
This module defines the cluster class
"""

class Cluster:
    """
    This class is used to gather basic information on a cluster found :
    :attribute pixel_list: the list of pixels (doublet of integers)
    :attribute centroid: the position of the centroid (doublet of integer)
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
        self.centroid = (0, 0)
        self.centroid_value = 0.
        self.integral = 0.

        for (i, j) in pixel_list:
            self.pixel_list.append((i, j))  # deep copy of the input pixel list in the object pixel list
            self.integral += pixels[i, j]   # compute the integral of the cluster
            if pixels[i, j] > self.centroid_value:  # find the centroid and its value (max pixel value)
                self.centroid = (i, j)
                self.centroid_value = pixels[i, j]
