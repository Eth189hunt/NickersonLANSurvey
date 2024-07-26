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
Still in NickersonLANSurvey/lansurvey and still . venv/bin/activate
npm run web:install
python3 manage.py migrate
python3 manage.py collectstatic (say yes)

## Be sudo user or root is easier

### Gunicorn
sudo copy gunicorn.socket to /etc/systemd/system/gunicorn.socket

sudo copy gunicorn.service to /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

Check Status
sudo systemctl status gunicorn.socket

Should look like this
gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
     Active: active (listening) since Mon 2022-04-18 17:53:25 UTC; 5s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
     CGroup: /system.slice/gunicorn.socket

Apr 18 17:53:25 django systemd[1]: Listening on gunicorn socket.



### Nginx
copy static files to /var/www/static
sudo cp -r /home/survey/NikcersonLANsurvey/static /var/www/static

sudo copy nginx conf survey to /etc/nginx/sites-available/survey
cp survey /etc/nginx/sites-available/survey

This activates the site by linking to the `sites-enabled` directory.
sudo ln -s /etc/nginx/sites-available/survey /etc/nginx/sites-enabled

Remove default sites available
sudo rm /etc/nginx/sites-enabled/default

test nginx
sudo nginx -t

restart nginx
sudo systemctl restart nginx


