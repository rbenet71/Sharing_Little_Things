#
# Little Script for Geotag Pictures of a Garmin DashCam
# Robert Benet - 30/08/2020
#
# Information extract from:
# How to configur Tesseract
# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i/53672281
# Install Teseract for windows
# https://github.com/UB-Mannheim/tesseract/wiki
# Install Tesseact for Python
# https://pypi.org/project/pytesseract/
# Tutorial for Tesseract
# https://nanonets.com/blog/ocr-with-tesseract/
# pyexiv2
# https://pypi.org/project/pyexiv2/

import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from pyexiv2 import Image

class Ocr_Dascam():
    def __init__(self,dir_to_find=None,oem=None,psm=None,parent=None,filter_image_selected=None):       
        from os import scandir,path
        
        # App Message
        if parent==None:
            self.parent=self
            self.parent.info=self.info

        #check exist and set path of EXE Tesseract
        exe_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not path.exists(exe_tesseract):
            self.parent.info('File not exist: '+exe_tesseract)
            return  
        pytesseract.pytesseract.tesseract_cmd = exe_tesseract

        # Adding custom options
        if not oem==None and not psm==None:
            custom_config=r'--oem '+str(oem)+' --psm '+str(psm[:2])
        elif not oem==None:
            custom_config=r'--oem '+str(oem)
            custom_config=r' --psm'+str(psm)
        else:
            custom_config = r'--oem 3 '
        
        # Select Photo Directory
        if dir_to_find==None:
            self.select_directory()
        else:
            self.dir_to_find=dir_to_find

        result={}
        correct=0
        incorrect=0
        # Create TXT File with Results
        file_txt=open(path.join(self.dir_to_find,'Result_OCR_Scan.txt'),'w')
        file_txt.write('Configuration '+custom_config+chr(10))
        file_txt.write('Filter '+filter_image_selected+chr(10)+chr(10))

        for file in scandir(self.dir_to_find):
            # extract name file and extension separate
            name,ext=path.splitext(file.name)

            # Find coordinates from a picture file
            if ext.upper()=='.JPG' or ext.upper()=='.JPEG' or ext.upper()=='.PNG':
                find=False
                incorrect+=1
                day=' No Encontrado'
                hour=''
                lat=''
                lon=''

                # Filter Image for a good reading
                self.filter_image(file.path,filter_image_selected)

                read = pytesseract.image_to_data(self.img, output_type=Output.DICT)

                for i in range(len(read['text'])):
                    if read['text'][i]=='GARMIN':
                        find=True
                        day=read['text'][i+1]
                        hour=read['text'][i+2]
                        lat=float(read['text'][i+3])
                        lon=float(read['text'][i+4])
                        
                        self.geotag_photo(file.path,lat,lon)
                        incorrect-=1
                        correct+=1
                        break
                    
                result[file.path]={'day':day,'hour':hour,'lat':lat,'lon':lon,'find':find}
                text_result=file.path+" "+day+" "+hour+" "+str(lat)+" "+str(lon)
                file_txt.write(text_result+chr(10))
                self.parent.info(text_result)

        #self.parent.info(result)
        self.parent.info('GeoLocalizados   : '+str(correct))
        self.parent.info('No GeoLocalizados: '+str(incorrect))
        
        file_txt.write('GeoLocalizados   : '+str(correct)+chr(10))
        file_txt.write('No GeoLocalizados: '+str(incorrect)+chr(10))
        file_txt.close()
        
    # Geotag Photo
    def geotag_photo(self,file,lat,lon):
        img = Image(file)
        exif_lat=str(int(lat))+"/1 "+str(int(lat % 1 * 60))+"/1 "+str(int(round((lat % 1 * 60)%1*60,4)*100))+"/100"
        exif_lon=str(int(lon))+"/1 "+str(int(lon % 1 * 60))+"/1 "+str(int(round((lon % 1 * 60)%1*60,4)*100))+"/100"
        if int(lat)<0:
            exif_lat_ref='S'
        else:
            exif_lat_ref='N'

        if int(lon)<0:
            exif_lon_ref='W'
        else:
            exif_lon_ref='E'
        img.modify_exif({'Exif.GPSInfo.GPSLatitudeRef': exif_lat_ref,'Exif.GPSInfo.GPSLatitude': exif_lat,'Exif.GPSInfo.GPSLongitudeRef': exif_lon_ref, 'Exif.GPSInfo.GPSLongitude': exif_lon})
        #self.parent.info(exif_lat,"_",exif_lon)
    
    # Select directory
    def select_directory(self):
        from tkinter import filedialog
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        self.dir_to_find = filedialog.askdirectory()

    # App Message
    def info(self,message):
        print (message)
    
    def filter_image(self,file,filter):
        img = cv2.imread(file) 
        img=self.get_grayscale(img) 
        if filter==None or filter=='Dilate':
            self.img=self.dilate(img)
        elif filter=='Thresholding':
            self.img=self.thresholding(img) 
        elif filter=='Remove Noise':
            self.img=self.remove_noise(img) 
        elif filter=='Erosion':
            self.img=self.erode(img)
        elif filter=='Opening':
            self.img=self.opening(img)  
        elif filter=='Canny':
            self.img=self.canny(img)  
        elif filter=='Eskew':
            self.img=self.deskew(img) 

    # gray scale
    def get_grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self,image):
        return cv2.medianBlur(image,5)
    
    #thresholding
    def thresholding(self,image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def dilate(self,image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
        
    #erosion
    def erode(self,image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self,image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(self,image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(self,image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    #template matching
    def match_template(self,image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 
    

if __name__ == "__main__":
    # Load Main Modul
    #action=Ocr_Dascam()

    import tkinter as tk
    from tkinter import ttk
    
    app = tk.Tk() 
    app.title("GeoTag Photos from Garmin Dash Cam")
    app.geometry('500x200')
    
    line0=tk.Label(app, text = '')
    line0.grid(column=0, row=0)
    
    labelOEM = tk.Label(app, text = "OEM")
    labelOEM.grid(column=0, row=2,sticky='W',padx=5)

    comboOEM = ttk.Combobox(app,values=[0,1,2,3])
    comboOEM.grid(column=1, row=2,sticky='W',padx=5)
    comboOEM.current(3)
    
    labelPSM = tk.Label(app, text = "PSM")
    labelPSM.grid(column=0, row=3,sticky='W',padx=5)
    
    comboPSM= ttk.Combobox(app, width=55,values=['0 Orientation and script detection (OSD) only.','1    Automatic page segmentation with OSD.','2    Automatic page segmentation, but no OSD, or OCR.','3    Fully automatic page segmentation, but no OSD. (Default)','4    Assume a single column of text of variable sizes.','5    Assume a single uniform block of vertically aligned text.','6    Assume a single uniform block of text.','7    Treat the image as a single text line.','8    Treat the image as a single word.','9    Treat the image as a single word in a circle.','10    Treat the image as a single character.','11    Sparse text. Find as much text as possible in no particular order.','12    Sparse text with OSD.','13    Raw line. Treat the image as a single text line, bypassing hacks that are'])
    comboPSM.grid(column=1, row=3,sticky='W',padx=5)
    comboPSM.current(3)
    
    labelFilter = tk.Label(app, text = "Photo Filter")
    labelFilter.grid(column=0, row=5,sticky='W',padx=5)
    
    comboFilter= ttk.Combobox(app,values=['Dilate','Thresholding','Remove Noise','Erosion','Opening','Canny','Eskew'])
    comboFilter.grid(column=1, row=5,sticky='W',padx=5)
    comboFilter.current(0)
    
    line6=tk.Label(app, text = '')
    line6.grid(column=0, row=6)
    
    buton_action=tk.Button(app, text = "Execute",command=lambda: Ocr_Dascam(oem=comboOEM.get(),psm=comboPSM.get(),filter_image_selected=comboFilter.get()))
    buton_action.grid(column=1, row=7,sticky='E',padx=5)
    
    app.mainloop()
    app.quit()



    #print(comboOEM .current(), comboOEM.get())
    #action=Ocr_Dascam(dir_to_find=r'C:\GisBike\Test\SECRETARIA\VOLTA 2020\RECORREGUTS\ETAPA 1\FOTOS\RECORREGUT_TEST')