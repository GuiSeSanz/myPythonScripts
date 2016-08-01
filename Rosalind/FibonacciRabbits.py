# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:03:10 2016

@author: guillermo
"""

def rabbitPairs(numMonths, numOffspring):
    if numMonths == 1: 
        return 1;
    
    elif numMonths == 2:
        return numOffspring;
    
    oneGen = rabbitPairs(numMonths -1, numOffspring);
    twoGen = rabbitPairs(numMonths -2, numOffspring);
    if numMonths <= 4 :
        return oneGen + twoGen
    
    return (oneGen + (twoGen * numOffspring));


rabbitPairs(35, 5)