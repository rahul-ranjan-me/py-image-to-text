import string, random, os, pytesseract
from flask import (
    Flask, request
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
            random_file_name = generate_random_filename()
            uploaded_image.save(random_file_name)
            open_high_res_image = Image.open(random_file_name)
            text = pytesseract.image_to_string(open_high_res_image, lang='eng')
            os.remove(random_file_name)
            return text
        else:
            return 'Some error occured'

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
