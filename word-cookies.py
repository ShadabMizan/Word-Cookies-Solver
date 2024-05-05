import time
import cv2

import Load
import Find
import Words
import Draw

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','Y','Z'] # Letters that we have.

def main():
    print("Loading Assets...")
    templates = Load.loadTemplates(letters)
    Dictionary = Load.loadTexts(letters)
    nextButton = cv2.imread('Assets/Templates/Next.png', 0)

    playing = True
    n = 0
    while playing:
        startTime = time.time()
        playAgain = False
        play(templates, Dictionary)
        print("Waiting for End Screen...")
        startTimeEnd = time.time()
        while Draw.nextRound(nextButton) == False:
            if time.time() - startTimeEnd > 7.0:
                playAgain = True
                break
            time.sleep(0.05)
        
        if playAgain == True:
            Draw.shuffle()
        else:
            print("Time to Complete Level: {:.3f} seconds".format(time.time() - startTime))
            n += 1
        
        if n > 20:
            break
        
        time.sleep(2)
    

    print("Deleting Temporary Files...")
    Load.deleteTempFiles()


def play(templates, Dictionary):
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




if __name__ == "__main__":
    main()