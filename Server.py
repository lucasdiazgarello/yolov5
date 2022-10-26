import os
import time

from flask import Flask, render_template, url_for, request, flash, redirect
import subprocess
import sys

from requests import session
from werkzeug.utils import secure_filename

import Legos
from multiprocessing import Process

IMAGE_UPLOAD = 'data/images'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
blocks = []
BloquesCargados = "Bloques no procesados"
FotoCargada = False
class Resultado:

    def __init__(self, titulo, direccionfoto, direcciondesc):
        self.titulo = titulo
        self.direccionfoto = direccionfoto
        self.direcciondesc = direcciondesc

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
    return render_template('subir.html', hay=BloquesCargados,foto=UPLOAD_FOLDER+'/' + BloquesCargados +'.png')


@app.route('/my-link')
def my_link():
    global blocks
    global BloquesCargados
    print('I got clicked!')
    p1 = Process(target=func1)
    p1.start()
    p1.join()
    get_img()
    piezas = Legos.contar("datos.csv")
    blocks = piezas.copy()
    BloquesCargados = "Bloques procesados"
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
    global BloquesCargados
    if request.method == 'POST':
        if BloquesCargados:
            aux = request.form['Titulo']
            titulo = aux + ".txt"
            titulo1 = aux + ".jpg"
            titulocsv = aux + ".csv"
            nombre = request.form['Nombre']
            desc = request.form['Descripcion']
            print(blocks)
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

                elementos = ''.join(blocks)
                with open(dire + "/" + titulocsv, mode='w') as bloques:
                    bloques.write(elementos)

                return redirect(url_for('upload_file', name="filename"))
        else:
            flash("Bloques no cargados", 'error')
    return render_template('subir.html', hay=BloquesCargados,foto=UPLOAD_FOLDER+BloquesCargados +'.png')


@app.route('/listar', methods=['GET', 'POST'])
def mostrarimagenes():
    if request.method == 'POST':
        resultados = [Resultado]
        carpeta = request.form.get('seleccion')
        print(carpeta)
        direccion = 'static/images/' + carpeta + '/'
        datos = os.listdir(direccion)
        for n in range(len(datos)):
            dire = direccion + datos[n]
            if ".txt" in datos[n]:
                with open(dire,mode='r')as f:
                    desc = f.read()
                foto = dire.replace('txt','jpg')
                titulo = datos[n].replace('.txt','')
            resu=Resultado(titulo,foto,desc)
            resultados.append(resu)
        return render_template("coleccion.html", resultados=resultados)


@app.route('/colecciones')
def listar():
    archivos = os.listdir('static/images/')
    carpetas = []
    for n in range(len(archivos)):
        if not ".jpg" in archivos[n] and not ".png" in archivos[n]:
            carpetas.append(archivos[n])

    return render_template('colecciones.html', opciones=carpetas)



@app.route('/buscar')
def buscar():
    archivos = os.listdir('static/images/')
    carpetas = []
    resultados = [Resultado]
    for n in range(len(archivos)):
        if not ".jpg" in archivos[n]:
            carpetas.append(archivos[n])

    for n in range(len(carpetas)):
        aux = os.listdir(UPLOAD_FOLDER + '/' + carpetas[n] + '/')
        for i in range(len(aux)):
            if '.csv' in aux[i]:
                direccion = UPLOAD_FOLDER + '/' + carpetas[n] + '/' + aux[i]

                if Legos.comparar(direccion,blocks):
                    with open(direccion.replace('.csv','.txt'), mode='r') as f:
                        desc=f.read()
                    resu = Resultado(aux[i].replace('.csv',''),direccion.replace('.csv','.jpg'),desc)
                    resultados.append(resu)
    return render_template('resultado.html', resu=resultados)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
