# 🍖 Parrilla 51 — Sistema de Gestión Integral

Sistema web desarrollado en **Flask + MySQL** para la gestión integral del restaurante **Parrilla 51**. Incluye autenticación de usuarios, gestión de empleados, pedidos, mesas, reservas, inventario y reportes avanzados en **Excel** y **PDF**.

---

## 🚀 Características Principales

* 🔐 **Autenticación y seguridad**

  * Registro con activación por correo
  * Inicio y cierre de sesión
  * Recuperación y cambio de contraseña
  * Control de acceso por roles

* 👥 **Gestión de usuarios y perfiles**

  * Visualización y edición de datos personales
  * Cambio de contraseña seguro

* 🧑‍🍳 **Módulo de empleados**

  * Dashboard del empleado
  * Gestión de mesas (libre / ocupada)
  * Registro de pedidos en mesa
  * Control de stock en tiempo real
  * Historial de pagos del restaurante

* 📦 **Pedidos y órdenes**

  * Órdenes para restaurante y domicilio
  * Cambio de estados (pendiente, preparación, entregado, cancelado)
  * Historial detallado de órdenes

* 📅 **Reservas**

  * Crear, editar y cancelar reservas
  * Validación de fechas disponibles
  * Historial de reservas

* 📊 **Reportes administrativos**

  * Reportes de ventas e inventario
  * Filtros por fecha, estado, categoría y stock
  * Exportación a **Excel** con formato profesional
  * Exportación a **PDF** personalizados con logo

---

## 🧩 Estructura del Proyecto

```text
📦 proyecto_parrilla51
 ┣ 📂 routes
 ┃ ┣ 📄 auth_routes.py        # Autenticación, registro y recuperación
 ┃ ┣ 📄 empleado_routes.py    # Funciones del empleado
 ┃ ┣ 📄 perfil_routes.py      # Perfil del usuario
 ┃ ┣ 📄 usuarios.py           # API de usuario (perfil y contraseña)
 ┃ ┗ 📄 reportes.py            # Reportes y exportaciones
 ┣ 📂 templates                # Vistas HTML
 ┣ 📂 static                   # CSS, JS e imágenes
 ┣ 📄 __init__.py              # Configuración Flask, MySQL y Mail
 ┗ 📄 app.py                   # Inicialización de la aplicación
```

---

## 🔐 Roles del Sistema

| Rol               | Descripción                                         |
| ----------------- | --------------------------------------------------- |
| **Administrador** | Acceso total al sistema, reportes y control general |
| **Empleado**      | Gestión de mesas, pedidos, reservas y atención      |
| **Cliente**       | Realiza pedidos, gestiona su perfil y reservas      |

---

## ⚙️ Tecnologías Utilizadas

* **Backend:** Python · Flask
* **Base de datos:** MySQL
* **Frontend:** HTML · CSS · JavaScript · Jinja2
* **Seguridad:** Werkzeug (hash de contraseñas)
* **Correos:** Flask-Mail
* **Reportes:** Pandas · OpenPyXL · FPDF

---

## 🛠️ Instalación Básica

### 📦 Requisitos del Sistema

Asegúrate de tener instalado lo siguiente:

* **Python 3.9 o superior**
* **MySQL 8.0 o superior**
* **pip** (gestor de paquetes de Python)
* **Servidor de correo SMTP** (Gmail recomendado)

---

### 📚 Librerías necesarias (instalación manual)

Este proyecto **no usa `requirements.txt`**, por lo tanto debes instalar las dependencias manualmente:

```bash
pip install flask
pip install flask-mysqldb
pip install mysqlclient
pip install pandas
pip install openpyxl
pip install fpdf
pip install flask-mail
pip install itsdangerous
pip install werkzeug
```

---

### ▶️ Pasos de Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/parrilla51.git
```

2. Crear y activar entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # Linux / Mac
```

3. Configurar la base de datos MySQL

* Crear la base de datos:

```sql
CREATE DATABASE parrilla51;
```

* Importar el script SQL del proyecto
* Verificar credenciales en el archivo `__init__.py`

4. Configurar correo (Flask-Mail)

En `__init__.py` configura:

* Correo Gmail
* Contraseña de aplicación
* Puerto SMTP

5. Ejecutar la aplicación

```bash
flask run
```

---

2. Crear entorno virtual e instalar dependencias

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configurar la base de datos MySQL

   * Crear la base de datos `parrilla51`
   * Importar el script SQL

4. Ejecutar la aplicación

   ```bash
   flask run
   ```

---

## 📌 Notas Importantes

* El sistema valida **stock en tiempo real** antes de confirmar pedidos.
* Las reservas no permiten fechas duplicadas activas.
* Los reportes solo son accesibles para administradores.
* La seguridad se maneja mediante **sesiones y roles**.

---

✨ Autor

Proyecto desarrollado para Parrilla 51 🍖

Servicio Nacional de Aprendizaje – SENA
Centro de Gestión de Mercados, Logística y Tecnologías de la Información (CGMLTI)

Aprendices:

Ashley Daniela Torres

Andrés Felipe Arias

Tatiana Vega

Wendy Mercado
