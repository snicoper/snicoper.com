# Instalación

## Prerrequisitos

* [nginx](http://apuntes-snicoper.readthedocs.io/es/latest/linux/nginx/instalacion_nginx.html)
* [postgresql](http://apuntes-snicoper.readthedocs.io/es/latest/linux/postgresql/instalacion_postgresql.html)
* [postfix/dovecot](http://apuntes-snicoper.readthedocs.io/es/latest/linux/fedora-centos/postfix.html)

## Group webapps

```bash
sudo groupadd webapps
sudo usermod -a -G webapps snicoper
```

## Directorio webapps

```bash
sudo mkdir /var/webapps
sudo chown snicoper:webapps /var/webapps

# Si SELinux esta activado.
sudo chcon -R -t  httpd_sys_content_t /var/webapps
```

## Instalación snicoper.com

```bash
cd /var/webapps
git clone https://github.com/snicoper/snicoper.com.git snicoper.com
cd snicoper.com
```

## Preparación de la base de datos

```bash
psql -U postgres

CREATE USER db_user WITH PASSWORD 'db_password';
CREATE DATABASE db_name WITH OWNER db_user;
```

Requiere el archivo `~/.pgpass` para los backups con `cron`

```bash
vim ~/.pgpass

db_host:db_port:db_name:db_user:db_password
```

Restaurar la base de datos, si la hay:

```bash
psql -U postgres snicopercom < backups/postgresql/archivo_restauracion.sql
```

## Instalación paquetes requeridos por la aplicación con pip y virtualenv

Instalación del entorno virtual de producción.

```bash
mkvirtualenv snicopercom
```

Añadir variables de entorno a `postactivate` y `postdeactivate`

```bash
vim $VIRTUAL_ENV/bin/postactivate
```

Añadir

```bash
source /var/webapps/snicoper.dev/bin/postactivate.sh

# Node
export NODE_ENV="production"
```

```bash
vim $VIRTUAL_ENV/bin/postdeactivate
```

Añadir

```bash
source /var/webapps/snicoper.dev/bin/postactivate.sh

# Node
unset NODE_ENV
```

Instalar requirements

```bash
pip install -r requirements/prod.txt
```

## Firewalld

```bash
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --permanent --zone=public --add-service=smtp
sudo firewall-cmd --permanent --zone=public --add-service=imaps
```

## Certificado SSL

Para crear el certificado, hacerlo sin configuración de nginx o renombrar ``/etc/nginx/conf.d/snicoper.com.conf`` a ``/etc/nginx/conf.d/snicoper.com``

[certbot](http://apuntes-snicoper.readthedocs.io/es/latest/linux/fedora-centos/certificado_lets_encrypt.html)

```bash
sudo dnf install certbot

sudo vim /etc/nginx/default.d/le-well-known.conf
```

Añadir

```bash
location ~ /.well-known {
  allow all;
}
```

Reiniciar nginx

```bash
sudo systemctl restart nginx
```

Para obtener el certificado.

```bash
sudo certbot certonly -a webroot --webroot-path=/usr/share/nginx/html -d snicoper.com -d www.snicoper.com -d mail.snicoper.com
```

Cuando todo haya salido bien, hay una maximo de 5 intentos cada hora.

```bash
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```

## postfix/dovecot

La configuración es la de [mis apuntes](http://apuntes-snicoper.readthedocs.io/es/latest/linux/fedora-centos/postfix.html)

Editar ``sudo vim /etc/postfix/main.cf``

```bash
myhostname = mail.snicoper.com
mydomain = snicoper.com
mynetworks = 192.168.1.0/24, 127.0.0.0/8, IP_PUBLICA # <---- Ip publica
smtpd_tls_cert_file = /etc/letsencrypt/live/snicoper.com/fullchain.pem
smtpd_tls_key_file = /etc/letsencrypt/live/snicoper.com/privkey.pem
```

Editar ``sudo vim /etc/dovecot/conf.d/10-ssl.conf``

```bash
ssl_cert = </etc/letsencrypt/live/snicoper.com/fullchain.pem
ssl_key = </etc/letsencrypt/live/snicoper.com/privkey.pem
```

Los archivos están en ``/var/webapps/snicoper.com/compose/configs/``

```bash
sudo cp compose/configs/nginx_https.conf /etc/nginx/conf.d/snicoper.com.conf
```

Eliminar de ``sudo vim /etc/nginx/nginx.conf`` en la linea 36 y 37 ``default_server``

Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

## staticfiles

```bash
./prod_manage.py collectstatic --clear --noinput
```

## Haystack
```bash
./prod_manage.py rebuild_index
```

## Gunicorn

Crear un servicio systemd para Gunicorn

.. code-block:: bash

    sudo cp compose/configs/gunicorn.service /etc/systemd/system/gunicorn.service
    sudo cp compose/configs/logrotate /etc/logrotate.d/gunicorn
    sudo mkdir /var/log/gunicorn/
    sudo chown snicoper:webapps /var/log/gunicorn/
    sudo systemctl start gunicorn.service
    sudo systemctl enable gunicorn.service

## Cron

Como usuario `crontab -e`

```bash
MAILTO=snicoper@snicoper.com

0 1 * * * /var/webapps/snicoper.com/cron/haystack_update_index.sh
2 1 * * * /var/webapps/snicoper.com/cron/postgres_db_backup.sh
4 1 * * * /var/webapps/snicoper.com/cron/clear_sessions.sh
6 1 * * * /var/webapps/snicoper.com/cron/ping_google.sh
8 1 * * * /var/webapps/snicoper.com/cron/media_backup.sh
```

Como root `sudo crontab -e`

```bash
MAILTO=snicoper@snicoper.com

30 2 * * 1 /usr/bin/certbot renew >> /var/log/le-renew.log
35 2 * * 1 /usr/bin/systemctl reload nginx
```
