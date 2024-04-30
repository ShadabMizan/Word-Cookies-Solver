import pyautogui
import time
import cv2
from PIL import ImageGrab
import numpy as np
import copy

# Borders of the entire playable screen are: (When docked to the left half of the window)
# (310, 64), (1128, 1514)

# Pan area is (310, 810) to (1128, 1514)
x1 = 0
y1 = 0
x2 = 1430
y2 = 1519

def main():
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','Y'] # Letters that we have.
    start_time = time.time()
    print("Loading Assets...")
    templates = loadTemplates(letters)
    Dictionary = loadTexts(letters)
    nextButton = cv2.imread('Assets/Next.png', 0)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Grabbing Cookie Pan...")
    cookiePan = loadCookiePan()
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Finding Letters...")
    lettersDict = findLetters(templates, letters, cookiePan, 0.8)
    for letter, data in lettersDict.items():
        print("{}: Vals: {}, Coords: {}".format(letter, data[0], data[1]))
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Finding Words...")
    wordsFound = findWords(lettersDict, Dictionary)
    print(wordsFound)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Drawing Known Words...")
    drawWords(wordsFound, lettersDict)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    start_time = time.time()
    print("Waiting for End Screen...")
    while nextRound(nextButton) == False:
        time.sleep(0.1)
    print("Elapsed time: ", time.time() - start_time, " seconds")

    

def loadCookiePan():
    # Grab a screenshot of the word-cookies screen.
    cookiePanScreenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    cookiePanScreenshot.save('Assets/cookie-pan.png')

    cookiePan = cv2.imread('Assets/cookie-pan.png', 0)
    return cookiePan

def loadTemplates(letters):
    # Store all the letters that we know in their imread form in a templates array.
    templates = []
    for letter in letters:
        file_path = 'Assets/Templates/{}.png'.format(letter)
        templates.append(cv2.imread(file_path, 0))
    
    return templates

def loadTexts(letters):
    Dictionary = {}
    for letter in letters:
        Dictionary[letter] = {3: [], 4: [], 5: []}  # Initialize sub-dictionary for each letter
        with open('Assets/Texts/{}/three.txt'.format(letter), 'r') as threeTxt:
            words = threeTxt.readlines()
            words = [word.strip() for word in words]  # Remove all \n and spaces
            Dictionary[letter][3].extend(words)  
        with open('Assets/Texts/{}/four.txt'.format(letter), 'r') as fourTxt:
            words = fourTxt.readlines()
            words = [word.strip() for word in words]  
            Dictionary[letter][4].extend(words) 
        with open('Assets/Texts/{}/five.txt'.format(letter), 'r') as fiveTxt:
            words = fiveTxt.readlines()
            words = [word.strip() for word in words]  
            Dictionary[letter][5].extend(words)  
    return Dictionary

