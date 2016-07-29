 #!/usr/bin/python2.7
"""
By Guillermo Serrano.

"""

from __future__ import division
import sys
import os
 
        
def fastq2fasta(inputfile, Nline):
    infile = open(inputfile, "r")
    filename =  inputfile.split(".")
    outputfile = filename[0] + "_mod2.fasta"
    out = open(outputfile, "w")
    lineNumber = 0
    lc = 0        
    for line in infile:
        lineNumber+=1
        print (lineNumber/int(Nlines)*100)
        lc += 1
        if lc == 1:
            seqID = line.split(" ")
            out.write(seqID[0].replace("@", ">") + "\n")  
            print (lineNumber/int(Nlines)*100)
            continue
        if lc == 2:
            out.write(line)
            continue
        if lc == 3:
            continue
        if lc == 4:
            lc = 0
            continue
    infile.close()
    out.close()      
    return
    
        
        
if __name__ == "__main__":  
    #inputfile = "/home/guillermo/Escritorio/Genefinding/PruebaAgustus/RNAseq/FirstTrial/prueba.fastq"
    inputfile = sys.argv[1]
    command = "wc -l %s" %(inputfile)
    lines = os.popen(command).read()
    Nlines = lines.split(" ")[0]
    fastq2fasta(inputfile, Nlines)
