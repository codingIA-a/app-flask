from flask_app import app
from flask import request, render_template, redirect, session
from ..models.usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('registro.html')

#renderizar plantilla de inicio de sesión
@app.route('/login_form')
def formulario_login():
    return render_template('iniciar_sesion.html')


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
        'contrasena' : hash_password,
        'email': request.form['email']
    }
    print(data)
    nuevo_usuario = Usuario(data)
    errores = nuevo_usuario.validar_campos()

    if errores:
        return render_template('registro.html', errores=errores)
    else:
        resultado = Usuario.save(data)
        print(resultado)
        session['user_id'] = resultado
        return redirect('dashboard')

#iniciar sesión
@app.route('/iniciar_sesion', methods=['POST'])
def inciar_sesion():
    usuario = Usuario.get_by_email(request.form)
    if not usuario:
        print('Invalid Email')
        return redirect('/login_form')
    
    if  not bcrypt.check_password_hash(usuario.contrasena, request.form['contrasena']):
        print('Invalid password')
        return redirect('/login_form')
    session['user_id'] = usuario.email
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    print('Cerrando sesión...')
    return redirect('/')
