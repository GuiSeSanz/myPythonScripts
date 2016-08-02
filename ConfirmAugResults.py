# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:50:53 2016

@author: guillermo
"""



def ReadResults(inputfile):
    infile = open(inputfile, 'r')
    results = []
    for line in infile:
        if "# start gene" in line:
            found_gene = line.split(" ")[3]
            results.append(found_gene.split("..")[0])
    infile.close()
    resultNames = set()
    for item in results:
        resultNames.add(item)
        
    return results, resultNames

def countGenes(results, resultNames):
    totalGenes = 0
    for name in resultNames:
        totalGenes += results.count(name)
        print name, results.count(name)
    print "found genes: ", totalGenes
    

        



if __name__=='__main__':
    inputfile = '/home/guillermo/Escritorio/DClass/MoreAugustusthanaugustus/Augustus/data/output/results.txt'
#==============================================================================
   # inputfile ="/home/guillermo/Escritorio/B2GO_Aug_Results/ResultChecekr.txt"
#==============================================================================
    results, resultNames = ReadResults(inputfile)
    countGenes(results, resultNames)