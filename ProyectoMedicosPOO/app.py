from flask import Flask
from flask import render_template, request, session, redirect, Response,url_for, flash 
from flask_mysqldb import MySQL, MySQLdb


app= Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWWORD']=""
app.config['MYSQL_DB']="medicospoo"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
     curSelect = mysql.connection.cursor()
     curSelect.execute('SELECT * FROM medicos')
     consulta = curSelect.fetchall()
     return render_template('admindash.html', listMedi = consulta)
 
@app.route("/agregarmedicos")
def agregaadmin():
     return render_template('guardarmedico.html')

#LOGIN
@app.route('/acceso-login', methods = ["GET", "POST"])
def login():
    
    if request.method == 'POST' and 'txtRFC' in request.form and 'txtPass':
        __rfc = request.form['txtRFC']
        __pass = request.form['txtPass']
        
        cur=mysql.connection.cursor()
        print("conexion a la BD exitosa")
        cur.execute('SELECT * FROM medicos WHERE rfc = %s AND pass = %s', (__rfc,__pass))
        account = cur.fetchone()
        
        if account:
            session['logueado'] = True
            session['rfc'] = account['rfc']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol'] == 1:
                return render_template('admindash.html')
            elif session['id_rol'] == 2:
                return render_template('usuindex.html')
        else:

            return render_template('index.html', mensaje = "Usuario O Contraseña Incorrectos")

@app.route('/salir')
def salir():
    return render_template('index.html')




if __name__ == '__main__':
    app.secret_key='mysecretkey'
    app.run(host = '0.0.0.0', port=5000, debug=True, threaded = True)