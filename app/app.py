from flask import *
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
def index():
    return render_template('index.html')

@app.route('/Registrar', methods=['POST'])
def registrar_usuario():
    Nombres = request.form['nombre']
    Apellidos = request.form['apellido']
    email = request.form['email']
    Direccion = request.form['direccion']
    Telefono = request.form['telefono']
    Usuario = request.form['usuario']
    Password = request.form['password']
    
    # Insertar datos a la tabla de mysql
    cursor.execute("INSERT INTO personas(nombrep, apellidop, emailp, dirp, telp, usup, passp) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, email, Direccion, Telefono, Usuario, Password))
    db.commit()
    
    return redirect(url_for('index'))

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola
