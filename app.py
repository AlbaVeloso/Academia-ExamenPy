from flask import Flask,render_template,request,redirect,url_for,session,flash
import pymysql
import db

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def index():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',alumnos=alumnos)

@app.route('/alumnos')
def mostrar_alumnos():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('alumnos.html', alumnos=alumnos)

@app.route('/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellidos']
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO alumnos (nombre, apellidos)
            VALUES (%s, %s)
        ''', (nombre, apellido))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Alumno registrado con éxito.', 'success')

        return redirect(url_for('registrar_alumno'))
    
    return render_template('registrar_alumno.html')


@app.route('/asignar_calificaciones/<int:idalumno>', methods=['GET', 'POST'])
def asignar_calificaciones(idalumno):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumnos WHERE idalumno = %s', (idalumno,))
    alumno = cursor.fetchone()

    if alumno is None:
        cursor.close()
        conn.close()
        return "Alumno no encontrado", 404
    
    cursor.execute('SELECT * FROM asignaturas')
    asignaturas = cursor.fetchall()

    if request.method == 'POST':
        asignatura_id = request.form['asignatura']
        nota = request.form['nota']
        cursor.execute(''' 
            INSERT INTO calificaciones (idalumno, idasignatura, calificacion)
            VALUES (%s, %s, %s)
        ''', (idalumno, asignatura_id, nota))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('mostrar_calificaciones', idalumno=idalumno))

    cursor.close()
    conn.close()
    return render_template('asignar_calificaciones.html', alumno=alumno, asignaturas=asignaturas)


@app.route('/calificaciones')
def mostrar_calificaciones():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT a.nombre AS alumno_nombre, asg.nombre AS asignatura_nombre, c.calificacion
    FROM calificaciones c
    JOIN alumnos a ON c.idalumno = a.idalumno
    JOIN asignaturas asg ON c.idasignatura = asg.idasignatura
    ''')
    calificaciones = cursor.fetchall()
    
    cursor.close()
    conn.close()
    

    return render_template('calificaciones_alumnos.html', calificaciones=calificaciones)



if __name__ == '__main__':
    app.run(debug=True)
