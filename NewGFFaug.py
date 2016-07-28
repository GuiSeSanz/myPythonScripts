# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 17:15:33 2016

@author: guillermo
"""
import argparse


def NewGFF(inputfile):
    infile =  open(inputfile, "r");    
    outputfile = "NewGFF.gff";
    out = open(outputfile, "w");
    for line in infile:
        if not line.startswith("#"):
            splitedLine = line.split("\t");
            newGFFline = splitedLine[0] + ":" + splitedLine[3] + \
            "-" +splitedLine[4] ;
            out.write(newGFFline);
            out.write("\n");
    return

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Split a FASTA file on diferent FASTAs.')
    parser.add_argument('INfile', help='Input FASTA file', type=str)
    #inputfile = "/home/guillermo/Escritorio/Scripts/Pruebas/GFF.gff"
    args = parser.parse_args()
    inputfile = args.File
    NewGFF(inputfile)
