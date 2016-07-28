# -*- coding: utf-8 -*-

import subprocess as sp
import os

#os.system('rm Results')
original = open("mod.prop", "r") 
invariable = original.read()
          
ECdefault=['AnnotationAlgoParameters.ecIDA=1.0',
'AnnotationAlgoParameters.ecIPI=1.0','AnnotationAlgoParameters.ecIMP=1.0',
'AnnotationAlgoParameters.ecIGI=1.0','AnnotationAlgoParameters.ecIEP=1.0',
'AnnotationAlgoParameters.ecEXP=1.0','AnnotationAlgoParameters.ecISS=0.8',
'AnnotationAlgoParameters.ecISO=0.8','AnnotationAlgoParameters.ecISA=0.8',
'AnnotationAlgoParameters.ecISM=0.8','AnnotationAlgoParameters.ecIGC=0.7',
'AnnotationAlgoParameters.ecIBA=0.8','AnnotationAlgoParameters.ecIBD=0.8',
'AnnotationAlgoParameters.ecIKR=0.8','AnnotationAlgoParameters.ecIRD=0.7',
'AnnotationAlgoParameters.ecRCA=0.8','AnnotationAlgoParameters.ecTAS=0.9',
'AnnotationAlgoParameters.ecNAS=0.8','AnnotationAlgoParameters.ecIC=0.9',
'AnnotationAlgoParameters.ecND=0.5','AnnotationAlgoParameters.ecNR=0.0']

ECvalue1=['AnnotationAlgoParameters.ecIDA=1.0',
'AnnotationAlgoParameters.ecIPI=1.0','AnnotationAlgoParameters.ecIMP=1.0',
'AnnotationAlgoParameters.ecIGI=1.0','AnnotationAlgoParameters.ecIEP=1.0',
'AnnotationAlgoParameters.ecEXP=1.0','AnnotationAlgoParameters.ecISS=1.0',
'AnnotationAlgoParameters.ecISO=1.0','AnnotationAlgoParameters.ecISA=1.0',
'AnnotationAlgoParameters.ecISM=1.0','AnnotationAlgoParameters.ecIGC=1.0',
'AnnotationAlgoParameters.ecIBA=1.0','AnnotationAlgoParameters.ecIBD=1.0',
'AnnotationAlgoParameters.ecIKR=1.0','AnnotationAlgoParameters.ecIRD=1.0',
'AnnotationAlgoParameters.ecRCA=1.0','AnnotationAlgoParameters.ecTAS=1.0',
'AnnotationAlgoParameters.ecNAS=1.0','AnnotationAlgoParameters.ecIC=1.0',
'AnnotationAlgoParameters.ecND=1.0','AnnotationAlgoParameters.ecNR=1.0']       
   
for AC in xrange(60, 100, 2): #(1, 100, 2)
    for GO in xrange(0, 20, 2): #(0, 20)
        for HSP in xrange( 0, 100,10): #(0, 100, 5)
            for IEA in [1 , 0.7, 0.8, 0.9, 0]:
                prop= ['AnnotationAlgoParameters.annotCutOff=', AC, 
                'AnnotationAlgoParameters.goWeight=', GO, 
                'AnnotationAlgoParameters.hspHitCoverageCutoff=', HSP,
                'AnnotationAlgoParameters.ecIEA=', IEA]
                
                archivo = 'AC%sGO%sHSP%sIEA%s' %(AC, GO, HSP, IEA) 
                infile = open(archivo+'.txt', "w")
                infile.write(invariable)
                for i in range(0, len(prop), 2):
                    infile.write(str(prop[i]) + str(prop[i+1]) + '\n')
                if (IEA == 1) or (IEA == 0):
                    EC='default'
                    for i in range(len(ECdefault)):
                        infile.write(ECdefault[i]+ '\n')
                else:
                    EC='value1'
                    for i in range(len(ECvalue1)):
                        infile.write(ECvalue1[i]+ '\n')
                infile.close()
               
                print archivo
                sp.call(['/home/guillermo/blast2go_cli/david_fixed_it/blast2go_cli_v1.2.0/AutomaticAnnotation/blast2go_cli.run',
                         '-useobo', 'go_201603.obo', '-loadb2g', 'rhizobiumaa_Mapping.b2g', 
                         '-annotation', '-savelog', archivo+'.log','-properties', archivo+'.txt']) 
                
                param= "%i'\t' %i'\t' %i'\t' %s'\t' %s'\t' Seq" %(AC, GO, HSP, IEA, EC)
                command='/home/guillermo/blast2go_cli/david_fixed_it/blast2go_cli_v1.2.0/AutomaticAnnotation/Rescatador.sh ' + param
                os.system(command)
                os.system('rm *.txt')
                os.system('rm *.log')
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
