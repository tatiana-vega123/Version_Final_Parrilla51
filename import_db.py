import pymysql
import os

# 🔹 Nombre de tu archivo SQL exportado
# Asegúrate de que esté en la misma carpeta que este script o pon la ruta completa
ARCHIVO_SQL = "parrilla51.sql"

# 🔹 Conexión a la base de datos de Railway usando variables de entorno
conn = pymysql.connect(
    host=os.environ["MYSQLHOST"],
    user=os.environ["MYSQLUSER"],
    password=os.environ["MYSQLPASSWORD"],
    database=os.environ["MYSQL_DATABASE"],
    port=int(os.environ.get("MYSQLPORT", 3306))
)

cur = conn.cursor()

# 🔹 Leer todo el SQL
with open(ARCHIVO_SQL, "r", encoding="utf-8") as f:
    sql_commands = f.read()

# 🔹 Separar por ; y ejecutar cada comando
for command in sql_commands.split(';'):
    if command.strip():
        try:
            cur.execute(command)
        except Exception as e:
            print(f"⚠️ Error ejecutando comando: {e}")

# 🔹 Confirmar cambios y cerrar
conn.commit()
cur.close()
conn.close()

print("✅ Base de datos importada correctamente.")
