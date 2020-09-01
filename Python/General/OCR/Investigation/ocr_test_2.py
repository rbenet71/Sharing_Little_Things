# How to configur Tesseract
# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i/53672281
# Install Teseract for windows
# https://github.com/UB-Mannheim/tesseract/wiki
# Install Tesseact for Python
# https://pypi.org/project/pytesseract/
# Tutorial for Tesseract
# https://nanonets.com/blog/ocr-with-tesseract/

import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from pyexiv2 import Image

if 'libreries'=='libreries':
    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image,5)
    
    #thresholding
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def dilate(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
        
    #erosion
    def erode(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(image):
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
    def match_template(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

#check exist
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Adding custom options
custom_config = r'--oem 3 '

from os import scandir,path
dir_to_find=r'C:\GisBike\Test\SECRETARIA\VOLTA 2020\RECORREGUTS\ETAPA 1\FOTOS\RECORREGUT_TEST'

result={}

for file in scandir(dir_to_find):
    # extract name file and extension separate
    name,ext=path.splitext(file.name)
    find=False
    day=' No Encontrado'
    hour=''
    lat=''
    lon=''

    # Find coordinates from a picture file
    if ext.upper()=='.JPG' or ext.upper()=='.JPEG' or ext.upper()=='.PNG':
        #pictures.append({'Path':file.path,'Name':name,'Lat':image.lat,'Lon':image.lon})

        img = cv2.imread(file.path) 
        img=get_grayscale(img) 
        #img=thresholding(img) 
        img=dilate(img)
        
        d = pytesseract.image_to_data(img, output_type=Output.DICT)

        for i in range(len(d['text'])):
            if d['text'][i]=='GARMIN':
                find=True
                day=d['text'][i+1]
                hour=d['text'][i+2]
                lat=float(d['text'][i+3])
                lon=float(d['text'][i+4])
                
                                
                img = Image(file.path)
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
                #print(exif_lat,"_",exif_lon)
                break
        result[file.path]={'day':day,'hour':hour,'lat':lat,'lon':lon,'find':find}
        print(file.path,day,hour,lat,lon)

print(result)