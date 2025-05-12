from pickle import STRING

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies)
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.config["JWT_SECRET_KEY"] = "jwt_clave_secreta"

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia según tu configuración
        database="gestión_de_residuos"
    )

# Ruta para registro y login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        accion = request.form['accion']
        cliente = request.form['cliente']
        password = request.form['contraseña']
        rol = request.form['rol']

        db = conectar_db()
        cursor = db.cursor()

        if accion == "registrar":
            # Verificar si el usuario ya existe
            cursor.execute('SELECT * FROM login WHERE cliente = %s', (cliente,))
            existe = cursor.fetchone()

            if existe:
                flash("El usuario ya existe. Intenta con otro nombre.")
            else:
                # Insertar nuevo usuario en la base de datos
                cursor.execute('INSERT INTO login (cliente, contraseña, rol) VALUES (%s, %s, %s)',
                               (cliente, password, rol))
                db.commit()
                flash("Registro exitoso. Ahora puedes iniciar sesión.")

            cursor.close()
            db.close()
            return redirect(url_for('login'))

        elif accion == "iniciar_sesion":
            cursor.execute('SELECT * FROM login WHERE cliente = %s AND contraseña = %s AND rol = %s',
                           (cliente, password, rol))
            user = cursor.fetchone()
            cursor.close()
            db.close()

            if user:
                # En lugar de un diccionario, usa una cadena simple para la identidad
                access_token = create_access_token(identity=cliente)  # Solo el nombre de usuario
                session['cliente'] = cliente
                session['rol'] = rol

                if rol == 'admin':
                    response = redirect(url_for('admin'))
                elif rol == 'usuario':
                    response = redirect(url_for('tabla'))
                else:
                    flash("Rol no válido.")
                    return redirect(url_for('login'))

                set_access_cookies(response, access_token)
                return response
            else:
                flash('Usuario o contraseña incorrectos.')

    return render_template('login.html')


# Ruta para mostrar la tabla (solo para usuarios)
@app.route("/tabla")
@jwt_required()
def tabla():
    cliente = session.get('cliente')
    rol = session.get('rol')

    if rol != "usuario":
        flash("No tienes permiso para acceder a esta sección.")
        return redirect(url_for('login'))

    return render_template("tabla.html", cliente=cliente)

# Ruta para administración (solo para administradores)
@app.route("/admin")
@jwt_required()
def admin():
    cliente = session.get('cliente')
    rol = session.get('rol')

    if rol != "admin":
        flash("No tienes permiso para acceder a esta sección.")
        return redirect(url_for('login'))

    return render_template("admin.html", cliente=cliente)
# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    flash("Sesión cerrada.")
    response = redirect(url_for('login'))
    unset_jwt_cookies(response)
    return response

if __name__ == "__main__":
    app.run(debug=True)
