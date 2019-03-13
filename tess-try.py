import numpy as np
import cv2
import pytesseract
from flask import (
    Flask, request, redirect, url_for, flash
)
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print (request.files)
        if 'file' not in request.files:
            return 'Please select a valid file.'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            im = Image.open(file)
            nx, ny = im.size
            im2 = im.resize(( int(nx*1.5), int(ny*1.5) ), Image.BICUBIC)
            im2.save("temp.png")
            newImg = Image.open("temp.png")
            text = pytesseract.image_to_string(newImg, lang = 'eng')
            return text
        else:
            return 'Some error occured'
    

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)