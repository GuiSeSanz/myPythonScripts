
import random
import itertools
from sets import Set


TITLE = '''
 _   _                                                  __  ______ _____  ________  ___
| | | |                                                / _| |  _  \  _  ||  _  |  \/  |
| |_| | __ _ _ __   __ _ _ __ ___   __ _ _ __     ___ | |_  | | | | | | || | | | .  . |
|  _  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \   / _ \|  _| | | | | | | || | | | |\/| |
| | | | (_| | | | | (_| | | | | | | (_| | | | | | (_) | |   | |/ /\ \_/ /\ \_/ / |  | |
\_| |_/\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|  \___/|_|   |___/  \___/  \___/\_|  |_/
                    __/ |
                   |___/
'''


def readWords(path):
    with open(path,'r') as f:
        wordList = f.readlines()
    wordList = map(lambda x: str.replace(x, "\n", ""), wordList)
    return wordList

def pickRandomWord(wordList, minWordSize=0):
    word = wordList[random.randint(1, len(wordList))]
    if len(word) < minWordSize:
        word = pickRandomWord(wordList, minWordSize)
    word = word.upper()
    return word

def checkLetter(word, query, letter):
    # letter = letter.upper()
    position = word.find(letter)
    firstAttempt = True
    if (position == -1) and (firstAttempt == True):
        firstAttempt = False
        trailMod = -1
        return query, trailMod
    if position != -1 :
        query = query.split()
        query[word.find(letter)] = letter
        query = ' '.join(query)
        word2 = list(word)
        word2[word.find(letter)] = '@'
        word = ''.join(word2)
        query, trailMod = checkLetter(word, query, letter)
    trailMod = 0
    return query, trailMod

def printQueryAndLetters(query, usedLetters):
    print(query + "\n")
    print('The letters already used are: {0}'.format(', '.join(usedLetters)))
    return

def demandLetter():
    letter = raw_input("Type a letter (a-zA-Z):")
    if not letter.isalpha():
        print("Character not avaliable, please insert a letter (a-zA-Z)")
        letter = demandLetter()
    return letter.upper()

def retrieveDefinition(word):
    link = 'https://en.oxforddictionaries.com/definition/'
    searchLink = link + word.lower()

if __name__ == "__main__":
    print(TITLE)
    path = "/home/guille/Desktop/tmp/words.txt"
    trials = 5
    usedLetters = Set([])
    wordList = readWords(path)
    word = pickRandomWord(wordList, 8)
    query = '_ '*len(word)
    print(query)

    ### Interaction begins
    while trials > 0:
        print('Remaining trials: {0}'.format(trials))
        letter = demandLetter()
        usedLetters.add(letter)
        query, trialMod = checkLetter(word, query, letter)
        trials += trialMod
        printQueryAndLetters(query, usedLetters)
        if word == query.replace(' ', ''):
            print("Congratulations!!!")
            break

    print(word)
