# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:19:05 2016

@author: guillermo
"""
import os
import numpy as np

def formatFasta(inpath):
     infile = open(inpath, 'r')
     outfile = open("modifiedFasta.tmp", 'w')
     for line in infile:
         if line.startswith('>'):
             outfile.write('\n')
             outfile.write(line)
         else:
             line = line.replace("\n", "")
             outfile.write(line)
     infile.close()
     outfile.close()
     return


def createMatrix():
    infile = open("modifiedFasta.tmp", 'r')
    matrix = []
    row = 4
    for line in infile:
        if line=='\n': continue
        if (matrix == []) and (not line.startswith('>')):
            col = len(line[:-1])
            for f in range(row):
                matrix.append( [0] * col)
        if not line.startswith('>'):
            for char in range(len(line)):
                if line[char] == 'A':
                    matrix[0][char] +=1
                if line[char] == 'C':
                    matrix[1][char] +=1
                if line[char] == 'G':
                    matrix[2][char] +=1
                if line[char] == 'T':
                    matrix[3][char] +=1
    infile.close()
   
    return matrix


def calculate_consensus(matrix):
    sequence = []
    array = np.array(matrix,dtype=int)
    maxList = array.max(axis=0)
    for i in range(len(maxList)):
        if maxList[i] == array[0][i]:
            sequence.append('A')
            continue
        if maxList[i] == array[1][i]:
            sequence.append('C')
            continue
        if maxList[i] == array[2][i]:
            sequence.append('G')
            continue
        if maxList[i] == array[3][i]:
            sequence.append('T')
            continue
    return sequence

def printable(matrix, sequence):
    print "".join(sequence)
    aaList = ['A', 'C', 'G', 'T']
    for i in range(len(matrix)):
        print  aaList[i]+':', ' '.join(map(str, matrix[i]))
    return
    
    
    
if __name__ == '__main__':
    inputFile = "matrix.txt"
    inputFile = "rosalind_cons4.txt"
    inpath = os.path.abspath(inputFile)
    formatFasta(inpath)
    matrix = createMatrix()
    sequence = calculate_consensus(matrix)
    printable(matrix, sequence)