import pyautogui
import time
import cv2
from PIL import ImageGrab

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
    letters = ['C','G','M','P','U','Y'] # Letters that we have.
    templates = []
    for letter in letters:
        file_path = 'Assets/{}.png'.format(letter)
        templates.append(cv2.imread(file_path, 0))
    


    findLetters(templates, letters, cookiePan, 0.8)


def findLetters(templates, letters, img, threshold):
    lettersFound = []
    for i in range(0,len(templates)):
        template = templates[i]
        height, width = template.shape

        # Need to rotate the template because the letters can spawn in any orientation. Then we need to test all these orientations to see if we get a really good match.
        # [-16,17] step size 8
        for angle in range(-16,17,8):
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            rotated_template = cv2.warpAffine(template, rotation_matrix, (width, height))
            result = cv2.matchTemplate(img, rotated_template, cv2.TM_CCOEFF_NORMED) # Resulting width of this new 2D img array is (W - w + 1, H - h + 1) Where W is the width of the base image adn w is the width of template
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                lettersFound.append(letters[i])
                print(letters[i])
                break


if __name__ == "__main__":
    main()