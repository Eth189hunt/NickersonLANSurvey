# Delpy Process

## Install these
sudo apt update
sudo apt install python3-env python3-dev libpq-dev nginx

## New user survey
sudo adduser survey
su survey
cd ~

## Create a virtual environment
python3 -m venv venv

### Gunicorn
sudo copy gunicorn.socket to /etc/systemd/system/gunicorn.socket

sudo copy gunicorn.service to /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

### Nginx
sudo copy nginx.conf to /etc/nginx/sites-available/myproject

This activates the site by linking to the `sites-enabled` directory.
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled



