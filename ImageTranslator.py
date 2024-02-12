from genericpath import isfile
from ntpath import join
import os
import pytesseract
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
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove shadows, cf. https://stackoverflow.com/a/44752405/11089932
    dilated_img = cv2.dilate(gray, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(gray, bg_img)
    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255,
                             norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # Threshold using Otsu's
    work_img = cv2.threshold(norm_img, 0, 255, cv2.THRESH_OTSU)[1]

    #tesseract
    custom_config = '--psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    d = pytesseract.image_to_data(work_img, output_type="dict")

    #change text
    n_boxes = len(d['text'])
    translator = Translator()
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60 and regex.search('[a-zA-Z]', d['text'][i]):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            ROI = img[y:y+h, x:x+w]
            blur = cv2.GaussianBlur(ROI, (51,51), 100)
            img[y:y+h, x:x+w] = blur
            trtext = translator.translate(d['text'][i], dest='ru').text
            img = cv2.putText(img, trtext, org = (d['left'][i], d['top'][i] + d['height'][i]),
                                                fontFace = cv2.FONT_HERSHEY_COMPLEX,
                                                fontScale = 1,
                                                color = (255, 0, 0), thickness = 2)
    #save image
    cv2.imshow('image', img)
    cv2.waitKey()

if ( __name__ == "__main__"):
    Run ()