# Club Deportivo - API de Reservas

API REST desarrollada en **Python + Flask** para gestionar las reservas de un club deportivo.

El sistema permite administrar deportes, canchas, socios y reservas, incluyendo disponibilidad de canchas, validación de horarios y control de superposición de reservas.

La especificación de la API se encuentra documentada en `swagger.yaml`.

---

## Tecnologías

- Python 3
- Flask
- MySQL
- SQLAlchemy
- PyMySQL
- python-dotenv
- Swagger / OpenAPI

---

## Estructura del proyecto

```text
club-api/
├── src/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── routes/
│   │   └── ...
│   │
│   ├── services/
│   │   └── ...
│   │
│   ├── repositories/
│   │   └── ...
│   │
│   ├── validators/
│   │   └── ...
│   │
│   └── db/
│       └── connection.py
│
├── tests/
│
├── scripts/
│   └── init_db.sql
│
├── swagger.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Responsabilidad de cada carpeta

**`routes/`**

Define los endpoints HTTP de la API.

Por ejemplo:

```text
GET /deportes
GET /canchas
POST /reservas
```

Las routes reciben las requests y devuelven las responses HTTP.

---

**`services/`**

Contiene las reglas de negocio.

Por ejemplo:

- Validar que una cancha esté activa.
- Validar que un socio esté activo.
- Comprobar superposición de reservas.
- Calcular el importe de una reserva.
- Validar cambios de estado.

---

**`repositories/`**

Contiene el acceso a la base de datos.

Acá se realizan las consultas SQL necesarias para obtener, insertar, actualizar o eliminar información.

El flujo general es:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
Database
```

---

**`validators/`**

Contiene validaciones relacionadas con los datos recibidos por la API.

Por ejemplo:

- Campos obligatorios.
- Tipos de datos.
- Formato de email.
- Parámetros válidos.
- Formato de fechas.

---

**`db/`**

Contiene la configuración necesaria para conectarse a MySQL.

`connection.py` crea el engine de SQLAlchemy utilizado por los repositories.

---

**`scripts/`**

Contiene scripts relacionados con la inicialización de la base de datos.

`init_db.sql` crea las tablas necesarias y carga los datos iniciales.

---

**`swagger.yaml`**

Contiene el contrato OpenAPI de la API.

Define los endpoints disponibles, parámetros, request bodies, responses y schemas.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```bash
cd club-api
```

---

## 2. Crear un entorno virtual

### macOS / Linux

```bash
python3 -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
```

Activarlo:

```bash
.venv\Scripts\activate
```

Cuando el entorno esté activo debería aparecer algo similar a:

```text
(.venv)
```

al comienzo de la terminal.

---

## 3. Instalar las dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Esto instalará las dependencias necesarias para ejecutar el proyecto.

---

# Configuración de MySQL

Es necesario tener un servidor **MySQL** ejecutándose localmente.

La configuración utilizada por la aplicación se define mediante variables de entorno.

## 4. Crear el archivo `.env`

En la raíz del proyecto crear:

```text
.env
```

Tomar como referencia `.env.example`.

Ejemplo:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=club_deportivo
```

> El archivo `.env` contiene configuración local y posibles credenciales, por lo que no debe subirse al repositorio.

---

## 5. Inicializar la base de datos

El proyecto incluye:

```text
scripts/init_db.sql
```

Este script crea la base de datos, las tablas necesarias y los datos iniciales.

Desde una terminal con MySQL disponible:

```bash
mysql -u root -p < scripts/init_db.sql
```

También puede ejecutarse desde **MySQL Workbench**:

1. Conectarse al servidor MySQL local.
2. Ir a `File > Open SQL Script`.
3. Seleccionar `scripts/init_db.sql`.
4. Ejecutar el script.

Para comprobar la creación:

```sql
SHOW DATABASES;

USE club_deportivo;

SHOW TABLES;
```

---

# Ejecutar la aplicación

Con `.venv` activado y MySQL ejecutándose:

```bash
python -m src.app
```

La API se ejecutará localmente.

Actualmente el servidor de desarrollo utiliza:

```text
http://127.0.0.1:5001
```

Para verificar que Flask está funcionando:

```text
GET http://127.0.0.1:5001/
```

Debería responder:

```json
{
  "status": "ok"
}
```

---

# Desarrollo

Cuando se instale una nueva dependencia:

```bash
pip install nombre-dependencia
```

actualizar `requirements.txt`:

```bash
pip freeze > requirements.txt
```

No se debe subir `.venv` al repositorio.

---

# Variables de entorno

El repositorio contiene `.env.example` como referencia.

Ejemplo:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=club_deportivo
```

Cada desarrollador debe crear su propio `.env`.

---

# API

Los principales recursos de la API son:

```text
/deportes
/canchas
/socios
/reservas
```

La definición completa de endpoints y estructuras de datos se encuentra en:

```text
swagger.yaml
```

---

# Flujo de una request

La arquitectura busca mantener separadas las responsabilidades:

```text
HTTP Request
     ↓
   Route
     ↓
 Validator
     ↓
  Service
     ↓
Repository
     ↓
   MySQL
     ↓
HTTP Response
```

No todas las operaciones necesariamente requieren todas las capas. Por ejemplo, una consulta simple puede no necesitar reglas de negocio adicionales.

---

# Base de datos

La información se almacena de forma persistente en MySQL.

Las entidades principales son:

```text
deportes
canchas
socios
reservas
```

Los deportes son datos precargados por `init_db.sql`.

---

# Documentación

La documentación de la API utiliza **OpenAPI** y se encuentra definida en:

```text
swagger.yaml
```

Swagger UI será utilizado para visualizar y probar los endpoints de la API.