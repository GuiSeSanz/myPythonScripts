 #!/usr/bin/python2.7

import argparse

def Splitting(inputfile, numLines):
    infile =  open(inputfile, "r");    
    lineCounter = 0;   
    header = "";
    filecounter = 0;
    
    outputfile = "Fastaseq_" + str(filecounter) + ".fsa";
    out = open(outputfile, "w")
    for line in infile:
        lineCounter += 1;        
        if line.startswith(">"):
            header = line.replace(" ", "").replace("\n", ""); 
            Header = header + "_fragment_" + str(filecounter) + "\n";
            out.write(Header)
        elif lineCounter < numLines:
            out.write(line);
        if lineCounter == numLines:
            lineCounter = 0;
            out.close
            filecounter += 1;
            outputfile = "Fastaseq_" + str(filecounter) + ".fsa";
            out = open(outputfile, "w");
            Header = header + "_fragment_" + str(filecounter) + "\n";
            out.write(Header)
    return

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Split a FASTA file on diferent FASTAs.')
    parser.add_argument('File', help='Input FASTA file', type=str)
    parser.add_argument('Numlines', help='The number of lines per file', type=int, default='100000' )
    #inputfile = "/home/guillermo/Escritorio/Scripts/Nueva carpeta/Apismelidera.fasta"
    #numLines = 100000  
    args = parser.parse_args()
    inputfile = args.File
    numLines = args.Numlines
    #numLines = int(sys.argv[2])
    #print inputfile, numLines
    Splitting(inputfile, numLines)
