from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import base64
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
        sql = ("SELECT usup, pass FROM persona WHERE usup = %s")
        cursor.execute(sql,(username,))
        usuarios = cursor.fetchone()
        
        if usuarios or check_password_hash(usuarios['pass'], password):
            session['usuario'] = username ['usup']
            session['rol'] = ['roles']
            
            if usuarios['roles'] == 'administrator':
                return redirect(url_for('lista'))
            else:
                return redirect(url_for('actualizar'))
        else:
            print("Credenciales invalidas")
            print("Credenciales invalidas. Por favor intentelo de nuevo")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Eliminar el usuario de la sesión
    session.pop('usuario', None)
    print("La sesión se ha cerrado")
    return redirect(url_for('login'))


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

@app.route('/registro/<int:id>',methods=['GET', 'POST'])
def registro_cancion():
    cursor = db.cursor()
    if request.method == 'POST':
        idcan = request.form.get('id_can')
        tituloc = request.form.get('titulo')
        artistac = request.form.get('artista')
        generoc = request.form.get('genero')
        precioc = request.form.get('precio')
        duracionc = request.form.get('duracion')
        lanzamientoc = request.form.get('lanzamiento')
        imgc = request.files['img']
        
        imagenblob = imgc.read()
        
        cursor = db.cursor()

        
        cursor.execute("INSERT INTO canciones (titulo, artista, genero, precio, duracion, lanzamiento,img) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                       (idcan,tituloc, artistac, generoc, precioc, duracionc,lanzamientoc,imgc,imagenblob))
        db.commit()
        return redirect(url_for('registro_cancion'))
    return render_template("Registro.html")

#Enlaazar-actualizar 
@app.route('/actualizar/<int:id>',methods=['GET', 'POST'])   
def editar_cancion(id): 
    cursor = db.cursor()
    if request.method == 'POST':
        tituloc = request.form.get('titulo')
        artistac = request.form.get('artista')
        generoc = request.form.get('genero')
        precioc = request.form.get('precio')
        duracionc = request.form.get('duracion')
        lanzamientoc = request.form.get('lanzamiento')
        
        sql = "UPDATE canciones SET titulo=%s, artista=%s, genero=%s, precio=%s,duracion=%s,lanzamiento=%s, where id_can=%s"
        cursor.execute(sql,(tituloc, artistac, generoc, precioc, duracionc,lanzamientoc,id,))
        db.commit()
        return redirect(url_for('lista'))
     
    else:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_canciones=%s' ,(id,))
        data = cursor.fetchall()

        return render_template('actualizar.html', canciones=data[0])

@app.route('/mostrarcanciones' , methods=["GET" , "POST"])
def mostrar_canciones():
    cursor = db.cursor()
    cursor.execute('SELECT titulo,artista,genero,precio,duracion,lanzamiento,img FROM canciones')
    canciones = cursor.fetchall()

    if canciones:
     cancioneslist = []
     
     for cancion in canciones:
        imagen = base64.b64encode(cancion[6]).decode('utf-8')
        cancioneslist.append ({
            'titulo':cancion[0],
            'artista':cancion[1],
            'genero':cancion[2],
            'precio':cancion[3],
            'duracion':cancion[4],
            'lanzamiento':cancion[5],
            'img':imagen   
        })
        
        return render_template("canciones.html", cancion=cancioneslist)
    else: 
        return print ("canciones.html")   
    
    
# Ejecutar app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola

