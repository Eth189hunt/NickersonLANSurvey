# NickersonLANSurvey

## Setup
Follow Deploy read me.
Then disable ssh for extra security.
systemctl disable ssh
systemctl stop ssh

## Hotspot/Wifi
sudo nmcli device wifi hotspot ssid <hotspot name> password <hotspot password> ifname wlan0
sudo nmcli connection modify <hotspot UUID> connection.autoconnect yes

# Copy data in export method
Login to pi on pilan
sudo su survey
cd ~
. venv/bin/activate
cd NickersonLANSurvey/lansurvey
python3 manage.py export_survey
ctl + d or logout of user
sudo mv /home/survey/NickersonLANSurvey/lansurvey/import.csv .
sudo systemctl start ssh

From another computer
scp pilan@10.42.0.1:import.csv .

Back on Pi
sudo systemctl stop ssh
