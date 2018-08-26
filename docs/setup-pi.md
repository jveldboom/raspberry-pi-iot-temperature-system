# Initial Pi Setup
## Install Raspbian
https://www.raspberrypi.org/learning/software-guide/quickstart/

---

## Enable SSH
- Enter `sudo raspi-config` in a terminal window
- Select Interfacing Options
- Navigate to and select SSH
- Choose Yes
- Select Ok
- Choose Finish

## Enable SSH on a headless Raspberry Pi
For headless setup, SSH can be enabled by placing a file named ssh, without any extension, onto the boot partition of the SD card.
When the Pi boots, it looks for the  ssh file. If it is found, SSH is enabled, and the file is deleted.
The content of the file does not matter: it could contain text, or nothing at all.


## Install Software
```
sudo apt-get update
sudo apt-get install -y vim
```

## Enable WiFi
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# add to bottom of file
network={
    ssid="testing"
    psk="testingPassword"
}


# restart interface
sudo wpa_cli reconfigure

# verify connected - should have ip
ifconfig wlan0
```

## Fix DNS resolution
```
sudo vi /etc/resolv.conf.head

# Google Servers
nameserver 8.8.8.8
nameserver 8.8.4.4
```

---

# Install Supervisor
[Original Source](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps)

```
sudo apt-get install supervisor
sudo service supervisor restart
```

__Add Program to Supervisor__
```
sudo vi /etc/supervisor/conf.d/{PROGRAM_NAME}

[program:readtemperature]
command=python run.py
directory = /home/pi/projects/iot-tempature-system
user = pi
autostart=true
autorestart=true
environment=CLIENT_ID=pi1,MQTT_HOST=xxxxxxxxx.iot.us-east-1.amazonaws.com
stderr_logfile=/var/log/read-tempature.log
stdout_logfile=/var/log/read-tempature.log
```
__Update Config After Change__
```
sudo supervisorctl reread
sudo supervisorctl update
```

---

## Install Docker
```
curl -sSL https://get.docker.com | sh

# allow Docker to run as pi user
sudo usermod -aG docker pi
```
