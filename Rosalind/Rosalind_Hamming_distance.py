# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 10:25:08 2016

@author: guillermo
"""
import os

def SeqReader(inputPath):
    infile = open(inputPath, 'r')
    seqList = []
    for line in infile:
        seqList.append(line)
    return seqList

def Hamming(seqList):
    Hamming = 0
    for i in xrange(len(seqList[0])):
        if seqList[0][i] != seqList[1][i]:
            Hamming += 1
    print Hamming
    return
    
if __name__ == '__main__':
    inputfile = "rosalind_hamm.txt"
    inputPath = os.path.abspath(inputfile)
    Hamming(SeqReader(inputPath))