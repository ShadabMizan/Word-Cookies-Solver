import time
import cv2

import Load
import Find
import Words
import Draw

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','Y'] # Letters that we have.

def main():
    print("Loading Assets...")
    templates = Load.loadTemplates(letters)
    Dictionary = Load.loadTexts(letters)
    bigrams, trigrams = Load.load_nGrams()
    nextButton = cv2.imread('Assets/Templates/Next.png', 0)
    emptySquare = cv2.imread('Assets/Templates/Empty-Square.png', 0)
    
    play(templates, Dictionary, emptySquare, bigrams, trigrams, nextButton)


def play(templates, Dictionary, emptySquare, bigrams, trigrams, nextButton):
    print("Grabbing Cookie Pan...")
    cookiePan = Load.loadCookiePan()

    print("Finding Letters...")
    lettersDict = Find.findLetters(templates, letters, cookiePan, 0.8)
    for letter, data in lettersDict.items():
        print("{}: Vals: {}, Coords: {}".format(letter, data[0], data[1]))

    print("Finding Words...")
    wordsFound = Words.findWords(lettersDict, Dictionary)
    print(wordsFound)

    print("Drawing Known Words...")
    Draw.drawWords(wordsFound, lettersDict)


    wordsLeft, sqrWidth, sqrHeight = Find.findEmptySquares(emptySquare)
    print(wordsLeft)

    guesses = Words.guessWords(lettersDict, wordsLeft, bigrams, trigrams)
    
    coords = []
    while len(wordsLeft) > 0:
        for i in range(0,len(guesses)):
            # Draw the guess
            guessLength = len(guesses[i])
            Draw.drawAWord(guesses[i], lettersDict)
            time.sleep(0.25)

            # Detect a change
            coords = Find.checkFoundWord(sqrWidth, sqrHeight, i)
            print(coords)

            if len(coords) > 0:
                if len(coords) in wordsLeft:
                    wordsLeft.remove(guessLength)
                    break
            
            

    Load.deleteTempFiles()
        



    # print("Waiting for End Screen...")
    # while Draw.nextRound(nextButton) == False:
    #     time.sleep(0.1)

if __name__ == "__main__":
    main()