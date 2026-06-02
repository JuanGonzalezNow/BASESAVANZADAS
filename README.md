# RideAxis

Aplicacion web en Flask para catalogo, carrito, checkout y administracion de motocicletas.

## Requisitos

- Python 3.11 o superior
- MySQL Server
- Git

## Instalacion

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd mi_app
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

En macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear la base de datos en MySQL:

```sql
CREATE DATABASE rideaxis_db;
```

5. Crear el archivo de variables de entorno:

```bash
copy .env.example .env
```

En macOS/Linux:

```bash
cp .env.example .env
```

6. Editar `.env` con los datos reales de MySQL:

```env
MYSQL_USER=root
MYSQL_PASSWORD=tu_contrasena
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=rideaxis_db
```

7. Ejecutar la aplicacion:

```bash
python run.py
```

La aplicacion quedara disponible en:

```text
http://127.0.0.1:5000
```

## Notas

- `run.py` crea las tablas automaticamente con `db.create_all()`.
- No subas el archivo `.env` a GitHub; cada persona debe crear el suyo desde `.env.example`.
- Los archivos generados por Python, como `__pycache__` y `*.pyc`, no deben versionarse.
