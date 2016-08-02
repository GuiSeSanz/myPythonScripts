# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:51:02 2016

@author: guillermo
"""
import os
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio import SeqIO


def ReadFile(inputPath):
    DNAseq = ''
    IntronList = []
    for seq_record in SeqIO.parse(inputPath, "fasta"):
        IntronList.append(str(seq_record.seq))
        if len(seq_record.seq) > len(DNAseq):
            DNAseq = str(seq_record.seq)
    IntronList.remove(DNAseq)
    return DNAseq, IntronList

def Splicing(DNAseq, IntronList):
    for intron in IntronList:
        DNAseq = DNAseq.replace(intron,"")
    return DNAseq

def Translate(DNAseq):
    coding_dna = Seq(DNAseq, IUPAC.unambiguous_dna)
    Protein = coding_dna.translate()
    print Protein[:-1]
    return

if __name__=='__main__':
    inputfile = 'RNAsplicing.txt'
    inputPath = os.path.abspath(inputfile)
    DNAseq, IntronList = ReadFile(inputPath)
    DNAseq = Splicing(DNAseq, IntronList)
    Translate(DNAseq)