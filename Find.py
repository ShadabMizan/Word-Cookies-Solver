# Find.py contains functions that deal with capturing an image from the word cookies screen and returning the coordinates of a targetted template

import cv2
import numpy as np
from PIL import ImageGrab

# Word cookies screen corners
x1 = 0
y1 = 0
x2 = 1430
y2 = 1519

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
                
                # Skip this detection if it was detected outside of the cookie pan area, which are points below (greater than) y = 775
                if max_loc[1] < 775: 
                    continue
                
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
    lettersToChange = [] # Contains a list of letters that will need to be changed
    thr = 25
    for letter1 in list(lettersFound.keys()):
        for letter2 in list(lettersFound.keys()):
            if letter1 == letter2:
                continue
            
            # Store max values and coordinates to compare if different letters are being detected in the smae spot.
            vals1 = lettersFound[letter1][0]
            coords1 = lettersFound[letter1][1]
            vals2 = lettersFound[letter2][0]
            coords2 = lettersFound[letter2][1]

            for i in range(0, len(coords1)):
                for j in range(0, len(coords2)):
                    if abs(coords1[i][0] - coords2[j][0]) < thr and abs(coords1[i][1] - coords2[j][1]) < thr:
                        # Letter 1 has a better match than letter 2 at that spot
                        if vals1[i] > vals2[j]:
                            # Remove from letter2
                            vals2New = vals2[:j] + vals2[j+1:]
                            coords2New = coords2[:j] + coords2[j+1:]
                            lettersToChange.append({letter2 : [vals2New, coords2New]})
                        # Letter 2 has a better match
                        elif vals1[i] < vals2[j]:
                            vals1New = vals1[:i] + vals1[i+1:]
                            coords1New = coords1[:i] + coords1[i+1:]
                            lettersToChange.append({letter1 : [vals1New, coords1New]})

    # Make the lettersToChange list unique so there are no duplicates
    uniqueLettersToChange = []
    for entry in lettersToChange:
        if entry not in uniqueLettersToChange:
            uniqueLettersToChange.append(entry)

    # A letter's values and coords can be empty if another letter has a better match for it at all its suspected locs
    # If so, remove it from the final lettersFound list.
    for entry in uniqueLettersToChange:
        for key, value in entry.items():
            if len(value[0]) == 0:
                lettersFound.pop(key)
            else:
                lettersFound[key] = value

    return lettersFound

def findEmptySquares(emptySquare):
    screen = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    screen.save('Assets/Temp/Empty-Squares-Check.png')

    screenImg = cv2.imread('Assets/Temp/Empty-Squares-Check.png', 0)
    
    missingWordLengths = []
    height = 0
    width = 0

    # Find what at what scale the squares in the image are
    bestMatch = 0
    bestScale = 0
    for scalar in range(60,100,2):
        scalar = scalar / 100
        emptySquareScaled = cv2.resize(emptySquare, None, fx=scalar, fy=scalar)

        height, width = emptySquareScaled.shape

        result = cv2.matchTemplate(screenImg, emptySquareScaled, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        if len(locations) == 0:
            continue

        if bestMatch < len(locations):
            bestMatch = len(locations)
            bestScale = scalar
        
    if bestScale == 0:
        # Did not find any empty squares
        return [], 0, 0
    
    emptySquareScaled = cv2.resize(emptySquare, None, fx=bestScale, fy=bestScale)

    height, width = emptySquareScaled.shape

    result = cv2.matchTemplate(screenImg, emptySquareScaled, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # Initialize lists to store coordinates and max_val
    squareLocs = []
    thr = 5
    # Iterate over each location and extract max_val
    for loc in locations:
        max_loc = (loc[0] + width/2, loc[1] + height/2)
        squareLocs.append(max_loc)

        for i in range(0,len(squareLocs)-1):
            if abs(squareLocs[-1][0] - squareLocs[i][0]) < thr and abs(squareLocs[-1][1] - squareLocs[i][1]) < thr:
                # Duplicate found, remove the most recent one
                squareLocs.pop()
                break
                
    # Determine if they are in a line, close together. 
    # Here are the acceptable thresholds for a line of squares to be considered part of the same missing word.
    thrX = 0.15*width
    thrY = 5

    # First, lets group points by their y-coords.
    wordLocsByY = [[squareLocs[0]]]

    for i in range(1,len(squareLocs)):
        found = False
        for j in range(0,len(wordLocsByY)):
            if abs(squareLocs[i][1] - wordLocsByY[j][0][1]) < thrY:
                wordLocsByY[j].append(squareLocs[i])
                found = True
        
        if not found:
            wordLocsByY.append([squareLocs[i]])

    # Then, We put them in ascending order of their x coordinates.
    wordLocs = []
    for line in wordLocsByY:
        wordLocs.append(sorted(line, key=lambda x: x[0]))

    wordLength = 1

    for line in wordLocs:
        for i in range(1,len(line)):
            xDist = line[i][0] - line[i-1][0] 
            if abs(xDist - width) < thrX:
                wordLength += 1
            else:
                missingWordLengths.append(wordLength)
                wordLength = 1
            
        missingWordLengths.append(wordLength)
        wordLength = 1
             
    return missingWordLengths, width, height

def checkFoundWord(squareWidth, squareHeight, n):
    screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    if n % 2 == 0:
        screen.save('Assets/Temp/screen1.png')
    elif n % 2 == 1:
        screen.save('Assets/Temp/screen2.png')

    screen1 = cv2.imread('Assets/Temp/screen1.png', 0)

    screen2 = cv2.imread('Assets/Temp/screen2.png', 0)
    if screen2 is None:
        screen2 = screen1.copy()
    

    # Compute absolute difference between the two images
    diff = cv2.absdiff(screen1, screen2)

    # Threshold the difference image
    diff_threshold = 30
    _, thresholded_diff = cv2.threshold(diff, diff_threshold, 255, cv2.THRESH_BINARY) # Set any pixels passing the diff_threshold to a max value of 255

    # Find contours in the thresholded difference image
    contours, _ = cv2.findContours(thresholded_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours and centre coords
    coords = []
    for contour in contours:
        x, y, _, _ = cv2.boundingRect(contour)
        # Only look at changes made in the word bank area
        if y > 185 and y < 775:
            coords.append((x + squareWidth/2, y + squareHeight/2))

    return coords
    
        