# backend_django

## MySQL
pour prépare la base de donnée, faire un utilisateur lui donner les droit sur une base nouvellement créer (pour éviter les problèmes d'overwrite).
Et noter le nom de l'utilisateur, la base de donnée, le mot de passe de l'utilisateurs.

## Base de l'installation
Télécharger le dépot github. Installer un venv python (3.12 de préférence) et le sourcer. Après installer les librairies avec la commandes:
```bash
pip install -r requirements.txt
```

créer un fichier `.env` dans le dossier du github et rentrer les informations suivantes:

```python
ALLOWED_HOST="https://your-domain.com"
BDD_ENGINE=django.db.backends.mysql

# Base de données que tu as créée
BDD_NAME="nom_de_la_base"

# Utilisateur que tu as créé
BDD_USER="utilisateur"
BDD_PASSWORD="password"

# Hôte et port (si local → localhost)
BDD_HOST=localhost
BDD_PORT=3306 #ou autre port de la base
SECRET_KEY=django-insecure-4z@t#(j$3x9y+v0^k8!p%1u2w!@randomstring #par exemple
```

après depuis le dossier du github faire les commandes:
```bash
python manage.py makemigrations && python manage.py migrate
```

Il est possible de tester avec :
```bash
python manage.py runserver
```
puis :
```bash
curl http://127.0.0.1:8000/events
```

## Installer en production

Pour installer en production le plus "proprement", c'est de faire avec `gunicorn + NGINX ou APACHE2`

créer un fichier : `/etc/systemd/system/gunicorn.service` et écrire:
```bash
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=user-session
Group=www-data
WorkingDirectory=/path/absolute/to/project
ExecStart=/path/to/virtual/env/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    back_pouic.wsgi:application

[Install]
WantedBy=multi-user.target
```

et lancer les commandes: 
```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

et mettre un reverse proxy avec NGINX par exemple:
créer un fichier : `/etc/nginx/sites-available/backend_django`

```bash
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
si il y a un domaine alors remplacer `server_name _` par `server_name my_domain.com`
puis faire les commandes:
```bash
sudo ln -s /etc/nginx/sites-available/backend_django /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

normalement pour du http cela devrait être bon. Pour du https il faut le certificat en plus. et modifier

```bash
    listen 80;
    server_name _;
```

pour avoir :

```bash
    listen 443 ssl;
    server_name ton-domaine.com www.ton-domaine.com;

    ssl_certificate /etc/letsencrypt/live/ton-domaine.com/fullchain.pem; #ou autre certif
    ssl_certificate_key /etc/letsencrypt/live/ton-domaine.com/privkey.pem; #ou autre privatekey

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
```

et ajouter dans le fichier `settings.py`:
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```