import os
import time

from flask import Flask, render_template, url_for, request, flash, redirect, session
import subprocess
import sys

from flask_session import Session
from werkzeug.utils import secure_filename

import Legos
from multiprocessing import Process

IMAGE_UPLOAD = 'static'
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
    Legos.detectar(session['name'], IMAGE_UPLOAD+"/"+ session['name'] + '.jpg')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/login", methods=["POST", "GET"])
def login():
    # if form is submited
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        if os.path.exists(IMAGE_UPLOAD + '/' + session['name'] + 'resultado.jpg'):
            global BloquesCargados
            BloquesCargados = "Bloques procesados"
        # redirect to the main page
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():

    global BloquesCargados
    BloquesCargados = "Bloques no procesados"
    if os.path.exists(IMAGE_UPLOAD + '/' + session['name'] + 'resultado.jpg'):
        os.remove(IMAGE_UPLOAD + '/' + session['name'] + 'resultado.jpg')
    if os.path.exists(IMAGE_UPLOAD + '/' + session['name'] + '.jpg'):
        os.remove(IMAGE_UPLOAD + '/' + session['name'] + '.jpg')
    session["name"] = None
    return redirect("/login")


@app.route("/")
def index():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    if os.path.exists(IMAGE_UPLOAD + '/' + session['name'] + 'resultado.jpg'):
        global BloquesCargados
        BloquesCargados = "Bloques procesados"
    return render_template('index.html')


# @app.route('/')
# def index():
#   return render_template('index.html')


@app.route('/subir')
def subir():
    return render_template('subir.html', hay=BloquesCargados, foto=UPLOAD_FOLDER + '/' + BloquesCargados + '.png')


@app.route('/my-link')
def my_link():
    global blocks
    global BloquesCargados
    print('I got clicked!')
    p1 = Process(target=func1)
    p1.start()
    p1.join()
    get_img()
    piezas = Legos.contar("static/"+session['name']+".csv")
    session['piezas']=piezas
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
    return session["name"]+"resultado.jpg"


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
            file.save(os.path.join(IMAGE_UPLOAD, session['name'] + ".jpg"))
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
            print("ARRANCA ACA")

            print("titulo"+aux)
            #nombre = request.form['Nombre']
            nombre = session['name']
            desc = request.form['Descripcion']
            #print("nombre"+nombre)
            #print("descripcion"+desc)
            #print(blocks)
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
                bloques = str(session['piezas'])
                print("LOS BLOQUES")
                print(bloques)
                elementos = ''.join(bloques)
                print("los elementos")
                print(elementos)
                print(dire + "/" + titulocsv)
                with open(dire + "/" + titulocsv, mode='w') as bloques:
                    bloques.write(elementos)

                return redirect(url_for('upload_file', name="filename"))
        else:
            flash("Bloques no cargados", 'error')
    return render_template('subir.html', hay=BloquesCargados, foto=UPLOAD_FOLDER + BloquesCargados + '.png')


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
                with open(dire, mode='r') as f:
                    desc = f.read()
                foto = dire.replace('txt', 'jpg')
                titulo = datos[n].replace('.txt', '')
                resu = Resultado(titulo, foto, desc)
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
        if not ".jpg" in archivos[n] and not ".png" in archivos[n]:
            carpetas.append(archivos[n])

    for n in range(len(carpetas)):
        aux = os.listdir(UPLOAD_FOLDER + '/' + carpetas[n] + '/')
        for i in range(len(aux)):
            if '.csv' in aux[i]:
                direccion = UPLOAD_FOLDER + '/' + carpetas[n] + '/' + aux[i]
                if Legos.comparar(direccion, blocks):
                    with open(direccion.replace('.csv', '.txt'), mode='r') as f:
                        desc = f.read()
                    resu = Resultado(aux[i].replace('.csv', ''), direccion.replace('.csv', '.jpg'), desc)
                    resultados.append(resu)
    return render_template('resultado.html', resu=resultados)


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')
