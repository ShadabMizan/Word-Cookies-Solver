# Words.py contains functions that deal with generating words given some letters
from itertools import permutations

def findWords(lettersFound, Dictionary):
    wordsFound = []
    letters = []
    # Fill letters with the letters that we have in the game. If a letter shows up twice, this will also account for that
    for l, data in lettersFound.items():
        numl = len(data[1])
        for n in range(0,numl):
            letters.append(l)

    maxWordLength = len(letters)
    # Iterate through every letter we have, and go through all 3,4,5, etc. letter combinations we can make.
    for letter in letters:
        for wordLength in Dictionary[letter]:
            if wordLength > maxWordLength: # Do not search 5 letter words if we only are given 4 letters        
                break

            for word in Dictionary[letter][wordLength]: # Ex. go through every 3 letter word for 'E'
                found = True
                tempLetters = letters.copy()
                for i in range(0,len(word)):
                    if word[i].upper() not in tempLetters: # Found a letter that is not in our word bank
                        found = False
                        break
                    tempLetters.remove(word[i].upper()) # Removing so that we can deal with if there are more than one occurance of a letter
                if found:
                    wordsFound.append(word.upper()) 

    wordsFound = list(set(wordsFound))
    return wordsFound

def guessWords(lettersDict, wordsLeft, bigrams, trigrams):
    letters = []

    trigramPerms = []
    bigramPerms = []
    # Extract letters from the lettersDict
    for l, data in lettersDict.items():
        numl = len(data[1])
        for n in range(0,numl):
            letters.append(l)

    # Figure out if we can make any trigrams
    trigramsFound = []
    for trigram in trigrams:
        found = True
        tempLetters = letters.copy()
        for i in range(0, 3):
            if trigram[i].upper() not in tempLetters:
                found = False
                break
            tempLetters.remove(trigram[i].upper())
        
        if found:
            trigramsFound.append(trigram.upper())

    # Check Bigrams
    bigramsFound = []
    for bigram in bigrams:
        found = True
        tempLetters = letters.copy()
        for i in range(0, 2):
            if bigram[i].upper() not in tempLetters:
                found = False
                break
            tempLetters.remove(bigram[i].upper())
        
        if found:
            bigramsFound.append(bigram.upper())
    
    # At this point, we have a list of popular trigrams and bigrams for the letters we have. 
    # Next is to test all permutations of the remaining letters and the ngrams for the letter sizes we are missing.
    # wordsLeft contains an array like [5, 3, 3] i.e missing a 5 letter word and 2 3 letter words. 
    # Therefore look for all 5 letter permutations with the ngrams.
    for wordSize in wordsLeft: 
        for trigram in trigramsFound:
            letterComb = [trigram]
            for i in range(0, len(letters)):
                if letters[i] not in trigram:
                    letterComb.append(letters[i])

            # At this point, letterComb would have a list containing the trigram and the remaining letters
            perms = permutations(letterComb, wordSize)
            for phrase in perms:
                phrase = ''.join(phrase)
                if len(phrase) == wordSize:
                    trigramPerms.append(phrase)
            
        for bigram in bigramsFound:
            letterComb = [bigram]
            for i in range(0, len(letters)):
                if letters[i] not in bigram:
                    letterComb.append(letters[i])

            perms = permutations(letterComb, wordSize)
            for phrase in perms:
                phrase = ''.join(phrase)
                if len(phrase) == wordSize:
                    bigramPerms.append(phrase)
    
    return trigramPerms, bigramPerms

        
    


