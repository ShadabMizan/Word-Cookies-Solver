# Words.py contains functions that deal with generating words given some letters

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