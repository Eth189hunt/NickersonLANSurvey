# Delpy Process

## Install these
sudo apt update
sudo apt install git python3-env python3-dev libpq-dev nginx nodejs npm

## New user survey
sudo adduser survey
su survey
cd ~

copy in project multiple ways ssh key deploy or copy files with scp

## Create a virtual environment
cd lansurvey
python3 -m venv venv
. ven/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

## Collect static files and migrate
Still in NickersonLANSurvey/lansurvey
npm run web:install
python3 manage.py migrate
python3 manage.py collectstatic

## Be sudo user

### Gunicorn
sudo copy gunicorn.socket to /etc/systemd/system/gunicorn.socket

sudo copy gunicorn.service to /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

### Nginx
sudo copy nginx.conf to /etc/nginx/sites-available/myproject

This activates the site by linking to the `sites-enabled` directory.
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled



