from genericpath import isfile
from ntpath import join
import os
import easyocr
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from Constants import *
import shutil
import cv2
import regex
import numpy as np
from googletrans import Translator
import shutil
import math


class ImageTranslator:
    
    def __init__(self):
        self.lang = "ru"
    
    def Translate(imagefile):
        img = cv2.imread(SourceDirectory + "/" + imagefile)
        reader = easyocr.Reader(['ru', 'en'])
        ocr = reader.readtext(img)
        n_boxes = len(ocr)

        #group words into phrases
        phs = {'phrases': [], 'tl': [], 'tr': [], 'br': [], 'bl': []}
        ph = ""
        # width = 0
        # height = 0  
        for i in range(n_boxes):
             if (ocr[i][2] >  0.5):
                ph += ocr[i][1] + "() "
        
        translator = Translator()
        trtext = translator.translate(ph, dest='ru').text
        

        PILimg = Image.open(SourceDirectory + "/" + imagefile)
        draw = ImageDraw.Draw(PILimg)
        textfont = ImageFont.truetype("arial.ttf", 32, encoding='UTF-8')
        
        for i in range(n_boxes):
            if (ocr[i][2] < 0.6):
                continue
            (tl,tr,br,bl) = (ocr[i][0][0], ocr[i][0][1], ocr[i][0][2], ocr[i][0][3])
            tl = tuple(map(int, tl))
            tr = tuple(map(int, tr))
            br = tuple(map(int, br))
            bl = tuple(map(int, bl))
            rectcolor = ImageTranslator.get_rectangle_color(img,tl,tr,br,bl)
            draw.rectangle((tl,br), fill = rectcolor)
            #draw.rectangle((tl,br),fill = rectcolor)
            
        for i in range(n_boxes):
            if (ocr[i][2] < 0.6):
                continue
            (tl,tr,br,bl) = (ocr[i][0][0], ocr[i][0][1], ocr[i][0][2], ocr[i][0][3])
            tl = tuple(map(int, tl))
            tr = tuple(map(int, tr))
            br = tuple(map(int, br))
            bl = tuple(map(int, bl))
            b = trtext.find("()")
            text2put = trtext[:b]
            trtext = trtext[b + 3:]
            draw.text((bl[0], int((bl[1] + tl[1])/2)),
                      text2put,
                      (255 - int(rectcolor[0]), 255 - int(rectcolor[1]), 255 - int(rectcolor[2])), font = textfont)
        PILimg.save(LocalDerictory + "/" + imagefile)
        print("Translation gone well!!!")

    def get_optimal_font_scale(text, width):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=scale/10, thickness=3)
            new_width = textSize[0][0]
            if (new_width <= width):
                print(new_width)
                return scale/10
        return 1
    
    def get_rectangle_color(img,tl,tr,bl,br):
        tlc = (img[tl[1], tl[0], 0], img[tl[1], tl[0], 1], img[tl[1], tl[0], 2])
        trc = (img[tr[1], tr[0], 0], img[tr[1], tr[0], 1], img[tr[1], tr[0], 2])
        blc = (img[bl[1], bl[0], 0], img[bl[1], bl[0], 1], img[bl[1], bl[0], 2])
        brc = (img[br[1], br[0], 0], img[br[1], br[0], 1], img[br[1], br[0], 2])
        RR = (int(tlc[0]) + int(trc[0]) + int(blc[0]) + int(brc[0]))/4
        RG = (int(tlc[1]) + int(trc[1]) + int(blc[1]) + int(brc[1]))/4
        RB = (int(tlc[2]) + int(trc[2]) + int(blc[2]) + int(brc[2]))/4
        result = (int(RR), int(RG), int(RB))
        return result

    def Run(filename):
        file = os.path.basename(filename)
        try:    
            ImageTranslator.Translate(file)
        except:
            shutil.copy(SourceDirectory + "/" + file, LocalDerictory + "/" + file)
            print("Error in Translition part!!")
                



def TestRun():
    onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
    for file in onlyfiles:  
        #try:
            ImageTranslator.Translate(file)
        #except:
        #    shutil.copy(SourceDirectory + "/" + file, LocalDerictory + "/" + file)
        #    print("Error in Translition part!!")
            
if ( __name__ == "__main__"):
    TestRun()
