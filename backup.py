from gtts import gTTS
import os
from PIL import Image
import subprocess
import cv2
import pytesseract

os.chdir(r"C:\Users\raza\Documents\PythonProjects\OCRtoTTS")

pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')

# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(r"C:\Users\raza\Documents\PythonProjects\OCRtoTTS\img.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
text_file = open("text.txt", "w")
text_file.write(data)
text_file.close()


cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imshow('invert', invert)
cv2.waitKey()

fh = open("text.txt", "r")
myText = fh.read().replace("\n", " ")


language = 'en'
accent= 'co.uk'
output = gTTS(text=myText, lang=language, slow=False, tld=accent)

output.save("output.mp3")
fh.close()
os.system("start output.mp3")