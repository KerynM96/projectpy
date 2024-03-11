from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import mysql.connector
import bcrypt

# Crear instancia
app = Flask(__name__)

# Configurar la conexión
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024"
)

cursor = db.cursor()

def encriptarcontra(contraencrip):
    
    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    
    return encriptar

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')
        
        cursor =db.cursor()
        cursor.execute('SELECT * FROM persona where usup = %s',(username,))
        usuarios = cursor.fetchone()
        
        if usuarios and bcrypt.check_password_hash(usuarios[7],password):
            session['usuario'] = username
            return redirect(url_for('lista'))
        else:
            error = 'credenciales invalidas. por favor intente de nuevo'
            return render_template('login.html', error=error)
        
    return render_template('login.html')
        

@app.route('/')  # Crear ruta
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM persona')
    usuario = cursor.fetchall()

    return render_template('index.html',usuario=usuario)

@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
       Nombres = request.form.get('nombre')
       Apellidos = request.form.get('apellido')
       email = request.form.get('email')
       Direccion = request.form.get('direccion')
       Telefono = request.form.get('telefono')
       Usuario = request.form.get('usuario')
       Password = request.form.get('password')
       
       encryptpassword = encriptarcontra(Password)
       
    
        # Insertar datos a la tabla de mysql
       cursor.execute("INSERT INTO persona(nombrep, apellidop, email, dirp, tel, usup, pass) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, email, Direccion, Telefono, Usuario, encryptpassword))
       db.commit()

            
       return redirect(url_for('lista'))  # Redirigir a la página principal
    return render_template("Registrar.html")

@app.route('/editar/<int:id>',methods=['GET', 'POST'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombreper = request.form.get('nombreper')
        apellidoper = request.form.get('apellidoper')
        emailper = request.form.get('emailper')
        dirper = request.form.get('dirper')
        telper = request.form.get('telper')
        usuper = request.form.get('usuper')
        passper = request.form.get('passper')

        sql = "UPDATE persona SET nombrep=%s, apellidop=%s, email=%s, dirp=%s, tel=%s, usup=%s, pass=%s WHERE polper=%s"
        cursor.execute(sql,(nombreper,apellidoper,emailper, dirper,telper,usuper,passper,id,))
        db.commit()
        return redirect(url_for('lista'))
    
    else: 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM persona WHERE polper=%s' ,(id,))
        data = cursor.fetchall()

        return render_template('editar.html', personas=data[0])

@app.route("/eliminar/<int:id>", methods=['GET', 'POST'])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombreper = request.form.get('nombreper')
        apellidoper = request.form.get('apellidoper')
        emailper = request.form.get('emailper')
        dirper = request.form.get('dirper')
        telper = request.form.get('telper')
        usuper = request.form.get('usuper')
        passper = request.form.get('passper')
        
    cursor.execute('DELETE FROM persona WHERE polper=%s', (id,))

    return redirect(url_for('lista'))
        
# Ejecutar app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola

