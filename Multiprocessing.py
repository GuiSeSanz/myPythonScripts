# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 13:51:46 2016

@author: guillermo
"""
import time
import multiprocessing
from multiprocessing import Queue
def worker(num):
    """worker function"""
    print 'Worker: ', num
    double = num * 2
    time.sleep(5)
    return double

if __name__ == '__main__':
    
    q = Queue()
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,) )
        
        p.start()
    p.join()
    print 'finished'