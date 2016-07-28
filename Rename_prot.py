# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:39:09 2016

@author: guillermo
"""
import sys

def LeerProt(archivoprot):
    infile = open(archivoprot, "r")
    lista = []
    sequence = False
    for line in infile:        
        if (line.startswith("# protein sequence of predicted genes")):
            sequence = True
            continue
        if (sequence):
            line=line.replace('\t', ' ' )
            lista.extend(line[:-1].split())
    infile.close()
    return lista
    
def ReescribirProt(lista, cabecera):
    ID = 0
    for i in xrange(len(lista)):
        if '>' in lista[i]:
            ID += 1
            lista[i] = '>' + str(cabecera) + '_prot_' + str(ID)
    
    archivo = cabecera + '.faa'
    outfile = open(archivo, "w")
    for i in xrange(len(lista)):
        outfile.write(lista[i]+'\n')
    print archivo, " succesfully created!!"
    outfile.close()  
    return      

def LeerGff3(archivogff3):
     infile = open(archivogff3, "r")
     header =[]
     listacoord = []
     coord = False
     for line in infile:  
         if(coord == False):
             header.append(line)  
         if (line.startswith("##sequence-region")):
             coord = True
             continue
         if(coord):
            #line=line.replace('\t', ' ' )
            listacoord.append(line) 
   
     infile.close()
     return (header, listacoord)

def Reescribirgff3(cabecera, header, listacoord):
    archivo = cabecera + 'bis.gff'
    outfile = open(archivo, "w")
    for i in xrange(len(header)):
        outfile.write(header[i])
        
        
        
    ID=0
        
    for i in xrange(len(listacoord)):
        if ("\tgene" in listacoord[i]):
            ID +=1
            listacoord[i]=listacoord[i].split("\t")
            listacoord[i][0] = cabecera+'_prot_'+str(ID)
            
        else:
              listacoord[i]=listacoord[i].split("\t")
              listacoord[i][0] = cabecera+'_prot_'+str(ID)
             
             
        listacoord[i]= ("\t").join(listacoord[i])
        outfile.write(listacoord[i])
    print archivo, " succesfully created!!"
    outfile.close()  
    return             
             
if __name__ == "__main__":
    
    #archivoprot='Salidach3prot'
    archivogff3='A.thaliana_chr3.gff'
    cabecera='A.thaliana_ch3'    
    #archivo = sys.argv[1]  
    #archivogff3 =  sys.argv[2]
    #cabecera = sys.argv[3] 
    #lista = LeerProt(archivoprot)
    #ReescribirProt(lista, cabecera)
    header, listacoord = LeerGff3(archivogff3)
    Reescribirgff3(cabecera, header, listacoord)
    
