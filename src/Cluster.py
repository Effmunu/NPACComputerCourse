#!/usr/bin/env python
# #-*- coding:utf-8 -*-

"""
This module defines the cluster class
"""

class Cluster:
    """
    This class is used to gather basic information on a cluster found :
    pixel_list : the list of pixels (doublet of integers)
    centroid : the position of the centroid (doublet of integer)
    centroid_value : the pixel value at of the centroid pixel (float)
    integral : total luminosity of the cluster
    """

#    def __init__(self):
#        """
#        default constructor, gives negative values to the centroid
#        """
#        self.pixel_list = []
#        self.centroid = (-1, -1)
#        self.centroid_value = -1
#        self.integral = -1

    def __init__(self, pixel_list, pixels):
        """
        standard constructor of a cluster
        """
        self.pixel_list = []    # if there is a deep_copy function, take it
        self.centroid = (0, 0)
        self.centroid_value = 0.
        self.integral = 0.

        for (i, j) in pixel_list:
            self.pixel_list.append((i, j))
            self.integral += pixels[i, j]
            if pixels[i, j] > self.centroid_value:
                self.centroid = (i, j)
                self.centroid_value = pixels[i, j]
