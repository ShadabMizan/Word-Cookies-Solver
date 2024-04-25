import pyautogui
import time
import cv2
from PIL import ImageGrab

# Borders of the entire playable screen are:
# (310, 64), (1128, 1514)

# Cookie area is (310, 810) to (1128, 1514)
x1 = 310
y1 = 64
x2 = 1128
y2 = 1514

cookiePanScreenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
cookiePanScreenshot.save('Assets/cookie-pan.png')

cookiePan = cv2.imread('Assets/cookie-pan.png', 0)

letters = ['C','G','M','P','U','Y']
templates = []
for letter in letters:
    t = 'Assets/{}.png'.format(letter)
    templates.append(cv2.imread(t, 0))

threshold = 0.8
for template in templates:
    cookiePanCopy = cookiePan.copy()
    height, width = template.shape

    result = cv2.matchTemplate(cookiePanCopy, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    location = max_loc
    top_left = (location[0], location[1])
    bottom_right = (location[0] + width, location[1] + height)
    if max_val >= threshold:
        cv2.rectangle(cookiePanCopy, top_left, bottom_right, 255, 5)
        cv2.imshow('Match', cookiePanCopy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No Match")
