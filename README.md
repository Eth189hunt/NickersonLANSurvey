# NickersonLANSurvey

## Setup
Follow Deploy read me.
Then disable ssh for extra security.
systemctl disable ssh
systemctl stop ssh

# Copy data in export method
sudo su survey
cd ~
. venv/bin/activate
cd NickersonLANSurvey/lansurvey
python3 manage.py export_survey