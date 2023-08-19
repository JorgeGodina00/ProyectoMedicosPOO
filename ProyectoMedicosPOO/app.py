from flask import Flask, render_template, request, redirect, url_for, flash #Importacion de librerias
from flask_mysqldb import MySQL


#iniciar servidor Flask
#configuracion de BD
app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWWORD']=""
app.config['MYSQL_DB']="medicospoo"

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



@app.route('/diagnostico', methods=['POST'])
def newdagnostico():
    if request.method == 'POST':
        Vnombre= request.form['nontxt']
        Vdate= request.form['fdntxt']
        Venfermedades= request.form['enftxt']
        Valergias= request.form['altxt']
        Vantesedentes= request.form['anttxt']
        Vdiagnostico= request.form['diagtxt']
        #print()
        CS = mysql.connection.cursor() #Variable de tipo cursor que contiene las herramientas paara realizar los querys
        CS.execute("INSERT INTO diagnostico (nombre, fecha_nacimiento, enfermedades, alergias, antecedentes, diagnostico) VALUES (%s, %s, %s,%s, %s, %s)", (Vnombre, Vdate, Venfermedades, Valergias, Vantesedentes, Vdiagnostico))
        mysql.connection.commit()
    flash('Se ha hecho el registro correctamente')    
    return redirect(url_for('index'))


@app.route('/guardarpaciente', methods=['POST'])
def newmedico():
    if request.method == 'POST':
        Vnombre= request.form['nomtxt']
        Vapellidop= request.form['aptxt']
        Vapellidom= request.form['amtxt']
        Vfecha_nacimiento= request.form['datetxt']
        Venfermedades= request.form['datetxt']
        Valergias= request.form['alttxt']
        Vantecedentes= request.form['roltxt']
        Vdiagnostico= request.form['passtxt']
        #print()    
        CS = mysql.connection.cursor() #Variable de tipo cursor que contiene las herramientas paara realizar los querys
        CS.execute("INSERT INTO medicos (nombre, apellido_paterno, apellido_materno, rfc, cedula, correo, rol, pass) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)", (Vnombre, Vapellidop, Vapellidom))
        mysql.connection.commit()
    flash('Se ha hecho el registro correctamente')    
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(port=5000, debug=True)