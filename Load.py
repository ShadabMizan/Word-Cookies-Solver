# Load.py contains functions that should load data from files in the Assets folder into memeory for fast look-up.

from PIL import ImageGrab
import cv2

# Word cookies screen corners
x1 = 0
y1 = 0
x2 = 1430
y2 = 1519

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