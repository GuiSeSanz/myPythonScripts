#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:19:07 2016

@author: guillermo
"""


import sys
from time import sleep

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# 
# Sample Usage
# 


# make a list
items = list(range(0, 100))
i = 0
l = len(items)

# Initial call to print 0% progress
printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
for item in items:
    # Do stuff...
    sleep(0.1)
    # Update Progress Bar
    i += 1
    printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)