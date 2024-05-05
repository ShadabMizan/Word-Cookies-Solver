# Draw.py contains functions that deal with the goal of interacting with the word cookies screen

import copy
import pyautogui
import time
from PIL import ImageGrab
import cv2

# Word cookies screen corners
x1 = 0
y1 = 0
x2 = 1430
y2 = 1519

# Cookie Pan centre Coordinates
pan_x = 713
pan_y = 1100

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
    pyautogui.click(pan_x, pan_y)
    time.sleep(0.25)

    for pointList in allDragOrders:
        pyautogui.moveTo(pointList[0][0], pointList[0][1]) # Move to the first letter
        for x,y in pointList[1:]:
            pyautogui.mouseDown()
            pyautogui.moveTo(x, y, 0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(pan_x, pan_y, 0.1) # Move to the center of the pan before letting go
        pyautogui.mouseUp()
        time.sleep(0.1)

def nextRound(nextButtonTemplate):
    ended = False
    height, width = nextButtonTemplate.shape
    screen = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    screen.save('Assets/Temp/Next-Menu.png')

    screenImg = cv2.imread('Assets/Temp/Next-Menu.png', 0)
    result = cv2.matchTemplate(screenImg, nextButtonTemplate, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    max_loc = (max_loc[0] + width/2, max_loc[1] + height/2) # Have max_loc coordinates centered on the button

    thr = 0.8
    if max_val > thr:
        ended = True
        pyautogui.click(max_loc)
    
    return ended

def drawAWord(word, lettersDictionary):
    dragOrder = []
    lettersDictTemp = copy.deepcopy(lettersDictionary) # Deep copy since this is a nested dictionary with arrays
    for letter in word:
        coords = lettersDictTemp[letter][1][-1] # Use the last coordinate of the list as a drag position
        dragOrder.append(coords)
        lettersDictTemp[letter][1].pop() # Get rid of that coordinate as it has been used.
    
    # Click cookie pan on the word cookies screen to focus on it
    pyautogui.click(pan_x, pan_y)
    time.sleep(0.25)

    if len(dragOrder) == 0:
        return

    pyautogui.moveTo(dragOrder[0][0], dragOrder[0][1]) # Move to the first letter
    for x,y in dragOrder[1:]:
        pyautogui.mouseDown()
        pyautogui.moveTo(x, y, 0.01)
    pyautogui.mouseDown()
    pyautogui.moveTo(pan_x, pan_y, 0.01) # Move to the center of the pan before letting go
    pyautogui.mouseUp()


def shuffle():
    # Click coordinates of shuffle button
    pyautogui.click(365, 1430) 
