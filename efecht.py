# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 09:22:50 2016

@author: guillermo
"""

import re
import random as rnd
from Bio import Entrez
from GeneClass import Gene

def CreateIDlist(IDnumber):
    randomList=[]
    for i in xrange(IDnumber):
        randomList.append(rnd.randrange(2222222, 84795111))
    return randomList

idList = CreateIDlist(10)



Entrez.email = "s.serrano.guillermo@gmail.com"
geneList = []
geneCount = 0

for ID in idList:
    name = "gene_" + str(geneCount)
    name2 = "gene_" + str(geneCount)
    name = Gene(ID)
    name.Name = name2
    geneList.append(name)
    geneCount += 1
    
for gene in Gene:
    print gene.ID 
    handle = Entrez.efetch(db="protein", id= gene.ID , rettype="gb", \
    retmode="txt")
    out = handle.read()
#    print(out)
    parseable = out.split("\n")
    taxa = False
    taxonomy = ''
    for line in parseable:
        #organism
        if "ORGANISM" in line:
            line = line.replace("ORGANISM", "")
            organism = line.strip()
            gene.organism = organism
        #taxonomy
            taxa = True
            continue
        
        if (taxa) and (line.split()[0].isupper()):     
            taxa = False
        if  taxa:
            taxonomy = taxonomy + line
            for i in taxonomy.split():
                gene.addTaxonomy(i)
           # gene.Taxonomy =  "".join(taxonomy.split())
            continue
        
        
        #mol_type
        if "/mol_type=" in line:
            line = line.replace("/mol_type=", "").replace("\"", "")
            moltype = line.strip()
            gene.moltype = moltype  
            continue
        #protein    
        if "/product=" in line:
            line = line.replace("/product=", "").replace("\"", "")
            protein = line.strip()
            gene.protein = protein
            continue
        #length    
        if "source   " in line:
            line = line.replace("source", "").replace("1..", "")
            length = line.strip()
            gene.length = int(length)
            continue
        #gene    
        if "/gene=" in line:
            line = line.replace("/gene=", "").replace("\"", "")
            genename = line.strip()
            gene.genename = genename    
            
handle.close()       
    
sort = False
if sort:    
    import operator
    geneList.sort(key=operator.attrgetter('organism'))

#for gene in geneList:
#    print "organism: %s  protein: %s  genename: %s" % (gene.organism, \
#    gene.protein, gene.genename)

#iterates over the list of genes and prints the org
Printtaxons = False
if Printtaxons:
    print "============================================"
    for i in geneList:
        print i.taxonomy
        print "============================================"

#creates a dictionary with Name : geneclass and prints the org
wololo = False
if wololo:
    genes ={}
    for gene in Gene:
        genes[gene.Name]=gene
    for gene in genes:
        print genes[gene].organism
    
    organism = "Drosophila"
    for gene in genes:
        if organism in genes[gene].organism:
            print genes[gene].__dict__
            print "\n"
        

def comapre2taxonomies(taxonomy1, taxonomy2):
    score = 0
    taxonomy1=geneList[0].taxonomy
    taxonomy2=geneList[1].taxonomy
    milength = min(len(geneList[0].taxonomy), len(geneList[1].taxonomy))    
    
    for i in range(milength):
        #print "tax1", taxonomy1[i]
        #print "tax2", taxonomy1[2]
        if taxonomy1[i] == taxonomy2[i]:
            score += 1
    print score 
    return

#comapre2taxonomies(geneList[0].taxonomy, geneList[1].taxonomy)









NCBI = True
if NCBI :
    from ete3 import NCBITaxa
    ncbi = NCBITaxa()
    #ncbi.update_taxonomy_database()
    taxIDlist=[]
    for gene in geneList:
        name2taxID = ncbi.get_name_translator([gene.organism])
        gene.taxID = name2taxID[gene.organism][0]
        for i in ncbi.get_lineage(gene.taxID):
            
            gene.addlineageid(i)
        taxIDlist.append(gene.taxID)
        
    #taxid2name = ncbi.get_taxid_translator([9606, 9443])
    #print taxid2name
tree = True
if tree :    
    tree = ncbi.get_topology(taxIDlist)
    print tree.get_ascii(attributes=["sci_name", "rank"])
    




    
    
    
    
