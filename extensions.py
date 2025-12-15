from flask_mysqldb import MySQL
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mysql = MySQL()
mail = Mail()
serializer = URLSafeTimedSerializer("pinchellave")
