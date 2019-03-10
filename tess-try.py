import numpy as np
import cv2
import pytesseract
from flask import (
    Flask
)

app = Flask(__name__)

@app.route('/')
def home():
    imageName = input("Enter your image name: ")
    im = cv2.imread(imageName, 0)

    text = pytesseract.image_to_string(im, lang = 'eng')

    return text

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)