def findLetters(templates, letters, img, threshold):

    # Map letters found to their location found
    lettersFound = {} 

    for l in range(0,len(templates)): # l represents the index in the templates array, which is in alphabetical order
        # print("Next Letter... ", letters[i])
        template = templates[l]
        height, width = template.shape

        # Array to store all the unique locations of a letter that is found.
        letterLocs = []
        letterVals = []


        # Need to rotate the template because the letters can spawn in any orientation. Then we need to test all these orientations to see if we get a really good match.
        # [-16,17] step size 8
        for angle in range(-16,17,8):
            # Generate rotation matrix and apply it to the template
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1) 
            rotated_template = cv2.warpAffine(template, rotation_matrix, (width, height))

            # Get the result matrix, holding values of a match at locations
            result = cv2.matchTemplate(img, rotated_template, cv2.TM_CCOEFF_NORMED) 

            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))

            # Map letter matches to their associated values and locations
            letterMatches = {} 

            thr = 25
            letter = letters[l]
            for loc in locations:
                max_val = result[loc[1], loc[0]] # Extract max_val, note (y,x) format of the result matrix
                max_loc = (loc[0] + width/2, loc[1] + height/2) # max_loc is centered at the location found
                
                
                letterLocs.append(max_loc)
                letterVals.append(max_val)

                # Go through every letter location to check for duplicates, or when matches are found close together such that they are essentially the same object
                for i in range(0,len(letterLocs)-1):
                    if abs(letterLocs[-1][0] - letterLocs[i][0]) < thr and abs(letterLocs[-1][1] - letterLocs[i][1]) < thr:
                        # Duplicate found, remove the pair with a lower value
                        if letterVals[i] >= letterVals[-1]:
                            letterVals.pop()
                            letterLocs.pop()
                        elif letterVals[i] < letterVals[-1]:
                            letterVals.pop(i) 
                            letterLocs.pop(i)


            letterMatches[letter] = [letterVals, letterLocs] 
            # Add letters that have been matched to the letters found 
            if letter not in lettersFound and len(letterMatches[letter][0]) != 0:
                lettersFound[letter] = letterMatches.get(letter) 
            elif letter in lettersFound:
                for i in range(0,len(lettersFound.get(letter)[0])):
                    # Check if the letterMatches has a higher value than what we know in lettersFound
                    if letterMatches.get(letter)[0][i] > lettersFound.get(letter)[0][i]:
                        # Change the position and value to the better match
                        lettersFound[letter][0][i] = letterMatches.get(letter)[0][i]
                        lettersFound[letter][1][i] = letterMatches.get(letter)[1][i]
                
    # Next is to compare the letters found to other letters found in roughly the same coords. 
    # This is to compare letters like P and F which are similar, and to see which has a higher value.

    # 1. Find the indices of coordinates that are similar.
    lettersToChange = []
    thr = 25
    for letter1 in list(lettersFound.keys()):
        for letter2 in list(lettersFound.keys()):
            if letter1 == letter2:
                continue

            vals1 = lettersFound[letter1][0]
            coords1 = lettersFound[letter1][1]

            vals2 = lettersFound[letter2][0]
            coords2 = lettersFound[letter2][1]

            for i in range(0, len(coords1)):
                for j in range(0, len(coords2)):
                    if abs(coords1[i][0] - coords2[j][0]) < thr and abs(coords1[i][1] - coords2[j][1]) < thr:
                        if vals1[i] > vals2[j]:
                            # Remove from letter2
                            vals2New = vals2[:j] + vals2[j+1:]
                            coords2New = coords2[:j] + coords2[j+1:]
                            lettersToChange.append({letter2 : [vals2New, coords2New]})
                        elif vals1[i] < vals2[j]:
                            vals1New = vals1[:i] + vals1[i+1:]
                            coords1New = coords1[:i] + coords1[i+1:]
                            lettersToChange.append({letter1 : [vals1New, coords1New]})

    uniqueLettersToChange = []
    for entry in lettersToChange:
        if entry not in uniqueLettersToChange:
            uniqueLettersToChange.append(entry)

    for entry in uniqueLettersToChange:
        for key, value in entry.items():
            if len(value[0]) == 0:
                lettersFound.pop(key)
            else:
                lettersFound[key] = value

    return lettersFound

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

def drawWords(words, lettersDictionary):
    allDragOrders = []
    
    for word in words:
        dragOrder = []
        lettersDictTemp = copy.deepcopy(lettersDictionary) # Deep copy since this is a nested dictionary with arrays
        for letter in word:
            coords = lettersDictTemp[letter][1][-1] # Use the last coordinate of the list as a drag position
            dragOrder.append(coords)
            lettersDictTemp[letter][1].pop() # Get rid of that coordinate as it has been used.
        allDragOrders.append(dragOrder)
    
    # Click cookie pan on the word cookies screen to focus on it
    pyautogui.click(713,1100)
    time.sleep(0.25)

    for pointList in allDragOrders:
        pyautogui.moveTo(pointList[0][0], pointList[0][1]) # Move to the first letter
        for x,y in pointList[1:]:
            pyautogui.mouseDown()
            pyautogui.moveTo(x, y, 0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(713,1100, 0.1) # Move to the center of the pan before letting go
        pyautogui.mouseUp()
        time.sleep(0.1)


def nextRound(nextButtonTemplate):
    ended = False
    height, width = nextButtonTemplate.shape
    screen = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    screen.save('Assets/Next-Menu.png')

    screenImg = cv2.imread('Assets/Next-Menu.png', 0)
    result = cv2.matchTemplate(screenImg, nextButtonTemplate, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    max_loc = (max_loc[0] + width/2, max_loc[1] + height/2)

    thr = 0.82
    if max_val > thr:
        ended = True
        pyautogui.click(max_loc)
        print(max_loc)
    
    return ended

if __name__ == "__main__":
    main()