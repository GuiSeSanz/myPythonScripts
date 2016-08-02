# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:34:25 2016

@author: guillermo
"""

def createWords( alphabet, wordLen ):
    alphabet = list(alphabet)
    alphabet = filter(lambda a: a != ' ', alphabet)
    
    
    word=''
    
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            word = alphabet[i]+alphabet[j]
            print word
            
    return


if __name__=='__main__':
    alphabet = 'T A G C'
    wordLen = 2
    createWords( alphabet, wordLen )