# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:35:53 2016

@author: guillermo
"""
from __future__ import division
import os

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
        
        
        
class Seq(object):
    __metaclass__ = IterRegistry
    _registry = []
    
    def __init__(self, ID):
        self.ID = ID
        self.sequence = ''
    def setGC(self, GC):
        self.setGC = GC


def fastaReader(filepath):
    infile = open(filepath, "r")
    SeqList = []
    Id = ''
    
    for line in infile:
        if line.startswith(">"):
            if Id != line[:-1]:
                
                Id = line[1:-1]
                newSeq = Seq(Id) 
                SeqList.append(newSeq)
            else:
                Id = line[:-1]
        else:
            newSeq.sequence = newSeq.sequence + line[:-1]
    
    return SeqList

def calculateGC(SeqList):
    for seq in SeqList:
        GC = ((seq.sequence.count('G') + seq.sequence.count('C')) / len(seq.sequence)) * 100
        seq.setGC = GC
    return

def Compare(SeqList):
    maxID = ''
    maxGC = 0
    for seq in SeqList:
        if seq.setGC > maxGC:
            maxGC = seq.setGC
            maxID = seq.ID
    print maxID
    print maxGC
    return

if __name__ == "__main__":
    inputfile = "rosalind_gc (1).txt"
    filepath = os.path.abspath(inputfile)
    SeqList = fastaReader(filepath)
    calculateGC(SeqList)
    Compare(SeqList)