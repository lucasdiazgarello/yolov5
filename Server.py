import os
import time

from flask import Flask, render_template, url_for, request, flash, redirect
import subprocess
import sys

from werkzeug.utils import secure_filename

import Legos
from multiprocessing import Process
IMAGE_UPLOAD = 'data/images'
UPLOAD_FOLDER = 'static/images'
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


@app.route('/subir')
def subir():
    return render_template('subir.html')


@app.route('/my-link')
def my_link():
    print('I got clicked!')
    p1 = Process(target=func1)
    p1.start()
    p1.join()
    get_img()
    piezas = Legos.contar()
    # print(piezas)
    with open("datos.txt", "r") as f:
        content = f.read()
    return render_template("index.html", sample=content, negrog=piezas[0], negroc=piezas[1], blancog=piezas[2],
                           blancoc=piezas[3], rojog=piezas[4], rojoc=piezas[5], azulg=piezas[6], azulc=piezas[7],
                           amarillog=piezas[8], amarilloc=piezas[9])


# black white red blue yellow

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
            file.save(os.path.join(IMAGE_UPLOAD, "Legos.jpg"))
            return redirect(url_for('upload_file', name="filename"))
    return render_template('index.html')


@app.route('/subircreacion', methods=['GET', 'POST'])
def subircreacion():
    if request.method == 'POST':
        aux = request.form['Titulo']
        titulo = aux + ".txt"
        titulo1 = aux + ".jpg"
        nombre = request.form['Nombre']
        desc = request.form['Descripcion']
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
            dire = UPLOAD_FOLDER + "/" + nombre
            if not os.path.exists(dire):
                os.mkdir(dire)
            file.save(os.path.join(dire, titulo1))
            with open(dire + "/" + titulo, mode='w') as texto:
                texto.write(desc)
            return redirect(url_for('upload_file', name="filename"))
    return render_template('subir.html')


@app.route('/mostrar')
def mostrarimagenes():
    pics = os.listdir('static/images/Felipe/')
    picstmp = pics.copy()
    for n in range(len(picstmp)):
        if ".txt" in picstmp[n]:
            pics.pop(n)
    return render_template("subir.html", pics=pics)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
