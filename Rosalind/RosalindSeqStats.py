# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:07:55 2016

@author: guillermo
"""

from __future__ import division
import re
from Bio.Seq import Seq

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
class Sequence(object):
    __metaclass__ = IterRegistry
    _registry = []
    
    def __init__(self, DNAfasta):
       self.DNAfasta = DNAfasta
       self.Seqlength = int(len(DNAfasta))
       self.Acontent = ""
       self.Ccontent = ""
       self.Gcontent = ""
       self.Tcontent = ""
       self.GCpercent = ""
       self.fastaID = ""
       self.ReverseDNA = ""
       self.ReversecComplementaryDNA = ""
       self.RNAfasta = ""
       self.ReverseRNA = ""
       self.ReverseComplementaryRNA = ""
       
def seq_composition(SequenceObject):
    Acontent = int(SequenceObject.DNAfasta.count('A'))
    Ccontent = int(SequenceObject.DNAfasta.count('C'))
    Gcontent = int(SequenceObject.DNAfasta.count('G'))
    Tcontent = int(SequenceObject.DNAfasta.count('T'))
    SequenceObject.Acontent = Acontent
    SequenceObject.Ccontent = Ccontent
    SequenceObject.Gcontent = Gcontent
    SequenceObject.Tcontent = Tcontent
    return 
    
def seq_GCpercent(SequenceObject):
    SequenceObject.GCpercent = ((SequenceObject.Gcontent + \
    SequenceObject.Ccontent) / SequenceObject.Seqlength) * 100
    return
    
def seq_RNAandReverse(SequenceObject):
    SequenceObject.RNAfasta = SequenceObject.DNAfasta.replace("T", "U")
    SequenceObject.ReverseDNA = SequenceObject.DNAfasta[::-1]
    SequenceObject.ReverseRNA = SequenceObject.RNAfasta[::-1]
    return

def Complementary(SequenceObject):
    listDNA = list(SequenceObject.DNAfasta)
    listRNA = list(SequenceObject.RNAfasta)
    for i in range(len(listRNA)):
        if listDNA[i] == 'A':
            listDNA[i] = 'T'
            listRNA[i] = 'T'
            continue
        if listDNA[i] == 'C':
            listDNA[i] = 'G'
            listRNA[i] = 'G'
            continue
        if listDNA[i] == 'G':
            listDNA[i] = 'C'
            listRNA[i] = 'C'
            continue
        if listDNA[i] == 'T':
            listDNA[i] = 'A'
            continue
        if listRNA[i] == 'U':
            listRNA[i] = 'T'
            continue
    SequenceObject.ReversecComplementaryDNA = "".join(listDNA)[::-1]
    SequenceObject.ReverseComplementaryRNA = "".join(listRNA)[::-1]

    return    
    
def tranlatemRNA(SequenceObject):
    myseq = Seq(SequenceObject.DNAfasta)
    print myseq.translate()
    return    
    
def calculateStats(DNA):
    SEQUENCE = Sequence(DNA)
    seq_composition(SEQUENCE)
    seq_GCpercent(SEQUENCE)
    seq_RNAandReverse(SEQUENCE)
    Complementary(SEQUENCE)
    tranlatemRNA(SEQUENCE)
    return SEQUENCE


    
if __name__ == "__main__":
    seq = "GATATATGCATATACTT"
    my_sequence = calculateStats(seq)
    attributes = vars(my_sequence)
    for item in attributes.items():
        print "%s: %s" % item
    
    


