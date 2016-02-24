#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading a FITS file and finding the clusters in the image, after background removal.
We use multithreading to accelerate the cluster exploration.
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import threading
import numpy as np
import mylib
import Cluster

# pylint: disable=E1101
# 'numpy' has indeed an 'histogram' member, this error is not relevant

class ClusterFactory(threading.Thread):
    """

    """
    def __init__(self, thr_id, lock_pixels_visited, pixels_visited, pixels, row, col, threshold):
        """

        :return:
        """
        threading.Thread.__init__(self)

        self.thr_id = thr_id
        self.threads_encountered = []

        self.sub_cluster = []
        self.lock_pixels_visited = lock_pixels_visited
        self.pixels_visited = pixels_visited
        self.pixels = pixels
        # initial values
        self.row = row
        self.col = col

        self.threshold = threshold

    def explore_cluster(self, row, col):
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
        if row < 0 or row >= len(self.pixels) \
                or col < 0 or col >= len(self.pixels[0]):
            return []
        with self.lock_pixels_visited:
            pixel_value = self.pixels_visited[row, col]
            # if already tested
            if not pixel_value: # already visited and below thr
                return []
            if pixel_value > 0: # if already visited by another thread
                self.add_to_list(pixel_value) # add thread id to encountered list
                return []
            if self.pixels[row, col] < self.threshold:
                self.pixels_visited[row, col] = 0  # this pixel has been tested and is below thr
                return []
            # else:
            self.pixels_visited[row, col] = self.thr_id  # this pixel has been tested by this thread
        return [(row, col)] + \
               self.explore_cluster(row, col-1) + \
               self.explore_cluster(row+1, col) + \
               self.explore_cluster(row, col+1) + \
               self.explore_cluster(row-1, col)

    def add_to_list(self, identity):
        """
        Add thread_id to the list of encountered threads if not already in.
        :param identity: thread id to add
        :return:
        """
        if not identity in self.threads_encountered:
            self.threads_encountered.append(identity)

    def run(self):
        """

        :return:
        """
        self.sub_cluster = self.explore_cluster(self.row, self.col)


def find_cluster(header, pixels, threshold):
    # We define an array of pixels visited: -1 if not visited,
    # 0 if under threshold, <id> if visited by thread <id>
    pixels_visited = - np.ones_like(pixels)
    cluster_list = []
    thread_list = []
    lock_pixels_visited = threading.RLock()

    # Initialize thread id's
    thr_id = 1

    # WARNING : pixels[row, col]: row corresponds to y and col to x
    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            if pixels_visited[row, col] >= 0:
                continue # If pixel visited, go to next pixel (next step of the loop)
            if pixels[row, col] < threshold:
                with lock_pixels_visited:
                    pixels_visited[row, col] = 0 # under thr
            else: # start a new thread
                new_thread = ClusterFactory(thr_id, lock_pixels_visited, pixels_visited,
                                            pixels, row, col, threshold)
                thr_id += 1 # increase the thread id number
                thread_list.append(new_thread)
                new_thread.start()
    # return the list of Cluster objects created by the merge function
    for thread in thread_list: # we wait for te threads to finish before merging
        thread.join()
    return merge_sub_clusters(thread_list, pixels, header)

def merge_sub_clusters(thread_list, pixels, header):
    """
    Merge sub_clusters into real clusters and create Cluster objects
    :param thread_list: list of threads launched by find_cluster
    :return: list of Cluster object of the image
    """
    merged_pixel_list = [] # contains doublets (pixels list, corresponding tread id's merged in this list)

    # .....

    # create the cluster_list
    cluster_list = []
    for (pixel_list, _) in merged_pixel_list:
        cluster_list.append(Cluster.Cluster(pixel_list, pixels, header))
    return cluster_list

def main():
    """
    Reading a FITS file and finding the clusters in the image, after background removal.
    We use multithreading to accelerate the cluster exploration.
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

    cluster_list = find_cluster(header, pixels, threshold)

    print cluster_list

    return 0

if __name__ == '__main__':
    sys.exit(main())
