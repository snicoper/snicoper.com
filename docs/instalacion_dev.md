# Instalación

## Prerrequisitos

* [nginx](http://apuntes-snicoper.readthedocs.io/es/latest/linux/nginx/instalacion_nginx.html)
* [postgresql](http://apuntes-snicoper.readthedocs.io/es/latest/linux/postgresql/instalacion_postgresql.html)
* [postfix/dovecot](http://apuntes-snicoper.readthedocs.io/es/latest/linux/fedora-centos/postfix.html)

## Descargar archivos snicoper.dev

```bash
cd ~/projects
git clone https://github.com/snicoper/snicoper.com.git snicoper.dev
cd snicoper.dev
```

## Preparación de la base de datos

```bash
psql -U postgres

CREATE USER db_user WITH PASSWORD 'db_password';
CREATE DATABASE db_name WITH OWNER db_user;

# Para test.
CREATE USER test_django WITH PASSWORD '123456' CREATEDB;
\q

vim ~/.pgpass

localhost:5432:*:db_user:db_password
localhost:5432:test_django_db:test_django:123456

chmod 600 ~/.pgpass
```

## virtualenvwrapper

Instalación del entorno virtual en desarrollo.

```bash
mkvirtualenv snicoperdev
```

Añadir variables de entorno a ``postactivate``

```bash
vim $VIRTUAL_ENV/bin/postactivate
```

Añadir

```bash
source ~/projects/snicoper.dev/bin/postactivate.sh

export NODE_ENV="development"
```

Desactivar y volver a activar

```bash
deactivate
workon snicoperdev
```

Añadir variables de entorno a ``postdeactivate``

```bash
vim $VIRTUAL_ENV/bin/postdeactivate
```

Añadir

```bash
source ~/projects/snicoper.dev/bin/postdeactivate.sh

unset NODE_ENV
```

Instalar requirements, tanto local como prod.

Para `prod` requiere:

```bash
sudo dnf install gcc libffi-devel python3-devel openssl-devel
```

```bash
pip install -r requirements/local.txt
pip install -r requirements/prod.txt
```

## Reinstall

```bash
reinstall_dev.sh
```

## Usuarios y passwords Web en dev

* snicoper: 123 (superuser)
* perico: 123 (normal)
