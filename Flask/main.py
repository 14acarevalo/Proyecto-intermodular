#Para aprender Flask tienes que tener en cuenta una serie de cosas

#Esto tiene que estar presente
from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL



#Esto tiene que estar presente
app = Flask(__name__)
app.secret_key = 'clave_secreta_flask'
#Conexion DB

#1 Genero configuración
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoIntermodular'

#2. Establezco conexion

mysql = MySQL(app)

#Como puedes observar en esta página, a la hora de crear rutas es necesario tener en cuenta los siguientes parametros:
@app.route('/')
def index():
    coches = [
        {'imagen_url': 'images/americano.jpg'},
        {'imagen_url': 'images/bmw.jpg'},
        {'imagen_url': 'images/citroen.jpg'},
        {'imagen_url': 'images/boda.jpg'},
        {'imagen_url': 'images/ford.jpg'},
        {'imagen_url': 'images/ranger.jpg'},
        {'imagen_url': 'images/vectra.jpg'},
        {'imagen_url': 'images/600.jpg'},


    ]
    return render_template('index.html', coches=coches)


@app.route('/inicio')
def inicio():
    coches = [
        {'imagen_url': 'images/americano.jpg'},
        {'imagen_url': 'images/bmw.jpg'},
        {'imagen_url': 'images/citroen.jpg'},
        {'imagen_url': 'images/boda.jpg'},
        {'imagen_url': 'images/ford.jpg'},
    ]
    return render_template('index.html', coches=coches)
 # Página de inicioPágina alternativa de inicio

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')  # Página de información

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/insertar-coche', methods=['GET', 'POST'])
def insertar_coche():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        anio = request.form['anio']
        dueno = request.form['dueno']
        kilometros = request.form['kilometros']
        motor = request.form['motor']
        telefono = request.form['telefono']
        password = request.form['password']

        # Ahora puedes insertar los datos sin la columna de imagen
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO vehiculos VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (marca, modelo, precio, ciudad, anio, dueno, kilometros, motor, telefono, password))
        mysql.connection.commit()

        flash('Has registrado el coche correctamente')
        return redirect(url_for('coches'))

    return render_template('crear_coche.html')

@app.route('/coches')
def coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculos ORDER BY id DESC")
    coches = cursor.fetchall()
    cursor.close()
    return render_template('coches.html', coches=coches)

@app.route('/mostrar-coches')
def mostrar_coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculos ORDER BY id DESC")
    coches = cursor.fetchall()
    cursor.close()
    return render_template('listar_coches.html', coches=coches)

@app.route('/coche/<coche_id>')
def coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE id=%s", (coche_id,))
    coche = cursor.fetchone()  # Usa fetchone() para un solo resultado
    cursor.close()

    if not coche:
        return "Coche no encontrado", 404

    return render_template('coche.html', coche=coche)

@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM vehiculos WHERE id=%s", (coche_id,))
    mysql.connection.commit()    
    cursor.close()

    flash ('Vehiculo eliminado')
    if not coche:
        return "Coche no encontrado", 404

    return redirect(url_for('coches'))

