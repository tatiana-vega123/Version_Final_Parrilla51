import pymysql
pymysql.install_as_MySQLdb()  # 🔧 Necesario para Railway

from flask import Flask
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_mysqldb import MySQL
import os

# 🔌 Extensiones globales
mysql = MySQL()
mail = Mail()
serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "pinchellave"))

def create_app():
    app = Flask(__name__, template_folder="template")
    app.secret_key = os.environ.get("SECRET_KEY", "pinchellave")

    # ------------------ CONFIGURACIÓN MYSQL (RAILWAY) ------------------
    # Usamos os.getenv() para evitar KeyError si falta alguna variable
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql.railway.internal')  # Dirección correcta del host
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')  # Usuario 'root'
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'UBoOKapMxkCvNzRUdLnXZwMdzMmlSdel')  # Contraseña de la base de datos directamente
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE', 'parrilla51')  # Nombre de la base de datos
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))  # Puerto por defecto
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)  # ✅ Inicializar MySQL

    # ------------------ CONFIGURACIÓN CORREO ------------------
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'enviodecorreosparrilla51@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'tyga bjte atex xajy')
    app.config['MAIL_DEFAULT_SENDER'] = 'enviodecorreosparrilla51@gmail.com'

    mail.init_app(app)

    # ------------------ REGISTRAR BLUEPRINTS ------------------
    from routes import (
        auth_routes,
        dashboard_routes,
        cliente_routes,
        admin_routes,
        empleado_routes
    )
    from routes.reportes import reportes_bp

    auth_routes.init_app(app)
    dashboard_routes.init_app(app)
    cliente_routes.init_app(app)
    admin_routes.init_app(app)
    empleado_routes.init_app(app)

    app.register_blueprint(reportes_bp, url_prefix='/reportes')

    return app
