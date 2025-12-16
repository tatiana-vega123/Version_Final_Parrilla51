from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from __init__ import mysql, mail, serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import uuid
import socket

# ⏱️ Timeout global para evitar bloqueos SMTP en Railway
socket.setdefaulttimeout(5)

# -------------------- BLUEPRINT --------------------
auth_bp = Blueprint('auth', __name__)

# -------------------- PÁGINA PRINCIPAL (HOME) --------------------
@auth_bp.route('/')
def home():
    return render_template("index.html")


# -------------------- LOGIN --------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['contraseña'], password):
            if user['estado'].lower() != 'activo':
                flash("⚠️ Cuenta inactiva. Revisa tu correo para activarla", "warning")
                return redirect(url_for('auth.login'))

            session['logueado'] = True
            session['id_usuario'] = user['id_usuario']
            session['nombre'] = user['nombre']
            session['apellido'] = user['apellido']
            session['rol'] = user['rol']

            flash(f"✅ Bienvenido {user['nombre']} {user['apellido']}", "success")

            if session['rol'] == 'administrador':
                return redirect(url_for('admin.admin_dashboard'))
            elif session['rol'] == 'empleado':
                return redirect(url_for('empleado.empleado_dashboard'))
            elif session['rol'] == 'cliente':
                return redirect(url_for('dashboard.cliente_dashboard'))
        else:
            flash("❌ Correo o contraseña incorrectos", "danger")

    return render_template("login.html")


# -------------------- REGISTRO --------------------
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        existe = cur.fetchone()

        if existe:
            flash("⚠️ Este correo ya está registrado", "warning")
            cur.close()
            return redirect(url_for('auth.registro'))

        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        password = generate_password_hash(request.form['password'])
        rol = 'cliente'
        token = str(uuid.uuid4())

        cur.execute("""
            INSERT INTO usuarios 
            (nombre, apellido, telefono, direccion, correo, contraseña, rol, estado, token_activacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'inactivo', %s)
        """, (nombre, apellido, telefono, direccion, correo, password, rol, token))
        mysql.connection.commit()
        cur.close()

        try:
            enlace = url_for('auth.activar_cuenta', token=token, _external=True)
            msg = Message(
                '📧 Activa tu cuenta - Parrilla 51',
                recipients=[correo]
            )
            msg.body = f"""
Hola {nombre},

Gracias por registrarte en Parrilla 51 🍖

Activa tu cuenta aquí:
{enlace}

Si no solicitaste este registro, ignora este correo.
"""
            mail.send(msg)
            flash("✅ Registro exitoso. Revisa tu correo para activar tu cuenta", "success")
        except Exception as e:
            print("Error enviando correo:", e)
            flash("⚠️ Usuario creado, pero no se pudo enviar el correo", "warning")

        return redirect(url_for('auth.login'))

    return render_template('registro.html')


# -------------------- ACTIVAR CUENTA --------------------
@auth_bp.route('/activar/<token>')
def activar_cuenta(token):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE token_activacion = %s", (token,))
    user = cur.fetchone()

    if user:
        cur.execute("""
            UPDATE usuarios 
            SET estado = 'activo', token_activacion = NULL
            WHERE id_usuario = %s
        """, (user['id_usuario'],))
        mysql.connection.commit()
        flash("✅ Cuenta activada exitosamente", "success")
    else:
        flash("❌ El enlace de activación es inválido o ya fue usado", "danger")

    cur.close()
    return redirect(url_for('auth.login'))


# -------------------- OLVIDÉ CONTRASEÑA --------------------
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        correo = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user:
            try:
                token = serializer.dumps(correo, salt='password-reset-salt')
                enlace = url_for('auth.reset_password', token=token, _external=True)

                msg = Message(
                    '🔑 Restablecer contraseña - Parrilla 51',
                    recipients=[correo]
                )
                msg.body = f"""
Hola,

Para restablecer tu contraseña, haz clic aquí:
{enlace}

Si no solicitaste este cambio, ignora este mensaje.
"""
                mail.send(msg)
                flash("✅ Correo de recuperación enviado", "success")
            except Exception as e:
                print("Error enviando correo:", e)
                flash("⚠️ No se pudo enviar el correo en este momento", "warning")
        else:
            flash("⚠️ El correo no está registrado", "warning")

        return redirect(url_for('auth.login'))

    return render_template("forgot_password.html")


# -------------------- RESTABLECER CONTRASEÑA --------------------
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        correo = serializer.loads(token, salt='password-reset-salt', max_age=900)
    except Exception:
        flash("❌ El enlace es inválido o ha expirado", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            flash("⚠️ Las contraseñas no coinciden", "warning")
            return redirect(request.url)

        hashed = generate_password_hash(password1)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (hashed, correo))
        mysql.connection.commit()
        cur.close()

        flash("✅ Contraseña restablecida exitosamente", "success")
        return redirect(url_for('auth.login'))

    return render_template("reset_password.html")


# -------------------- CERRAR SESIÓN --------------------
@auth_bp.route('/logout')
def logout():
    nombre = session.get('nombre', 'Usuario')
    session.clear()
    flash(f"👋 Hasta pronto {nombre}", "info")
    return redirect(url_for('auth.login'))


# -------------------- REGISTRAR BLUEPRINT --------------------
def init_app(app):
    app.register_blueprint(auth_bp)
