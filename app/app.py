from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Crear instancia
app = Flask(__name__)
app.secret_key = '789456123'
# Configurar la conexión
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024"
)

cursor = db.cursor()

@app.route('/password/<contraencrip>')
def encriptarcontra(contraencrip):
    #generar un hash de la contraseña
    #encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    encriptar= generate_password_hash(contraencrip)
    value= check_password_hash(encriptar,contraencrip)
    
    #return "Encriptado:{0} | coincide:{1}".format(encriptar,value)
    return value

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')
        
        cursor =db.cursor()
        cursor.execute("SELECT usup, pass FROM persona WHERE usup = %s",(username,))
        usuarios = cursor.fetchone()
        
        if usuarios or check_password_hash(usuarios[1], password):
            session['usuario'] = username
            return redirect(url_for('lista'))
        else:
            print("Credenciales invalidas")
            print("Credenciales invalidas. Por favor intentelo de nuevo")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
          #Eliminar el usuario de la sesión
          session.pop['usuario', None]
          return redirect/url_for(('login'))

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
       
       #Encriptar la contraseña
       encryptpassword = generate_password_hash(Password)
       
       cursor=db.cursor()
       cursor.execute( "SELECT * FROM persona WHERE usup = %s OR email = %s", (Usuario, email))
       existing_user = cursor.fetchone()
       
       if existing_user:
           print('El usuario o correo ya esta registrado.')
           return render_template('Registrar.html')
    
        # Insertar datos a la tabla de mysql
      
       cursor.execute("INSERT INTO persona(nombrep, apellidop, email, dirp, tel, usup, pass) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (Nombres,Apellidos,email,Direccion, Telefono, Usuario, encryptpassword))
       db.commit()

            
       return redirect(url_for('login'))  # Redirigir a la página principal
    #return redirect(url_for('Registrar usuario'))

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
    cursor.execute('DELETE FROM persona WHERE polper=%s', (id,))
    db.commit()
    cursor.close()

    return redirect(url_for('lista'))
        
# Ejecutar app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola

