 #!/usr/bin/python2.7
"""
By Guillermo Serrano.

"""

from __future__ import division
import sys
import os

def ModifyFile(inputfile, Nlines):
    infile = open(inputfile, "r")
    filename =  inputfile.split(".")
    outputfile = filename[0] + "_mod2.fastq"
    out = open(outputfile, "w")
    lineNumber = 0
    for line in infile:
        lineNumber+=1
        print (lineNumber/int(Nlines)*100)
        #print str(lineNumber) + '/' + str(Nlines)
        if (line.startswith("@") or (line.startswith("+"))) and (len(line.split(" ")[0])<30):
            line = line.replace (".", "-")
            goodheader = line.split(" ")
            out.write(goodheader[0] + "\n" )
        else:
            out.write(line)
        
    infile.close()
    out.close()
    return
    
    
if __name__ == "__main__":  
    #inputfile = "/home/guillermo/Escritorio/Genefinding/PruebaAgustus/RNAseqBoar/ThirdTrial(separated)/prueba.fastq"
    inputfile = sys.argv[1]
    command = "wc -l %s" %(inputfile)
    lines = os.popen(command).read()
    Nlines = lines.split(" ")[0]
    ModifyFile(inputfile, Nlines)
