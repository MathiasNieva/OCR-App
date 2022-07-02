from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import ocr
import pathlib
import os, glob

UPLOAD_FOLDER = './static/uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':

        for file in os.scandir(app.config['UPLOAD_FOLDER']):
            os.remove(file.path)

        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('index.html', msg='No file selected')

        if file and allowed_file(file.filename):

            #save uploaded image 
            filename = secure_filename(file.filename)
            path = pathlib.Path(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            # call the OCR function on it
            extracted_text = ocr.ocr_core(file)
            text_with_space = ocr.text_with_space(extracted_text)
            text_lines = ocr.lines(extracted_text)
            most_common_words = ocr.mostCommon(extracted_text)
            audio_path = ocr.textToSpeech(extracted_text, app.config['UPLOAD_FOLDER'], filename)

            

            # extract the text and display it
            return render_template('index.html',
                                   msg='Successfully processed',
                                   extracted_text=text_with_space,
                                   most_common_words=most_common_words,
                                   text_lines=text_lines,
                                   audio_path=audio_path,
                                   img_src=path)
    elif request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.run()