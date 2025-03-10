from flask import Flask,render_template,request,redirect,url_for, session
import pymysql

app = Flask(__name__)
app.secret_key="123456"

@app.route('/login',methods=['GET'])
def index():
    return render_template("index.html")

#recibir dos parametros nombre y edad
@app.route('/saludo/<nombre>/<int:edad>')
def prueba(nombre,edad):
    if(edad<18):
        return "Hola "+nombre+" eres menor de edad"
    else:
        return "Hola "+nombre+" eres mayor de edad"

#login post
@app.route('/login',methods=['POST'])
def login():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    conexion = pymysql.connect(host='localhost', user='root', password='', db='tiendamvc')
    try:
        with conexion.cursor() as cursor:
            #creamos la consulta
            consulta = "SELECT * FROM user WHERE username=%s AND password=%s"
            datos=(username,password)
            cursor.execute(consulta,datos)
            resultados = cursor.fetchone()
        if(len(resultados)>0):
            session["username"]=username
            return redirect(url_for('admin'))
        else:
            return render_template("index.html",mensaje="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al consultar: ", e)
    finally:
        conexion.close()
        print("Conexion cerrada")
    

    
    
@app.route('/admin',methods=['GET'])
def admin():
    if "username" in session:
        return render_template("admin/admin.html")
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':    
    app.run(debug=True,port=80)
    