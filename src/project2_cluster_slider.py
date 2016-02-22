"""
Reads a FITS image
Display it with a slider controlling the background level to be removed
Now also compute the clusters
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import numpy as np
import mylib
import matplotlib.pyplot as plt
import matplotlib.widgets as widg

def event_handler(pads, header, pixels, thresh_slider):
    """
    Event handler
    :param fig: the canvas to draw into
    :param pads: the pad to plot the image
    :param header: header of the FITS image to display
    :param pixels: The image to display
    :param thresh_slider: threshold slider
    :return:
    """

    def update(event):
        """
        Action on slider change
        :param event: the event
        :return:
        """
        pads.cla()
        cluster_list, _ = mylib.find_clusters(header, pixels, thresh_slider.val)
        mask = np.zeros_like(pixels)
        # we only want to display pixels above threshold belonging to a cluster
        for cluster in cluster_list:
            for (row, col) in cluster.pixel_list:
                mask[row, col] = 1
        # proposed solution to refresh data
#        pads.set_data(pixels * mask)
        pads.imshow(pixels * mask) # to use otherwise
        # display the number of clusters found
        text_id = pads.text(0, 0, "Number of cluster found : %i" % len(cluster_list),
                            fontsize=14, color='white')
#        text_id.remove()

    thresh_slider.on_changed(update)


def main():
    """
    Display it with a slider controlling the background level to be removed.
    Compute the number of clusters found by adjusting the background
    """

    input_file_path = "/Users/npac09/PycharmProjects/npac09/data/common.fits"

    # open file and retrieve data
    header, pixels = mylib.open_fits(input_file_path)

    # creation of the histogram from the data
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(pixels.ravel(), bin_number)

    # apply the fit, only needed to compute the initial value of the slider
    _, background, dispersion = mylib.gaussian_fit(bin_boundaries[:-1], bin_values)
    threshold = 6.0 * dispersion # may remove this line, not needed

    # plot
    _, pads = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    pads.imshow(pixels)
    # pad containing the slider : left, bot, width, height
    pad_slider = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg='white')
    thr_slider = widg.Slider(pad_slider, "Threshold", 0, np.max(pixels), valinit=background)

    event_handler(pads, header, pixels, thr_slider)

    # display
    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
