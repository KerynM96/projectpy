from flask import Flask,render_template
import mysql.connector

#Crear instancia 
app = Flask (__name__)

#configurar la conexion 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024" 
)

cursor = db.cursor()

@app.route('/') #crear ruta
def index():
    return render_template('index.html')

@app.route('/Registrar')
def registrar():
    return render_template('Registrar.html')
#ejecutar app 
if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True,port=5005) #debug para que me salgan los errores en consola 

#crear ruta 