@app.route('/editar-coche/<coche_id>', methods=['GET', 'POST'])
def editar_coche(coche_id):

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        anio = request.form['anio']
        dueno = request.form['dueno']
        kilometros = request.form['kilometros']
        motor = request.form['motor']
        telefono = request.form['telefono']
        password = request.form['password']

        # Actualizar los datos del coche sin la columna de imagen
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE vehiculos
            SET marca = %s, modelo = %s, precio = %s, ciudad = %s, anio = %s, dueno = %s, kilometros = %s, motor = %s, telefono = %s, password = %s
            WHERE id = %s
        """, (marca, modelo, precio, ciudad, anio, dueno, kilometros, motor, telefono, password, coche_id))
        mysql.connection.commit()
        flash('Coche actualizado correctamente')
        return redirect(url_for('coches'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE id = %s", (coche_id,))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('crear_coche.html', coche=coche[0])


#Creamos las rutas para la opción evento:
#Hay que meter la opcion insertar, editar y borrar, la tabla ya esta creada y se llama eventos, dentro de proyectoflask que ya esta enlazada al principio en la conexión

#Insertar

@app.route('/insertar-evento', methods=['GET', 'POST'])
def insertar_evento():
    if request.method =="POST":
        nombreEvento = request.form['nombreEvento']
        direccionEvento = request.form['direccionEvento']
        organizadorEvento = request.form['organizadorEvento']
        participantesEvento = request.form['participantesEvento']
        ciudadEvento = request.form['ciudadEvento']
        telefonoEvento = request.form['telefonoEvento']

        #Metemos conexion con la base de datos y los diferentes parametros con los que vamos a trabajar    
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO eventos VALUES (NULL, %s, %s, %s, %s, %s, %s)", (nombreEvento, direccionEvento, organizadorEvento, participantesEvento, ciudadEvento, telefonoEvento))
        mysql.connection.commit()
         
        flash ('Evento creado correctamente')
        return redirect(url_for('mostrar_eventos'))

    return render_template('crear_evento.html')

@app.route('/mostrar-eventos')
def mostrar_eventos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eventos ")
    eventos = cursor.fetchall()
    cursor.close()
    
    return render_template('eventos.html', eventos=eventos)

@app.route('/listado-eventos')
def listado_eventos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eventos ")
    eventos = cursor.fetchall()
    cursor.close()
    
    return render_template('listar_eventos.html', eventos=eventos)

@app.route('/listar-evento/<evento_id>')
def listar_evento(evento_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eventos WHERE id = %s", (evento_id,))
    evento = cursor.fetchone()
    cursor.close()
    
    if not evento:
        return "Evento no encontrado"
    
    return render_template ("evento.html", evento=evento)

@app.route('/borrar-evento/<evento_id>')
def borrar_evento(evento_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Evento eliminado correctamente')  # Mensaje de confirmación
    
    return redirect(url_for('mostrar_eventos'))  # Redirige correctamente


@app.route('/editar-evento/<evento_id>', methods=['GET', 'POST'])
def editar_evento(evento_id):

    if request.method == 'POST':
        nombreEvento = request.form['nombreEvento']
        direccionEvento = request.form['direccionEvento']
        organizadorEvento = request.form['organizadorEvento']
        participantesEvento = request.form['participantesEvento']
        ciudadEvento = request.form['ciudadEvento']
        telefonoEvento = request.form['telefonoEvento']
        

        # Actualizar los datos del coche sin la columna de imagen
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE eventos
            SET nombreEvento = %s, direccionEvento = %s, organizadorEvento = %s, participantesEvento = %s, ciudadEvento = %s, telefonoEvento = %s
            WHERE id = %s
        """, (nombreEvento, direccionEvento, organizadorEvento, participantesEvento, ciudadEvento, telefonoEvento, evento_id))
        mysql.connection.commit()
        flash('Evento actualizado correctamente')
        return redirect(url_for('mostrar_eventos'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eventos WHERE id = %s", (evento_id,))
    evento = cursor.fetchall()
    cursor.close()

    return render_template('crear_evento.html', evento=evento[0])

@app.route('/insertar-usuario', methods=['GET', 'POST'])
def insertar_usuario():
    if request.method =="POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']

        #Metemos conexion con la base de datos y los diferentes parametros con los que vamos a trabajar    
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuario VALUES (NULL, %s, %s, %s, %s, %s)", (nombre, apellidos, telefono, email, password))
        mysql.connection.commit()
         
        flash ('Usuario creado correctamente')
        return redirect(url_for('login'))

    return render_template('crearUsuario.html')

# Credenciales de administrador
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "1234"

@app.route('/listado-usuarios')
def listar_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario ")
    usuarios = cursor.fetchall()
    cursor.close()
    
    return render_template('listar_usuario.html', usuarios=usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Recibir datos del formulario
        email = request.form['email']
        password = request.form['password']

        # Validar administrador
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user'] = 'admin'
            return render_template('menuAdmin.html')

        # Validar usuario normal
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email, password FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[1] == password:  # Validación de contraseña
            session['user'] = 'user'
            return render_template('menuUsuario.html')

        # Si las credenciales no coinciden
        return render_template('login.html', error="Credenciales incorrectas")

    # Mostrar el formulario de login (GET)
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('user') == 'admin':
        return "Bienvenido al panel de administrador"
    return redirect(url_for('login'))

@app.route('/menuUsuario')
def menu_usuario():
    return render_template('menuUsuario.html')

@app.route('/menuAdmin')
def menu_admin():
    return render_template('menuAdmin.html')

@app.route('/logout')
def logout():
    # Eliminar el usuario de la sesión
    session.pop('user', None)
    # Redirigir al usuario a la página de login
    return redirect(url_for('login'))
   

#Esto tiene que estar presente
if __name__=='__main__':
    app.run(debug=True)
    

