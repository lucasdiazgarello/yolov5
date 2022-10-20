import os
import time

from flask import Flask, render_template, url_for, request, flash, redirect
import subprocess
import sys

from werkzeug.utils import secure_filename

import Legos
from multiprocessing import Process

UPLOAD_FOLDER = 'data/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def func1():
  print('func1: starting')
  Legos.detectar()

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link')
def my_link():
  print ('I got clicked!')
  p1 = Process(target=func1)
  p1.start()
  p1.join()
  get_img()

  #time.sleep(3)
  with open("datos.txt", "r") as f:
    content = f.read()
  return render_template("index.html",sample=content)


@app.route("/getimage")
def get_img():
    return "resultado.jpg"

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "Legos.jpg"))
            return redirect(url_for('upload_file', name="filename"))
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
