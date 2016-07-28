# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 13:01:20 2016

@author: guillermo
"""
import os
os.path.abspath("mydir/myfile.txt")
from ete3 import NCBITaxa
    #ncbi.update_taxonomy_database()

def model_organisms(inputfile):
    ncbi = NCBITaxa()
    infile = open(inputfile, "r")
    modelList = []
    for line in infile:
        modelList.append(line[:-1])
    infile.close()
  
    if modelList[0].isdigit():        
        print "List of model IDs Loaded"
        Type = 'Id'
    else:
        print "List of model names Loaded"
        Type = 'Sp'
    modelIDList = []
    
    if Type == 'Sp':
        name2taxID = ncbi.get_name_translator(modelList)
        for model in modelList:
            modelIDList.append(name2taxID[model][0])
    else:
       modelIDList = modelList 
       
    return modelIDList
    
def AddmyID(modelIDList, ID, filepath):
    ncbi = NCBITaxa()
    if ID.isdigit(): 
        modelIDList.append(int(ID))        
    else:
         name2taxID = ncbi.get_name_translator(ID)
         modelIDList.append(int(name2taxID[ID][0]))
         
    tree = ncbi.get_topology(modelIDList)
    print tree.get_ascii(attributes=["sci_name", "rank"])
    
    outfile = "outTree.txt"
    out = open(outfile, "w") 
    for line in tree.get_ascii(attributes=["sci_name", "rank"]):
        out.write(line)        
    out.close()
    
    return modelIDList


def model2Tree(modelIDList):    
    ncbi = NCBITaxa()        
    tree = ncbi.get_topology(modelIDList)
    print tree.get_ascii(attributes=["sci_name", "rank"])
    
    return
    
if __name__ == "__main__":
    inputfile = "models.txt"
    filepath = os.path.abspath(inputfile)
    modelIDList = model_organisms(filepath) 
    model2Tree(modelIDList)
    ID = '33169'
    AddmyID(modelIDList, ID, filepath)