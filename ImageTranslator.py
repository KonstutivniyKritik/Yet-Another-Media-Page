from genericpath import isfile
from ntpath import join
import os
import easyocr
from PIL import Image
from Constants import *
import shutil
import cv2
import regex
import numpy as np
from googletrans import Translator

def Run():
    onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
    for sourcefileineng in onlyfiles:
            Translate(sourcefileineng)

                
def Translate(imagefile):
    img = cv2.imread(SourceDirectory + "/" + imagefile)
    
    # Convert to HSV color-space
    work_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Up-sample
    work_img = cv2.resize(work_img, (0, 0), fx=2, fy=2)

    
    # dilated_img = cv2.dilate(work_img, np.ones((7, 7), np.uint8))
    # bg_img = cv2.medianBlur(dilated_img, 21)
    # diff_img = 255 - cv2.absdiff(work_img, bg_img)
    # norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255,
    #                          norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    reader = easyocr.Reader(['ru', 'en'])
    ocr = reader.readtext(img)

    #group words into phrases
    # phs = {'phrases': [], 'left': [], 'top': [], 'width': [], 'height': []}
    # ph = ""
    # left = max(d['left'])
    # top= max(d['top'])
    # width = 0
    # height = 0
    # for i in range(len(d['conf'])):
    #      if d['conf'][i] > 60:
    #          ph += d['text'][i] + " "
    #          left = left if left < d['left'][i] else d['left'][i]
    #          top = top if top < d['top'][i] else d['top'][i]
    #          width += d['width'][i]
    #          height = height if height > d['height'][i] else d['height'][i]
    #      elif ph != '':
    #          phs['phrases'].append(ph) 
    #          phs['left'].append(left)
    #          phs['top'].append(top)
    #          phs['width'].append(width)
    #          phs['height'].append(height)
    #          ph = ""
    #          left = max(d['left'])
    #          top = max(d['top'])
    #          width = 0
    #          height = 0
        
    #change text
    n_boxes = len(ocr)
    translator = Translator()
    for i in range(n_boxes):
        (tl,tr,br,bl) = (ocr[i][0][0], ocr[i][0][1], ocr[i][0][2], ocr[i][0][3])
        #colorR = img[x - 1 , y - 1, 0]
        #colorG = img[x - 1 , y - 1, 1]
        #colorB = img[x - 1 , y - 1, 2]
        img = cv2.rectangle(img, (int(tl[0]),int(tl[1])) , (int(br[0]),int(br[1])), color = (0, 0, 0), thickness= 1)
        #trtext = translator.translate(phs['phrases'][i], dest='ru').text
        #img = cv2.putText(img, trtext, org = (x, y + h),
        #                                     fontFace = cv2.FONT_HERSHEY_COMPLEX,
        #                                     fontScale = get_optimal_font_scale(phs['phrases'][i], phs['width'][i]),
        #                                     color = (255 - int(colorR), 255 - int(colorG), 255 - int(colorB)), 
        #                                     thickness = 2)
    # for i in range(n_boxes):
    #     if int(d['conf'][i]) > 60 and regex.search('[a-zA-Z]', d['text'][i]):
    #         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    #         ROI = img[y:y+h, x:x+w]
    #         blur = cv2.GaussianBlur(ROI, (51,51), 100)
    #         img[y:y+h, x:x+w] = blur
    #         trtext = translator.translate(d['text'][i], dest='ru').text
    #         img = cv2.putText(img, trtext, org = (d['left'][i], d['top'][i] + d['height'][i]),
    #                                             fontFace = cv2.FONT_HERSHEY_COMPLEX,
    #                                             fontScale = 1,
    #                                             color = (0, 0, 0), thickness = 2)
    #save image
    #cv2.imshow('image', img)
    #cv2.waitKey()
    cv2.imwrite(LocalDerictory + "/" + imagefile, img)
    print("succes")


def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=scale/10, thickness=2)
        new_width = textSize[0][0]
        if (new_width <= width):
            print(new_width)
            return scale/10
    return 1

if ( __name__ == "__main__"):
    Run()