# -*- coding: utf-8 -*-
"""
Program written by Guillermo Serrano.
v 1.0_11/04/16
"""
import sys

def Leergff3(archivo):
    #leemos el archivo gff y le damos formato
    archivo = archivo +'.gff'
    infile = open(archivo, "r")
    lista = []
    for line in infile:
        line=line.replace('\t', ' ' )
        lista.append(line[:-1].split())
    infile.close()
    
    listaprov=[]
    feature=[]
    if '>' in lista[3][3]:
            feature.insert(0, lista[3][3:])
    padentro = False
    for i in xrange(len(lista)):
        if (padentro) and ('gene' in lista[i]):
            padentro = False
            feature.append(listaprov)
            listaprov=[]
        if 'gene' in lista[i]:
            padentro = True
        if padentro:
            listaprov.append(lista[i])
    return feature



def EscribirTBL(feature, archivo):
    #strand->[x][x][6]
    #Pos->[x][x][3-4]
    #feature->[x][x][2]
####QUALIFYERS THAT MAY BE ADDED WITH THE ANNOTATION TO THE CDS SECTION#########
    prot = 'ATPasa'
    protcode = 'SP'
    protID = 'gln|Guillelab|atg_' #used for protein tracking gnl|dbname|string 
    #where db name is the code of our lab, and string the unique name for the prot
    transID = 'gln|Guillelab|mrna.atg_' #same as the protID, but for the transcript
    #written with mrna, because must be unique
    ECnumber = 'EC 5.99.1.3' #Number of the enzime by the consortium
    #can be added the: go_component, go_process, go_function
    GOcomp = 'This is a celullar component|00056985|IEA' 
    GOproc = 'This is a celullar proccess|00066985|IEA'
    GOfunc = 'This is a celullar function|00076985|IEA'
################################################################################
    Revcoord=[] #para guardar las coordenadas de los CDS en la reverse strand
    table = []  #esto será el .tbl que imprimiremos
    newfeature = [] #esto es lo que iremos añadiendo
    #cabecera del .tbl que contiene el ID 
    feature[0][0]=feature[0][0][1:] 
    SeqID='_'.join(feature[0])
    newfeature.extend(['>feature '+SeqID])
    table.append(''.join(newfeature))
    newfeature = []
    for i in xrange(1, len(feature)):
        for j in xrange(len(feature[i])):
            #print 'feature[%i][%i][%i]' %(i, j, k)
            #añadimos la región en función de la strand
            #añadimos el tipo de feature gene, mRNA, CDS...
            if feature[i][j][2] != 'Intron':
                if feature[i][j][6] == '+':
                    newfeature.append(feature[i][j][3])
                    newfeature.append(feature[i][j][4])
                    newfeature.append(feature[i][j][2])
                    table.append('\t'.join(newfeature))
                    newfeature = []
                elif feature[i][j][6] == '-':
                    newfeature.append(feature[i][j][4])
                    newfeature.append(feature[i][j][3])
                    newfeature.append(feature[i][j][2])
                    table.append('\t'.join(newfeature))
                    if feature[i][j][2] == 'CDS':
                        Revcoord.append(len(table)-1)                        
                    newfeature = []
                if feature[i][j][2] == 'gene':
                    #se le añade el nombre funcional del gen
                    newfeature.extend(['\t\t\tgene', '\tSP' + str(i), '\n'])
                    #se le añade el codigo funcional del gen (3 letras 5 cifras)
                    newfeature.extend(['\t\t\tlocus_tag', '\tatg_' + str(i)]) 
                    table.append(''.join(newfeature))
                    newfeature = []
                if feature[i][j][2] == 'mRNA':
                    newfeature.extend(['\t\t\tproduct', '\t', prot + str(i), '\n'])
                    newfeature.extend(['\t\t\ttranscript_id', '\t',transID + str(i) ])
                    table.append(''.join(newfeature))
                    newfeature = []
                
                #añadir values al CDS
                try:
                    if feature[i][j+2][2] == 'CDS':
                        continue
                except:
                    if feature[i][j][2] == 'CDS':
                        newfeature.extend(['\t\t\tproduct','\t' ,prot, '\n'])
                        newfeature.extend(['\t\t\tproduct','\t' , protcode + str(i), '\n'])
                        newfeature.extend(['\t\t\tprotein_id','\t' , protID + str(i), '\n'])
                        newfeature.extend(['\t\t\ttranscript_id', '\t', transID + str(i), '\n'])
                        newfeature.extend(['\t\t\tEC_number', '\t', ECnumber, '\n'])
                        newfeature.extend(['\t\t\tgo_component', '\t', GOcomp, '\n'])
                        newfeature.extend(['\t\t\tgo_process', '\t', GOproc, '\n'])
                        newfeature.extend(['\t\t\tgo_function', '\t', GOfunc, '\n'])
                        newfeature.extend(['\t\t\tcodon_start','\t0'])#, feature[i][j][7]])
                        table.append(''.join(newfeature))
                        newfeature = []   
    #reescribimos los CDS en la reverse strand
    provisional = []
    coord = []
    for i in xrange(len(Revcoord)):
        try:
            if Revcoord[i] - Revcoord[i+1] == -1:
                provisional.append(Revcoord[i])    
            elif (Revcoord[i] - Revcoord[i-1] == 1) and (Revcoord[i] -Revcoord[i+1] !=1) :
                provisional.append(Revcoord[i])
                coord.append(provisional)
                provisional= []
        except:
            continue
    for i in xrange(len(coord)):
        izda = int(coord[i][0])
        dcha = int(coord[i][-1])
        new = table[izda:dcha+1]
        new.reverse()
        for j in range(len(coord[i])):
            table[coord[i][j]] =  new[j]
    #eliminar los CDS de las lineas de coordenadas, dejando la primera                    
    for i in reversed(range(len(table))):
        try:
            if ('CDS' in table[i]) and ('CDS'in table[i+1]) :
                table[i+1] = table[i+1][:-3]
        except:
            continue
    archivo = archivo + '.tbl'
    outfile = open(archivo, "w")
    for i in xrange(len(table)):
        outfile.write(table[i]+'\n')
    outfile.close()           
    return archivo
                
if __name__ == "__main__":
    #archivo = "Pombefeatures"
    archivo = sys.argv[1]
    feature = Leergff3(archivo)
    table = EscribirTBL(feature, 'Spombe')