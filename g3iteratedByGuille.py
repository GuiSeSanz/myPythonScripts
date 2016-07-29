#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:22:25 2016

@author: guillermo
"""
import os



def parseParameters (inputfile):
    infile = open(inputfile, "r")
    runglimmer = ""
    glimmeroptions = ""
    genome = ""
    icmModel = ""
    iterated = False
    parameters={}
    for line in infile:
        parameter = line.split("=")
        key = parameter[0].strip()
        value = parameter[1].replace(' ', '')
        value = value.split("\n")
        value = value[0]
        parameters[key] = value
    infile.close()
    #GLIMMER RUNS
    if (parameters['useICM'] == "true"):
        icmModel =  parameters['icmModel']
        if (parameters['runModel'] == "Single"):
            runglimmer = "SingleICM"
            
        else:
            runglimmer = "IterateICM"
            iterated = True
            
    if (parameters['useICM'] == "false"):
        if (parameters['runModel'] == "Single"):
            runglimmer = "SingleNew"
        else:
            runglimmer = "IterateNew"
            iterated = True
    if(parameters['buildICM'] == "true"):
        runglimmer = "BuildICM"
            
    genome = "/data/input/" + parameters['fastaFile']
    if(iterated):
        glimmeroptions = "-z %s -g %s -o %s -t %s -A %s -Z %s -P %s -C %s" %(parameters['geneticCode'], parameters['setMinLenght'], 
        parameters['maxOverlap'], parameters['minScore'], parameters['startCodons'], parameters['stopCodons'], parameters['startCodonsWeight'], 
        parameters['contentGC'])
    else:
        glimmeroptions = "-z %s -g %s -o %s -t %s" %(parameters['geneticCode'], parameters['setMinLenght'], 
        parameters['maxOverlap'], parameters['minScore'])
        if('contentGC'in parameters) and (parameters['contentGC'] != "Automatic"): glimmeroptions = glimmeroptions + " -C %s" %(parameters['contentGC'])
    if ('genomeShape' in parameters) and (parameters['genomeShape'] != 'Circular'):
        glimmeroptions = glimmeroptions + " -l"
    #reciclo parametros:
    if (runglimmer == "BuildICM"):
        glimmeroptions = "-t %s -z %s -A %s" %(parameters['entropy'], parameters['geneticCode'], parameters['startCodons'])#longorfparam
        icmModel = "-r -p -w -d " %(parameters['entropy'], parameters['width'],  parameters['depth']) #buildicmparam
        if ('frameStop' in parameters) and (parameters['frameStop'] != 'false'):
            icmModel = icmModel + " -F"
        
        #outputDir, fastaFile, startCodons-, geneticCode-, entropy-, width, depth, period,frameStop
    
    return (glimmeroptions, genome, runglimmer, icmModel)


def NEWSingleRun(genome, tag, glimmeroptions):

    numsteps = 5    
    
    print "NEWSingleRun"
    #step1
    # Find long, non-overlapping orfs to use as a training set
    print "Step 1 of %i:  Finding long orfs for training" %(numsteps)
    command = "long-orfs -n -t 1.15 %s %s.longorfs" %(genome, tag)
    os.system(command)
    
    #step2
    print "Step 2 of %i:  Extracting training sequences" %(numsteps)
    command = "extract -t %s  %s.longorfs > %s.train" %(genome, tag, tag)
    os.system(command)    
    
    #step3
    print "Step 3 of %i: Building ICM" %(numsteps)
    command = "build-icm -r %s.icm < %s.train" %(tag, tag)
    os.system(command)
    
    #step4
    print "Step 4 of %i: Running Glimmer3" %(numsteps)
    command = "glimmer3 %s %s %s.icm %s.run1" %(glimmeroptions, genome, tag, tag)
    os.system(command)
    
    #step5
    print "Step 5 of %i: Extract the sequences" %(numsteps)
    command = "grep -c '>' %s" %(genome)
    out=os.popen(command).read()
    
    predictionfile = tag + ".run1.predict" 
   
    if out > 2:
        #multifasta
        mylist = ReadFile(predictionfile)
        PrintNewFile(predictionfile ,mylist)
        outfile = predictionfile + "input_to_multiextract"
        command = "multi-extract -2 %s %s > Results.fasta" %(genome, outfile)
        os.system(command)
        
    else:
        command = "extract -2 %s %s > Results.fasta" %(genome, predictionfile)
        
    return
   
def NEWIteratedRun(genome, tag, glimmeroptions):
 
    print "NEWIteratedRun"
       
    # add/change glimmer options here
    
    numsteps = 9
    
    #step1
    # Find long, non-overlapping orfs to use as a training set
    print "Step 1 of %i:  Finding long orfs for training" %(numsteps)
    command = "long-orfs -n -t 1.15 %s %s.longorfs" %(genome, tag)
    os.system(command)

    
    #step2
    print "Step 2 of %i:  Extracting training sequences" %(numsteps)
    command = "extract -t %s  %s.longorfs > %s.train" %(genome, tag, tag)
    os.system(command)
    
    #step3
    print "Step 3 of %i: Building ICM" %(numsteps)
    command = "build-icm -r %s.icm < %s.train" %(tag, tag)
    os.system(command)
    
    #step4
    print "Step 4 of %i: Running first Glimmer3" %(numsteps)
    command = "glimmer3 %s %s %s.icm %s.run1" %(glimmeroptions, genome, tag, tag)
    os.system(command)
    
    #step5
    print "Step 5 of %i: Getting training coordinates" %(numsteps)
    command = "tail -n +2 %s.run1.predict > %s.coords" %(tag, tag)
    os.system(command)
    
    #step6
    print "Step 6 of %i: Making PWM from upstream regions" %(numsteps)
    command = "awk -f /app/glimmer3.02/scripts/upstream-coords.awk 25 0 %s.coords \
               | extract %s - > %s.upstream" %(tag, genome, tag) 
    os.system(command)
    
    command = "elph %s.upstream LEN=6 | awk -f /app/glimmer3.02/scripts/get-motif-counts.awk > %s.motif" %(tag, tag)
    os.system(command)
    
    #step7
    print "Step 7 of %i: Getting start-codon usage" %(numsteps)
    command = "start-codon-distrib -3 %s %s.coords" %(genome, tag)
    startuse=os.popen(command).read()
    startuse1=startuse[:-2]
    
    
    #step8
    print "Step 8 of %i: Running second Glimmer3" %(numsteps)
    command = "glimmer3 %s -b %s.motif -P %s %s %s.icm %s" %(glimmeroptions, tag, startuse1, genome, tag, tag)
    os.system(command)
    
    #step9
    print "Step 9 of %i: Extract the sequences" %(numsteps)
    command = "grep -c '>' %s" %(genome)
    out=os.popen(command).read()
    
    predictionfile = tag + ".predict" 
   
    if out > 2:
        #multifasta
        mylist = ReadFile(predictionfile)
        PrintNewFile(predictionfile ,mylist)
        outfile = predictionfile + "input_to_multiextract"
        command = "multi-extract -2 %s %s > Results.fasta" %(genome, outfile)
        os.system(command)
    else:
        
        command = "extract -2 %s %s > Results.fasta" %(genome, predictionfile)
    return
    
def CreateICM(genome, tag, glimmeroptions, icmModel):  
    print "CreateICM"

    numsteps = 3    
    
    #step1
    # Find long, non-overlapping orfs to use as a training set
    print "Step 1 of %i:  Finding long orfs for training" %(numsteps)
    command = "long-orfs -n %s %s %s.longorfs" %(glimmeroptions, genome, tag)
    os.system(command)
    
    #step2
    print "Step 2 of %i:  Extracting training sequences" %(numsteps)
    command = "extract -t %s  %s.longorfs > %s.train" %(genome, tag, tag)
    os.system(command)    
    
    #step3
    print "Step 3 of %i: Building ICM" %(numsteps)
    command = "build-icm %s %s.icm < %s.train" %(icmModel, tag, tag)
    os.system(command)
    
    return
    
    
def SingleRunWithICM(genome, tag, icmModel, glimmeroptions):
    print "SingleRunWithICM"
    numsteps = 2 
    
    #step4
    print "Step 1 of %i: Running Glimmer3" %(numsteps)
    command = "glimmer3 %s %s %s %s.run1" %(glimmeroptions, genome, icmModel, tag)
    os.system(command)
    
    print "Step 2 of %i: Extract the sequences" %(numsteps)
    command = "grep -c '>' %s" %(genome)
    out=os.popen(command).read()
    
    predictionfile = tag + ".run1.predict" 
   
    if out > 2:
        #multifasta
        mylist = ReadFile(predictionfile)
        PrintNewFile(predictionfile ,mylist)
        outfile = predictionfile + "input_to_multiextract"
        command = "multi-extract -2 %s %s > Results.fasta" %(genome, outfile)
        os.system(command)
        
    else:
        command = "extract -2 %s %s > Results.fasta" %(genome, predictionfile)
        
    return
    
    
def IteratedRunWithICM(genome, tag, icmModel, glimmeroptions):
    print "IteratedRunWithICM"

    numsteps = 6
    
    #step1
    print "Step 1 of %i: Running first Glimmer3" %(numsteps)
    command = "glimmer3 %s %s %s %s.run1" %(glimmeroptions, genome, icmModel, tag)
    os.system(command)
    
    #step2
    print "Step 2 of %i: Getting training coordinates" %(numsteps)
    command = "tail -n +2 %s.run1.predict > %s.coords" %(tag, tag)
    os.system(command)
    
    #step3
    print "Step 3 of %i: Making PWM from upstream regions" %(numsteps)
    command = "awk -f /app/glimmer3.02/scripts/upstream-coords.awk 25 0 %s.coords \
               | extract %s - > %s.upstream" %(tag, genome, tag) 
    os.system(command)
    
    command = "elph %s.upstream LEN=6 | awk -f /app/glimmer3.02/scripts/get-motif-counts.awk > %s.motif" %(tag, tag)
    os.system(command)
    
    #step4
    print "Step 4 of %i: Getting start-codon usage" %(numsteps)
    command = "start-codon-distrib -3 %s %s.coords" %(genome, tag)
    startuse=os.popen(command).read()
    startuse1=startuse[:-2]
    
    
    #step5
    print "Step 5 of %i: Running second Glimmer3" %(numsteps)
    command = "glimmer3 %s -b %s.motif -P %s %s %s %s" %(glimmeroptions, tag, startuse1, genome, icmModel, tag)
    os.system(command)
    
    #step6
    print "Step 6 of %i: Extract the sequences" %(numsteps)
    command = "grep -c '>' %s" %(genome)
    out=os.popen(command).read()
    
    predictionfile = tag + ".predict" 
   
    if out > 2:
        #multifasta
        mylist = ReadFile(predictionfile)
        PrintNewFile(predictionfile ,mylist)
        outfile = predictionfile + "input_to_multiextract"
        command = "multi-extract -2 %s %s > Results.fasta" %(genome, outfile)
        os.system(command)
    else:
        
        command = "extract -2 %s %s > Results.fasta" %(genome, predictionfile)
        os.system(command)

    return
    return
    
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
   
   
def Copy2Output(tag):
    command = "mv " + tag + ".fasta " + tag + ".predict " + tag + ".detail "+ tag + ".icm " + "/data/output"
    os.system(command)
    return
    
 
    
if __name__ == "__main__":
    inputfile = "/data/parameters.txt"
    #inputfile="/home/guillermo/Escritorio/DClass/glimmerfiles/data/parameters.txt"
    glimmeroptions, genome, runglimmer, icmModel = parseParameters (inputfile) 
    tag = "Results"
    if(runglimmer == 'SingleICM'): SingleRunWithICM(genome, tag, icmModel, glimmeroptions)
    if(runglimmer == ' IterateICM'): IteratedRunWithICM(genome, tag, icmModel, glimmeroptions)
    if(runglimmer == 'SingleNew'): NEWSingleRun(genome, tag, glimmeroptions)
    if(runglimmer == 'IterateNew'): NEWIteratedRun(genome, tag, glimmeroptions)
    if(runglimmer == 'BuildICM'): CreateICM(genome, tag, glimmeroptions, icmModel)
    Copy2Output(tag)
    
   
    
       
    
