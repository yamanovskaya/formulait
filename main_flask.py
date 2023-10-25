import uuid
import threading
from flask import Flask, render_template, request, session, jsonify, make_response
from img_processor import *
import os
import base64

app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'

def start_process_thread(name : str):
    x = do_processing_image(app.config['UPLOAD_FOLDER'], name)
    print(x)

@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')
@app.route('/uploadajax', methods=['post'])
def uploadFile():
    if request.method == 'POST':
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        # Upload file flask
        uploaded_img = request.files['file']
        # Extracting uploaded data file name
        img_filename = uploaded_img.filename
        request_id = uuid.uuid4().hex
        session['request_id'] = request_id
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], request_id))
        file_size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], request_id))
        prc = threading.Thread(target=start_process_thread, args=(request_id,)) #string from tuple for args
        prc.start()
        return jsonify(request_id=request_id, name=img_filename, size=file_size)

@app.route("/processing", methods=['get', 'post'])
def Processing():
    return render_template('processing.html')
@app.route("/waiting/<id>", methods=["POST"])
def DoWaiting(id):
    if request.method == 'POST':
        if(os.path.exists(get_data_file_path(id))):
            return jsonify(status="completed")
        else:
            return jsonify(status="processing")

@app.route('/describe')
def describe():
    return render_template('describe.html')


@app.route('/result', methods=['get', 'post'])
def result():
    return render_template('resalt.html')

@app.route('/get_image/<id>', methods=['get', 'post'])
def get_image(id):
    if request.method == 'GET':
        if(os.path.exists(get_data_file_path(id))):
            with open(get_data_file_path(id), "rb") as f:
                info = json.load(f)
                with open(info['filename'], "rb") as f:
                    image_binary = f.read()

                    response = make_response(base64.b64encode(image_binary))
                    response.headers.set('Content-Type', 'image/png')
                    response.headers.set('Content-Disposition', 'attachment', filename=info['filename'])
                    return response

@app.route('/get_preview', methods=['get', 'post'])
def get_preview():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['file']
        if not os.path.exists(OUTPUT_DIR_PREVIEW):
            os.makedirs(OUTPUT_DIR_PREVIEW)
        name = uuid.uuid4().hex
        filename = os.path.join(OUTPUT_DIR_PREVIEW, name)
        uploaded_img.save(filename)
        image_binary = get_preview_from_file(name)
        response = make_response(base64.b64encode(image_binary))
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='preview')
        return response


@app.route('/get_result/<id>', methods=['get', 'post'])
def get_result(id):
    if request.method == 'POST':
        if(os.path.exists(get_data_file_path(id))):
            with open(get_data_file_path(id), "rb") as f:
                info = json.load(f)
                return jsonify(info) #not using direct file coz it could contains shit

if __name__ == '__main__':
    app.run()
