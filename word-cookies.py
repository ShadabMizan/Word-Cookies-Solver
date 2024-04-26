import pyautogui
import time
import cv2
from PIL import ImageGrab
import numpy as np

# Borders of the entire playable screen are: (When docked to the left half of the window)
# (310, 64), (1128, 1514)

# Pan area is (310, 810) to (1128, 1514)
x1 = 310
y1 = 64
x2 = 1128
y2 = 1514

def main():
    # Grab a screenshot of the word-cookies screen.
    cookiePanScreenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    cookiePanScreenshot.save('Assets/cookie-pan.png')

    cookiePan = cv2.imread('Assets/cookie-pan.png', 0)

    # Store all the letters that we know in their imread form in a templates array.
    letters = ['A','B','C','F','G','M','O','P','T','U','Y'] # Letters that we have.
    templates = []
    for letter in letters:
        file_path = 'Assets/{}.png'.format(letter)
        templates.append(cv2.imread(file_path, 0))
    


    foundLetters, locationsLetters = findLetters(templates, letters, cookiePan, 0.8)
    print(foundLetters)
    print(locationsLetters)


def findLetters(templates, letters, img, threshold):
    lettersFound = []
    lettersLocs = []
    lettersVals = []
    for check in range(2):
        for i in range(0,len(templates)):
            template = templates[i]
            height, width = template.shape

            # Need to rotate the template because the letters can spawn in any orientation. Then we need to test all these orientations to see if we get a really good match.
            # [-16,17] step size 8
            for angle in range(-16,17,8):
                rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
                rotated_template = cv2.warpAffine(template, rotation_matrix, (width, height))
                result = cv2.matchTemplate(img, rotated_template, cv2.TM_CCOEFF_NORMED) 
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # Match found, but can be false positives. ex. F and P look similar
                if max_val >= threshold:
                    if letters[i] not in lettersFound:
                        lettersFound.append(letters[i])
                        lettersLocs.append(max_loc)
                        lettersVals.append(max_val)
                        if lettersVals[-1] < max_val:
                            lettersVals[-1] = max_val
                        break                                
        print("Shuffling...")    
        pyautogui.click(360, 1420)
        time.sleep(1)
    
    # Threshold to check if a location of an identified letter is too close (i.e. the same spot) as another letter
    thr = 25
    indices = []
    for i in range(len(lettersLocs)):
        for j in range(i + 1, len(lettersLocs)):
            if abs(lettersLocs[i][0] - lettersLocs[j][0]) <= thr and abs(lettersLocs[i][1] - lettersLocs[j][1]) <= thr: # Two x and y coords are close together.
                # Check which letter has a higher match
                if lettersVals[i] > lettersVals[j]:
                    indices.append(j)
                else:
                    indices.append(i)
    indices.sort()
    indices = list(set(indices))
    while len(indices) > 0:
        lettersLocs.pop(indices[-1])
        lettersFound.pop(indices[-1])
        indices.pop()
                


    return lettersFound, lettersLocs

if __name__ == "__main__":
    main()