from genericpath import isfile
from ntpath import join
import os
import easyocr
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from Constants import *
import shutil
from googletrans import Translator


class ImageTranslator:
    
    def __init__(self):
        self.lang = "ru"
    
    def Translate(imagefile):
        reader = easyocr.Reader(['ru', 'en'])
        ocr = reader.readtext(SourceDirectory + "/" + imagefile)
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
        
        for i in range(n_boxes):
            if (ocr[i][2] < 0.5):
                continue
            tl = (int(ocr[i][0][0][0]),int(ocr[i][0][0][1]))
            tr = (int(ocr[i][0][1][0]) - 1,int(ocr[i][0][1][1]))
            br = (int(ocr[i][0][2][0]) - 1,int(ocr[i][0][2][1]) - 1)
            bl = (int(ocr[i][0][3][0]),int(ocr[i][0][3][1]) - 1)
            rectcolor = ImageTranslator.get_rectangle_color(PILimg,tl,tr,br,bl)
            draw.rectangle((tl,br), fill = rectcolor)
            #draw.rectangle((tl,br),fill = rectcolor)
            
        for i in range(n_boxes):
            if (ocr[i][2] < 0.5):
                continue
            tl = (int(ocr[i][0][0][0]),int(ocr[i][0][0][1]))
            tr = (int(ocr[i][0][1][0]) - 1,int(ocr[i][0][1][1]))
            br = (int(ocr[i][0][2][0]) - 1,int(ocr[i][0][2][1]) - 1)
            bl = (int(ocr[i][0][3][0]),int(ocr[i][0][3][1]) - 1)
            
            b = trtext.find("()")
            text2put = trtext[:b]
            trtext = trtext[b + 3:]
            
            rectcolor = ImageTranslator.get_rectangle_color(PILimg,tl,tr,br,bl)
            textcolor = (0,0,0)
            if (rectcolor[0] + rectcolor[1] + rectcolor[2] < 382):
                textcolor = (255,255,255)
                
            textfont = ImageFont.truetype(Font, int(bl[1]/2 - tl[1]/2), encoding='UTF-8')
            draw.text((bl[0], int(bl[1] + ((tl[1] - bl[1])/2))),
                      text2put,
                      textcolor, font = textfont)
        PILimg.save(LocalDerictory + "/" + imagefile)
        print("Translation gone well!!!")

    
    def get_rectangle_color(pimg,tl,tr,bl,br):
        rgb_im = pimg.convert('RGB')
        tlc = (rgb_im.getpixel((tl)))
        trc = (rgb_im.getpixel((tr)))
        blc = (rgb_im.getpixel((bl)))
        brc = (rgb_im.getpixel((br)))
        RR = (int(tlc[0]) + int(trc[0]) + int(blc[0]) + int(brc[0]))/4
        RG = (int(tlc[1]) + int(trc[1]) + int(blc[1]) + int(brc[1]))/4
        RB = (int(tlc[2]) + int(trc[2]) + int(blc[2]) + int(brc[2]))/4
        result = (int(RR), int(RG), int(RB))
        return result

    def Run(filename):
        file = os.path.basename(filename)
        #try:    
        ImageTranslator.Translate(file)
        #except:
        #    shutil.copy(SourceDirectory + "/" + file, LocalDerictory + "/" + file)
        #    print("Error in Translition part!!")
                



def TestRun():
    onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
    for file in onlyfiles:  
        try:
            ImageTranslator.Translate(file)
        except:
            shutil.copy(SourceDirectory + "/" + file, LocalDerictory + "/" + file)
            print("Error in Translition part!!")
            
if ( __name__ == "__main__"):
    TestRun()
