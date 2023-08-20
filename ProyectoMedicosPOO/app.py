from flask import Flask, render_template, request, redirect, url_for, flash #Importacion de librerias
from flask_mysqldb import MySQL
import bcrypt


#iniciar servidor Flask
#configuracion de BD
app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWWORD']=""
app.config['MYSQL_DB']="medicos"

app.secret_key='mysecretkey'

mysql = MySQL(app)

#Declaracion de la ruta
#Ruta index
#La ruta se compone de la ruta y su funcion
@app.route('/')
def index():
    return render_template('templateusu.html')





@app.route('/agregarpacientes')
def addpacientes():
    return render_template('pacientes.html')






#Registro de pacientes
@app.route('/guardarpaciente', methods=['POST'])
def newpaciente():
    if request.method == 'POST':
        rfc= request.form['rfctxt']
        nombre= request.form['nomtxt']
        apellidop= request.form['aptxt']
        apellidom= request.form['amtxt']
        fecha_nacimiento= request.form['datetxt']
        enfermedades= request.form['entxt']
        alergias= request.form['altxt']
        antecedentes= request.form['anttxt']
        #print()    
        CS = mysql.connection.cursor() #Variable de tipo cursor que contiene las herramientas paara realizar los querys
        CS.execute("INSERT INTO pacientes (RFC_MED, Nombre, apellido1, apellido2, Fecha_nacimiento, Enfermedades, Alergias, Antecedentes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (rfc, nombre, apellidop, apellidom, fecha_nacimiento, enfermedades, alergias, antecedentes))
        mysql.connection.commit()
    flash('Se ha hecho el registro correctamente')    
    return redirect(url_for('index'))

#editar pacientes
@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('SELECT * FROM pacientes WHERE Id_paciente = %s', (id,))
    consulId = curEditar.fetchone()
    return render_template('actualizarpaciente.html', paciente=consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        rfc= request.form['rfctxt']
        nombre= request.form['nomtxt']
        apellidop= request.form['aptxt']
        apellidom= request.form['amtxt']
        fecha_nacimiento= request.form['datetxt']
        enfermedades= request.form['entxt']
        alergias= request.form['altxt']
        antecedentes= request.form['anttxt']
        CS = mysql.connection.cursor() #Variable de tipo cursor que contiene las herramientas paara realizar los querys
        CS.execute('UPDATE pacientes SET RFC_MED=%s, Nombre=%s, apellido1=%s, apellido2=%s, Fecha_nacimiento=%s, Enfermedades=%s, Alergias=%s, Antecedentes=%s WHERE Id_paciente=%s', (rfc, nombre, apellidop, apellidom, fecha_nacimiento, enfermedades, alergias, antecedentes, id))
        mysql.connection.commit()
    flash('Se ha hecho el registro correctamente')    
    return render_template('templateusu.html')





#Borrar pacientes
@app.route('/borrar/<id>')
def borrar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('SELECT * FROM pacientes WHERE Id_paciente = %s', (id,))
    consulId = curEditar.fetchone()
    return render_template('eliminarpaciente.html', album=consulId)

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':
        curEli = mysql.connection.cursor()
        curEli.execute('DELETE FROM pacientes WHERE Id_paciente=%s', (id,))
        mysql.connection.commit()
        flash('El Paciente ha sido eliminado :)')
    return render_template('templateusu.html')

#Lista Pacientes
@app.route('/lista')
def buscar():
    curSelect = mysql.connection.cursor()
    curSelect.execute('SELECT * FROM pacientes')
    consulta = curSelect.fetchall()
    return render_template('listapacientes.html', listPacientes = consulta)



#Registro de Médicos






if __name__ == '__main__':
    app.run(port=5000, debug=True)