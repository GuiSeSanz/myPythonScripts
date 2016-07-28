# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:03:37 2016

@author: guillermo
"""
def ReadFile(inputfile):
    
    infile = open(inputfile, "r")
    mylist = []
    TAB = '\t'
    name = ""
    for line in infile:
       if line.startswith(">"):
           name = line[1:-1]
           print name
       else:
           
           splitedline=' '.join(line.split()).split(' ')
           newline = splitedline[0] + TAB + name + TAB + splitedline[1] + \
           TAB + splitedline[2] + TAB + splitedline[3]
           mylist.append(newline)
           
    infile.close()
    
    return mylist
    
def PrintNewFile(inputfile ,mylist):
    outfile = inputfile + "input_to_multiextract"
    out = open(outfile, 'w') 
    for line in mylist:
        out.write(line + '\n')
    out.close()
    return


if __name__ == "__main__":
    inputfile = "/home/guillermo/Escritorio/PruebaGlimmer/Prueba1/multiiterated.predict"
    mylist = ReadFile(inputfile) 
    PrintNewFile(inputfile ,mylist)