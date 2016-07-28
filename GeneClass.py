# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 10:11:12 2016

@author: guillermo
"""



class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
class Gene(object):
    __metaclass__ = IterRegistry
    _registry = []
    
    def __init__(self, ID, organism = "unknown", genename= "unknown", protein= "unknown", length= 0, moltype= "unknown"):
        self._registry.append(self)
        self.ID = ID
        self.organism = organism
        self.genename = genename
        self.protein = protein
        self.length = length
        self.moltype = moltype
        self.taxonomy = []
        self.taxID = ""
        self.lineageid = []
        
    def setnotes(self, notes=""):
        self.notes = notes
        
    def Name(self, name):
        self.name = str(name)
    
    def addTaxonomy(self, taxa):
        self.taxonomy.append(taxa)
        
    def addlineageid(self, lineageid):
        self.lineageid.append(lineageid)
    