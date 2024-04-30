import time
import cv2

import Load
import Find
import Words
import Draw

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','Y'] # Letters that we have.

def main():
    start_time = time.time()
    print("Loading Assets...")
    templates = Load.loadTemplates(letters)
    Dictionary = Load.loadTexts(letters)
    nextButton = cv2.imread('Assets/Templates/Next.png', 0)
    emptySquare = cv2.imread('Assets/Templates/Empty-Square.png', 0)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Grabbing Cookie Pan...")
    cookiePan = Load.loadCookiePan()
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Finding Letters...")
    lettersDict = Find.findLetters(templates, letters, cookiePan, 0.8)
    for letter, data in lettersDict.items():
        print("{}: Vals: {}, Coords: {}".format(letter, data[0], data[1]))
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Finding Words...")
    wordsFound = Words.findWords(lettersDict, Dictionary)
    print(wordsFound)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Drawing Known Words...")
    Draw.drawWords(wordsFound, lettersDict)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Waiting for End Screen...")
    while Draw.nextRound(nextButton) == False:
        time.sleep(0.1)
    print("Elapsed time: ", time.time() - start_time, " seconds")


if __name__ == "__main__":
    main()