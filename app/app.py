from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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

@app.route('/')  # Crear ruta
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    usuario = cursor.fetchall()

    return render_template('index.html' ,usuario=usuario)

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
    
        # Insertar datos a la tabla de mysql
       cursor.execute("INSERT INTO personas(nombrep,apellidop,emailp,dirp,telp,usup,passp) VALUES (%s,%s,%s,%s,%s,%s,%s)",(Nombres,Apellidos,email,Direccion,Telefono,Usuario,Password))
       db.commit()

            
       return redirect(url_for('registrar_usuario'))  # Redirigir a la página principal
    return render_template("Registrar.html")

# Ejecutar app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola

