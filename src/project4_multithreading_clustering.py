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
    def __init__(self, lock_pixels_visited, pixels_visited, pixels, row, col, threshold):
        """

        :return:
        """
        threading.Thread.__init__(self)
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
            # if already tested
            if self.pixels_visited[row, col]:
#####                if >thershold
#####                    self.joined clusters.apend(num)
                return []
            if self.pixels[row, col] < self.threshold:
                self.pixels_visited[row, col] = 1  # this pixel has been tested
                return []
            # else:
            self.pixels_visited[row, col] = 1  # this pixel has been tested
        return [(row, col)] + \
               self.explore_cluster(row, col-1) + \
               self.explore_cluster(row+1, col) + \
               self.explore_cluster(row, col+1) + \
               self.explore_cluster(row-1, col)

    def run(self):
        """

        :return:
        """
        self.sub_cluster = self.explore_cluster(self.row, self.col)

#class LockContext(threading.Lock):
#    """
#
#    """
#    def __init__(self):
#        """
#
#        :return:
#        """





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


    # We define an array of pixels visited: 1 if visited, 0 elsewise
    pixels_visited = np.zeros_like(pixels)
    cluster_list = []
    thread_list = []
    lock_pixels_visited = threading.RLock()

    # WARNING : pixels[row, col]: row corresponds to y and col to x
    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            if pixels_visited[row, col]:
                continue # If pixel visited, go to next pixel (next step of the loop)
            if pixels[row, col] < threshold:
                with lock_pixels_visited:
                    pixels_visited[row, col] = 1 # visited
            else: # start a new thread
                new_thread = ClusterFactory(lock_pixels_visited, pixels_visited,
                                            pixels, row, col, threshold)
                thread_list.append(new_thread)
                new_thread.start()

    for thread in thread_list:
        thread.join() # we wait for te threads to finish
        cluster_list += thread.sub_cluster

    cluster_list.sort()
    print cluster_list

    # TODO: Add flag to pixels_visited: 'id' of thread that has visited it first.
    # Add flag for termination of explore_cluster: 'out', 'done', 'below', '<id>' (id of another thread)




    return 0

if __name__ == '__main__':
    sys.exit(main())
