# Load.py contains functions that should load data from files in the Assets folder into memeory for fast look-up.

from PIL import ImageGrab
import cv2
import os

# Word cookies screen corners
x1 = 0
y1 = 0
x2 = 1430
y2 = 1519

def loadCookiePan():
    # Grab a screenshot of the word-cookies screen.
    cookiePanScreenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    cookiePanScreenshot.save('Assets/Temp/cookie-pan.png')

    cookiePan = cv2.imread('Assets/Temp/cookie-pan.png', 0)
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
        Dictionary[letter] = {3: [], 4: [], 5: [], 6: []}  # Initialize sub-dictionary for each letter
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
        with open('Assets/Texts/{}/six.txt'.format(letter), 'r') as sixTxt:
            words = sixTxt.readlines()
            words = [word.strip() for word in words]  
            Dictionary[letter][6].extend(words)  
    return Dictionary

def load_nGrams():
    Bigrams = []
    Trigrams = []
    with open('Assets/Texts/bigrams.txt', 'r') as file:
        bigrams = file.readlines()
        bigrams = [bigram.strip() for bigram in bigrams]
        Bigrams.extend(bigrams)
    with open('Assets/Texts/trigrams.txt', 'r') as file:
        trigrams = file.readlines()
        trigrams = [trigram.strip() for trigram in trigrams]
        Trigrams.extend(trigrams)
    
    return Bigrams, Trigrams

def deleteTempFiles():
    folderPath = 'Assets/Temp'
    # List all files in the folder
    files = os.listdir(folderPath)
    
    # Iterate over each file and delete it
    for fileName in files:
        filePath = os.path.join(folderPath, fileName)
        try:
            os.remove(filePath)
            print(f"Deleted: {filePath}")
        except Exception as e:
            print(f"Failed to delete: {filePath}. Error: {e}")