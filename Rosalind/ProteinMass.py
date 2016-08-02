# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:23:11 2016

@author: guillermo
"""


import os

def Readfile(inputPath):
    infile = open(inputPath, 'r')
    aaSeq = []
    for line in infile:
        aaSeq.extend(line[:-1])
    infile.close()
    return aaSeq

def CalculateWeigth(aaSeq):
    weigth={
    'A' :  71.03711,
    'C' :  103.00919,
    'D' :  115.02694,
    'E' : 129.04259,
    'F' :  147.06841,
    'G' :  57.02146,
    'H' :  137.05891,
    'I' :  113.08406,
    'K' :  128.09496,
    'L' :  113.08406,
    'M' :  131.04049,
    'N' :  114.04293,
    'P' :  97.05276,
    'Q' :  128.05858,
    'R' :  156.10111,
    'S' :  87.03203,
    'T' :  101.04768,
    'V' :  99.06841,
    'W' : 186.07931,
    'Y' :  163.06333 }
    
    totalMass= 0
    for aa in aaSeq:
        totalMass += weigth[aa]
    print totalMass
    return


if __name__ == '__main__':
    print 'Hello'
    inputfile = 'rosalind_prtm.txt'
    inputPath = os.path.abspath(inputfile)
    aaSeq = Readfile(inputPath)
    CalculateWeigth(aaSeq)