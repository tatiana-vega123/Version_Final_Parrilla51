import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_mysqldb import MySQL
import os

mysql = MySQL()
mail = Mail()
serializer = URLSafeTimedSerializer(
    os.environ.get("SECRET_KEY", "pinchellave")
)

def create_app():
    app = Flask(__name__, template_folder="template")
    app.secret_key = os.environ.get("SECRET_KEY", "pinchellave")

    # ---------- MYSQL ----------
    app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST')
    app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQLDATABASE')
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT', 3306))
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.config['MYSQL_CONNECT_TIMEOUT'] = 10

    mysql.init_app(app)

    # ---------- MAIL ----------
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'enviodecorreosparrilla51@gmail.com'
    app.config['MAIL_PASSWORD'] = 'tyga bjte atex xajy'
    app.config['MAIL_DEFAULT_SENDER'] = 'enviodecorreosparrilla51@gmail.com'

    mail.init_app(app)

    # ---------- BLUEPRINTS ----------
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
