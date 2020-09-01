
import pytesseract
from pytesseract import Output
import cv2

img = cv2.imread('39.jpg')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Adding custom options
custom_config = r'--oem 3 --psm 6'
custom_config = r'--oem 3 '
#print(pytesseract.image_to_string(img, config=custom_config))

d = pytesseract.image_to_data(img, output_type=Output.DICT)
#d = pytesseract.image_to_data(img)

print(d)
print(d['text'])
print(len(d['text']))

for i in range(len(d['text'])):
    print(d['text'][i])
    if d['text'][i]=='GARMIN':
        lat=d['text'][i+3]
        lon=d['text'][i+4]
        break
print(lat,lon)
