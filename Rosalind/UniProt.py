# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:16:00 2016

@author: guillermo
"""

import urllib


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
class Acces(object):
    __metaclass__ = IterRegistry
    _registry = []
    
    def __init__(self, ID):
        self._registry.append(self)
        self.ID = ID
        self.header = ''
        self.fasta = ''
        self.motifs =[]


def ListIds(inputfile):
    infile = open(inputfile, 'r')
    IdList = []
    for line in infile:
        IdList.append(line[:-1])
    return IdList
    
def retrieveFromUniprot(IdList):
    for Id in IdList:
        print Id
        newentry = Acces(Id)
        data = urllib.urlopen("http://www.uniprot.org/uniprot/" + Id + ".fasta").read()
        data = data.split("\n")
        newentry.header = data[0]
        newentry.fasta = "".join(data[1:-1])
    print "==========================================================="
    return
    
def retrieveMotifs(seq):
    sitesList = []
    for i in range(len(seq)):
        if (seq[i]=='N') and (seq[i+1] != 'P') and ((seq[i+2]== 'S')  or
        (seq[i+2]== 'T')) and (seq[i+3] != 'P'):
            sitesList.append(i)
    return sitesList
    
def retrieveMotifsFromUni(Acces):
    for Id in Acces:
        sitesList = retrieveMotifs(Id.fasta)
        for site in sitesList:
            Id.motifs.append(site+1)
    return
    
def print2Rosalind(Acces):
    for Id in Acces: 
        if len(Id.motifs)>0:
            print Id.ID
            print ' '.join(map(str, Id.motifs))
    return
    
if __name__ == '__main__':
#==============================================================================
#     seq = """MFTFLKIILWLFSLALASAININDITFSNLEITPLTANKQPDQGWTATFDFSIADASSIREGDE
#     FTLSMPHVYRIKLLNSSQTATISLADGTEAFKCYVSQQAAYLYENTTFTCTAQNDLSSYNTIDGSITFSLNFS
#     DGGSSYEYELENAKFFKSGPMLVKLGNQMSDVVNFDPAAFTENVFHSGRSTGYGSFESYHLGMYCPNGYFLGG
#     TEKIDYDSSNNNVDLDCSSVQVYSSNDFNDWWFPQSYNDTNADVTCFGSNLWITLDEKLYDGEMLWVNALQSL
#     PANVNTIDHALEFQYTCLDTIANTTYATQFSTTREFIVYQGRNLGTASAKSSFISTTTTDLTSINTSAYSTGS
#     ISTVETGNRTTSEVISHVVTTSTKLSPTATTSLTIAQTSIYSTDSNITVGTDIHTTSEVISDVETISRETAST
#     VVAAPTSTTGWTGAMNTYISQFTSSSFATINSTPIISSSAVFETSDASIVNVHTENITNTAAVPSEEPTFVNA
#     TRNSLNSFCSSKQPSSPSSYTSSPLVSSLSVSKTLLSTSFTPSVPTSNTYIKTKNTGYFEHTALTTSSVGLNS
#     FSETAVSSQGTKIDTFLVSSLIAYPSSASGSQLSGIQQNFTSTSLMISTYEGKASIFFSAELGSIIFLLLSYL
#     LF"""
#==============================================================================
    inputfile = "IDlist.txt"
    a = ListIds(inputfile)
    retrieveFromUniprot(a)
    retrieveMotifsFromUni(Acces)
    print2Rosalind(Acces)
#==============================================================================
#     Id = "B5ZC00"
#     data = urllib.urlopen("http://www.uniprot.org/uniprot/" + Id + ".fasta").read()
#==============================================================================
