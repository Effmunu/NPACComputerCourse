#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Opens a graphical application to select a file
:Author: LAL npac09 <laudrain@ipno.in2p3.fr>
:Date:   February 2016
"""

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.widgets as widg

class Application(object):
    """
    Graphical application to select a file
    """
    def __init__(self, path):
        """
        Initializes the application to the path given in argument
        :param path: initial path to run the file selector
        :return:
        """
        self.path = path
        self.selected_file = ""

        _, self.pads = plt.subplots(2)
        self.display_current() # Display function

        plt.show()

    def display_current(self):
        """
        Displays the current directory
        """
        # retrieves the informations on the current dir (only one iteration of for loop)
        dirpath, dirnames, filenames = "", [], []
        for dirpath, dirnames, filenames in os.walk(self.path):
            break
        if self.path != "/":
            dirnames.insert(0, "..") # We have to add '..' by hand

        # display
        self.pads[0].set_title("Files in %s" % os.path.abspath(dirpath))
        self.pads[1].set_title("Directories in %s" % os.path.abspath(dirpath))
        self.radio_file = widg.RadioButtons(self.pads[0], filenames) # Files buttons
        self.radio_dir = widg.RadioButtons(self.pads[1], dirnames) # Dir buttons
        # we must redefine the action each time since we create a new object
        self.radio_file.on_clicked(self.select_file)
        self.radio_dir.on_clicked(self.select_dir)

    def select_file(self, label):
        """
        Action to undertake if a file has been selected:
        record the selected file and quit the application.
        :param label: label of the selected item in the RadioButton
        :return:
        """
        self.selected_file = os.path.abspath(self.path) + "/" + label
        plt.close() # Quit the plotting area, thus the application

    def select_dir(self, label):
        """
        Action to undertake if a directory has been selected:
        move to that directory and display the updated infos.
        :param label: label of the selected item in the RadioButton
        :return:
        """
        self.path += "/"
        self.path += label
        self.pads[0].cla() # clear pads
        self.pads[1].cla() # clear pads
        self.display_current() # Display function
        plt.draw() # Redraw new directory files and directories



def main():
    """
    Lauches the application and checks its results
    """
    app = Application(".")

    if app.selected_file == "":
        print "No file selected"
    else:
        print "File selected:", app.selected_file

    return 0

if __name__ == '__main__':
    sys.exit(main())
