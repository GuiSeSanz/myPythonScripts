# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 13:53:51 2016

@author: guillermo
"""

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
class Feature(object):
    __metaclass__ = IterRegistry
    _registry = []
    def __init__(self, ID, feature, start, end):
        self.ID = ID
        self.feature = feature
        self.start = int(start)
        self.end = int(end)
        
def ReadGff(inputfile):
    infile = open(inputfile, 'r')
    featureList = []
    for line in infile:
        splitedLine = line.split('\t')
        featureList.append(Feature(splitedLine[0], splitedLine[2], splitedLine[3], splitedLine[4]))
    infile.close()
    return featureList
    
def meanLength(featureList):
    lengthList = []
    for feature in featureList:
        length = feature.end - feature.start
        lengthList.append(length)
    avg=0
    for i in lengthList:
        avg=avg+i
    avg = avg/len(lengthList)
    print avg
    return

if __name__=='__main__':
    inputfile = "/home/guillermo/Escritorio/Genefinding/PruebaAgustus/Augustus_hints/Goathints.gff"
    featureList = ReadGff(inputfile)
    meanLength(featureList)