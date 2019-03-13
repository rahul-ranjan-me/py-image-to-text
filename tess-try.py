import numpy as np
import cv2
import string
import random
import os
from pytesseract import image_to_string
from flask import (
    Flask, request, redirect, url_for, flash
)
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_filename(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))+'.png'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Please select a valid file.'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            uploaded_image = Image.open(file)
            uploaded_image_x, uploaded_image_y = uploaded_image.size
            high_res_image = uploaded_image.resize((int(uploaded_image_x*1.5), int(uploaded_image_y*1.5)), Image.BICUBIC)
            uploaded_image.close()
            random_file_name = generate_random_filename()
            high_res_image.save(random_file_name)
            open_high_res_image = Image.open(random_file_name)
            text = image_to_string(open_high_res_image, lang='eng')
            open_high_res_image.close()
            os.remove(random_file_name)
            return text
        else:
            return 'Some error occured'

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
