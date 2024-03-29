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


class ImageTranslator:
    
    def __init__(self):
        self.lang = "ru"
    
    def Translate(imagefile):
        img = cv2.imread(SourceDirectory + "/" + imagefile)
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
        PILimg = Image.open(SourceDirectory + "/" + imagefile)
        draw = ImageDraw.Draw(PILimg)
        textfont = ImageFont.truetype("arial.ttf", 32, encoding='UTF-8')
        
        n_boxes = len(ocr)
        translator = Translator()
        for i in range(n_boxes):
            if (ocr[i][2] < 0.6):
                continue
            (tl,tr,br,bl) = (ocr[i][0][0], ocr[i][0][1], ocr[i][0][2], ocr[i][0][3])
            tl = tuple(map(int, tl))
            tr = tuple(map(int, tr))
            br = tuple(map(int, br))
            bl = tuple(map(int, bl))
            mbx = int((tl[0] + tr[0])/2)
            mby = int((tl[1] + bl[1])/2)
            rectcolor = ImageTranslator.get_rectangle_color(img,tl,tr,br,bl)
            draw.rectangle((tl,br), fill = rectcolor)
            #img = cv2.rectangle(img, (tl[0],tl[1]) , (br[0],br[1]), color = rectcolor, thickness= -1)
            trtext = translator.translate(ocr[i][1], dest='ru').text
            draw.text((bl[0], int((bl[1] + tl[1])/2)),
                      trtext,
                      (255 - int(rectcolor[0]), 255 - int(rectcolor[1]), 255 - int(rectcolor[2])), font = textfont)
        PILimg.save(LocalDerictory + "/" + imagefile)
        
#            img = cv2.putText(img, trtext, org = (bl[0], int((bl[1] + tl[1])/2)),
#                                                 fontFace = cv2.FONT_HERSHEY_COMPLEX,
#                                                 fontScale = ImageTranslator.get_optimal_font_scale(ocr[i][1], int(tl[0]-tr[0])),
#                                                 color = (255 - int(rectcolor[0]), 255 - int(rectcolor[1]), 255 - int(rectcolor[2])), 
#                                                 #color = (255,255,255),
#                                                 thickness = 2)
#        cv2.imwrite(LocalDerictory + "/" + imagefile, img)
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
        TLCR = img[tl[1], tl[0], 0]
        TLCG = img[tl[1], tl[0], 1]
        TLCB = img[tl[1], tl[0], 2]
        
        TRCR = img[tr[1], tr[0], 0]
        TRCG = img[tr[1], tr[0], 1]
        TRCB = img[tr[1], tr[0], 2]
        
        BLCR = img[bl[1], bl[0], 0]
        BLCG = img[bl[1], bl[0], 1]
        BLCB = img[bl[1], bl[0], 2]
        
        BRCR = img[br[1], br[0], 0]
        BRCG = img[br[1], br[0], 1]
        BRCB = img[br[1], br[0], 2]
        
        RR = (int(TLCR) + int(TRCR) + int(BLCR) + int(BRCR))/4
        RG = (int(TLCG) + int(TRCG) + int(BLCG) + int(BRCG))/4
        RB = (int(TLCB) + int(TRCB) + int(BLCB) + int(BRCB))/4
        result = (int(RR), int(RG), int(RB))
        return result

    def Run():
        onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
        for sourcefileineng in onlyfiles:
            try:    
                ImageTranslator.Translate(sourcefileineng)
            except:
                shutil.copy(SourceDirectory + "/" + sourcefileineng, LocalDerictory + "/" + sourcefileineng)
                print("Error in Translition part!!")
                



def TestRun():
    onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
    for sourcefileineng in onlyfiles:
        try:    
            ImageTranslator.Translate(sourcefileineng)
        except:
            shutil.copy(SourceDirectory + "/" + sourcefileineng, LocalDerictory + "/" + sourcefileineng)
            print("Error in Translition part!!")
            
if ( __name__ == "__main__"):
    TestRun()
