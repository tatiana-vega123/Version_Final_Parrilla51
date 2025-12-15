import pymysql
import os

ARCHIVO_SQL = "parrilla51.sql"

conn = pymysql.connect(
    host=os.environ["MYSQLHOST"],
    user=os.environ["MYSQLUSER"],
    password=os.environ["MYSQLPASSWORD"],
    database=os.environ["MYSQLDATABASE"],  # ✅ CORRECTO
    port=int(os.environ.get("MYSQLPORT", 3306)),
    charset="utf8mb4",
    autocommit=False
)

cur = conn.cursor()

with open(ARCHIVO_SQL, "r", encoding="utf-8") as f:
    sql_commands = f.read()

for command in sql_commands.split(';'):
    if command.strip():
        try:
            cur.execute(command)
        except Exception as e:
            print(f"⚠️ Error ejecutando comando:\n{e}\n")

conn.commit()
cur.close()
conn.close()

print("✅ Base de datos importada correctamente.")
