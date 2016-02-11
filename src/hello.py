#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Print message 'Hello, world!'.

:Author: LAL npacxx <npacxx@lal.in2p3.fr>
:Date:   February 2016
"""

import sys

# By convention, a function name must contain only lowercase characters and _.
# string=None defines a default value for string and makes it optional.
def print_msg(string=None):
    """Print a message received as an argument or a default message
    if none is passed.

    :param string: a string to print (optional)
    :return: status value (always success, 0)
    """

    if string is None:
        # Define a default message
        string = 'Hello, world!'
    print "%s" % string
    return 0

def read_msg():
    """Read a message in the std input

    :param
    :return: input string
    """

    return raw_input("Enter sentence : ")

# The following test is considered as a best practice: this way a module
# can be used both as a standalone application or as a module called by another
# module.
if __name__ == "__main__":

    # The main program is implement mainly as a function: this avoids having
    # all the variables used in this context (e.g. string in print_msg) to
    # become global variables.

    msg_list = []
    run=1
    print "type 'exit' to quit"
    while run:
        msg=read_msg()
        if msg=="exit":
            run=0
        else:
            msg_list.append(msg)
    for msg in msg_list:
        status = print_msg(msg)

    sys.exit(status)