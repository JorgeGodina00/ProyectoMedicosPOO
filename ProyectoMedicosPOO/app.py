from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps


app= Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWWORD']=""
app.config['MYSQL_DB']="medicos_poo_v2"


mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


#LOGIN
@app.route('/acceso-login', methods = ['POST'])
def login():
        __rfc = request.form['txtRFC']
        __pass = request.form['txtPass']
        
        cur=mysql.connection.cursor()
        print("conexion a la BD exitosa")
        consulta = "SELECT * FROM medicos WHERE RFC = %s AND Contraseña = %s"
        cur.execute(consulta, (__rfc,__pass))
        resultado = cur.fetchone()
        
        if resultado is not None:
            Rol = "select Rol from medicos where RFC = %s AND Contraseña = %s"
            cur.execute(Rol,  (__rfc,__pass))
            rol_resultado = cur.fetchone()
            
            if rol_resultado is not None and rol_resultado[0] == "Administrador":
                session['RFC'] = __rfc
                return render_template('admindash.html')
            else:
                session['RFC'] = __rfc
                return render_template('usuindex.html')
        else:
            flash('RFC o contraseña incorrectos. Intente nuevamente.')
            return redirect(url_for('index'))
       
       
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'RFC' not in session:
            flash('Debe iniciar sesión para acceder a esta página.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
def admindash():
        return render_template('admindash.html')

@app.route('/menu')
@login_required
def menuusu():
    return render_template('usuindex.html')


@app.route('/salir')
def salir():
    session.pop('RFC', None)
    return redirect(url_for('index'))

@app.route('/registrarmedico', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        VRFC = request.form['txtRFC']
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VCed = request.form['txtCed']
        VCorr = request.form['txtCorr']
        VRol = request.form['txtRol']
        VPass = request.form['txtPass']
       
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO medicos (RFC, Nombre, Apellido1, Apellido2, Cedula, Correo, Rol, Contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (VRFC, VNom, VAP, VAM, VCed, VCorr, VRol, VPass))
        mysql.connection.commit()
        flash('Médico agregado correctamente')
        return render_template('admindash.html')

    return render_template('admindash.html')

@app.route('/consultarmedicos')
@login_required
def consultarmedicos():
    curSelect = mysql.connection.cursor()
    curSelect.execute('SELECT * FROM medicos')
    consulta = curSelect.fetchall()
    return render_template('consultarmedicos.html', listMedicos = consulta)

@app.route('/agregarpacientes')
@login_required
def addpacientes():
    return render_template('agregarpacientes.html')

@app.route('/guardarpaciente', methods=['POST'])
@login_required
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

@app.route('/lista')
def buscar():
    curSelect = mysql.connection.cursor()
    curSelect.execute('SELECT * FROM pacientes')
    consulta = curSelect.fetchall()
    return render_template('consultarpacientes.html', listPacientes = consulta)

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

@app.route('/borrar/<id>')
def borrar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('SELECT * FROM pacientes WHERE Id_paciente = %s', (id,))
    consulId = curEditar.fetchone()
    return render_template('eliminarpaciente.html', paciente=consulId)

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':
        curEli = mysql.connection.cursor()
        curEli.execute('DELETE FROM pacientes WHERE Id_paciente=%s', (id,))
        mysql.connection.commit()
        flash('El Paciente ha sido eliminado :)')
    return render_template('templateusu.html')


if __name__ == '__main__':
    app.secret_key='mysecretkey'
    app.run(port=5000, debug=True, threaded = True)