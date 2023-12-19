from flask_app import app
from flask import request, render_template, redirect, session
from ..models.usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    #convertir contraseña a hash
    hash_password = bcrypt.generate_password_hash(request.form['contrasena'])
    print(hash_password)
    data = {
        'nombre' : request.form['nombre'],
        'apellido': request.form['apellido'],
        'edad': int(request.form['edad']),
        'fecha_nacimiento' : request.form['fecha_nacimiento'],
        'contrasena' : hash_password
    }
    print(data)
    nuevo_usuario = Usuario(data)
    errores = nuevo_usuario.validar_campos()

    if errores:
        return render_template('registro.html', errores=errores)
    else:
        resultado = Usuario.save(data)
        print(resultado)
        session['id'] = resultado
        return redirect('dashboard')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


