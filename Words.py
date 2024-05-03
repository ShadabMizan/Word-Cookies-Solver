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
            if wordLength > maxWordLength: # I.e. do not search 5 letter words if we only are given 4 letters        
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
    guesses = []

    ngrams = []
    for trigram in trigrams:
        ngrams.append(trigram.upper())

    for bigram in bigrams:
        ngrams.append(bigram.upper())

    # Extract letters from the lettersDict
    for l, data in lettersDict.items():
        numl = len(data[1])
        for n in range(0,numl):
            letters.append(l)

    # Figure out if we can make any trigrams
    for ngram in ngrams:
        found = True
        tempLetters = letters.copy()
        for i in range(0, len(ngram)):
            if ngram[i] not in tempLetters:
                found = False
                break
            tempLetters.remove(ngram[i])
        
        if found:
            # Since we found a suitible trigram, now we need to generate word guesses based around it.
            # Here is a parts array, containing the trigram and the remaining letters we guess places around.
            parts = [ngram]
            for l in letters:
                if l not in ngram:
                    parts.append(l)
            
            # Of course, we need to take into account the length of the word we are working with.
            for wordLength in wordsLeft:
                # len(trigram) is obviously 3, and n represents the number of entries we need to have a permutation of. So, the remaining letters plus 1, or the ngram itself
                n = wordLength - len(ngram) + 1
                perms = list(set(permutations(parts, n)))
                for perm in perms:
                    perm = ''.join(perm)
                    guesses.append(perm)
                    
    return guesses




    


        
    


