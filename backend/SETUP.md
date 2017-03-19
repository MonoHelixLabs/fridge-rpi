Raspberry Pi Lean Setup (Mac OS)

# Fresh Install
## Download Minibian
```
mac:~ radu$ cd ~/LeanSetup/
mac:LeanSetup radu$ wget http://downloads.sourceforge.net/project/minibian/2016-03-12-jessie-minibian.tar.gz
mac:LeanSetup radu$ tar -xvf 2016-03-12-jessie-minibian.tar.gz
```
## Check integrity of download
For this file we have: 
```
MD5: 136CAC722A4F78F49B54971AE1CC03EE
SHA1: 7C83919698BD58A221A741495872021CAF6CEEF3
```
Check the Minibian website for the latest version
```
mac:LeanSetup radu$ md5 2016-03-12-jessie-minibian.tar.gz
MD5 (2016-03-12-jessie-minibian.tar.gz) = 136cac722a4f78f49b54971ae1cc03ee
```
## Insert SD card
Insert SD card on computer

## Find disk identifier for SD card and unmount
```
$ diskutil list 
$ diskutil unmountDisk /dev/disk11
```
## (Optional) Install pv to monitor next step
```
mac:LeanSetup radu$ brew install pv
```
## Write Image to disk
```
mac:LeanSetup radu$ pv 2016-03-12-jessie-minibian.img | sudo dd bs=4m of=/dev/disk11
```
or if the optional step before was skipped:
```
mac:LeanSetup radu$ sudo dd bs=4m if=2016-03-12-jessie-minibian.img of=/dev/disk11
```
# Configure installation
## Change password
Initial password for root is `raspberry` and we need to change to something more secure.
```
rpi:~# passwd
```
Upgrade packages to latest versions:
```
root@minibian:~# apt-get update && apt-get upgrade
```
Install nano text editor:
```
root@minibian:~# apt-get install nano
```
Install raspian config tool:
```
root@minibian:~# apt-get install raspi-config
```
## Create a user
Install sudo:
```
root@minibian:~# apt-get install sudo
```
Create a user:
```
root@minibian:~# adduser <user>
```
Add user to sudo group:
```
root@minibian:~# adduser <user> sudo
```
Logout from `ssh` with `exit` and login with `ssh <user>@<host>`

Disable `root` login:
```
radu@minibian:~$ sudo passwd -l root
```
## Configure WiFi
Install `usbutils`:
```
radu@minibian:~$ sudo apt-get install usbutils
```
Check which firmware you need:
```
radu@minibian:~$ lsusb | grep -i wireless
Bus 001 Device 004: ID 7392:7811 Edimax Technology Co., Ltd EW-7811Un 802.11n Wireless Adapter [Realtek RTL8188CUS]
```
Install firmware:
```
radu@minibian:~$ sudo apt-get install firmware-realtek
```
Install `wpasupplicant` and `wireless-tools` (for the `iwlist`):
```
radu@minibian:~$ sudo apt-get install wpasupplicant wireless-tools
```
Change interfaces configuration file:
```
radu@minibian:~$ sudo nano /etc/network/interfaces
```
Update the file to look like:
```
auto lo
iface lo inet loopback
iface eth0 inet dhcp
allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```
Change `wpa_supplicant` configuration file:
```
radu@minibian:~$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Update the file to look like:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="<SSID>"
    psk="<WIFI_PASSWORD>"
}
```
### (Optional) Disable power save mode on Edimax EW-7811Un
Make a file `8192cu.conf` in directory `/etc/modprobe.d/`:
```
radu@minibian:~$ sudo nano /etc/modprobe.d/8192cu.conf
```
Add following to file:
```
# Disable power management
options 8192cu rtw_power_mgnt=0 rtw_enusbss=0
```
# Secure system
## Change SSH configuration
```
radu@minibian:~$ sudo nano /etc/ssh/sshd_config
```
Add following to file:
```
Port 12
PasswordAuthentication no
PermitRootLogin no
Match Address 10.0.0.0/8
    PasswordAuthentication yes
```
# Camera setup
## Setup USB cameras
Install `fswebcam`:
```
radu@minibian:~$ sudo apt-get install fswebcam
```
Add user to `video` group:
```
radu@minibian:~$ sudo adduser radu video
```
## Take pictures with USB cameras
```
radu@minibian:~$ fswebcam -d /dev/video0 --top-banner --title CAM0 -r 1920x720 v0.jpg; fswebcam -d /dev/video1 --top-banner --title CAM1 -r 1920x720 v1.jpg
```
## Setup RPi camera
Enable camera from `raspi-config`.
## Take pictures with RPi camera
```
radu@minibian:~$ raspistill -w 1440 -h 720 -o v2.jpg -t 1
```
## Take pictures with all cameras and time execution
```
radu@minibian:~$ time raspistill -w 1440 -h 720 -o v2.jpg -t 1 ; time fswebcam -q -d /dev/video0 --no-banner -r 1920x720 v0.jpg; time fswebcam -q -d /dev/video1 --no-banner -r 1920x720 v1.jpg
```
# Integration
## Connect to S3
Install pip:
```
radu@minibian:~$ sudo apt-get install python3-pip
```
Install `awscli`, for managing AWS services:
```
radu@minibian:~$ sudo pip3 install awscli
```
Install `boto3`, for interfacing with AWS services:
```
radu@minibian:~$ sudo pip3 install boto3
```
## Talk some MQTT
Install `paho`:
```
radu@minibian:~$ sudo pip3 install paho-mqtt 
```
Install `adafruit-io`:
```
radu@minibian:~$ sudo pip3 install adafruit-io
```
Set `AIOKEY` and `AIOUSER` environment variable:
```
radu@minibian:~$ sudo nano /etc/environment
```
## Code the GPIO
Install `RPi.GPIO`:
```
radu@minibian:~$ sudo pip3 install RPi.GPIO
```
Set permissions for `/dev/mem`:
```
radu@minibian:~$ sudo groupadd gpio
radu@minibian:~$ sudo gpasswd -a radu gpio
```
Add `udev` rule:
```
radu@minibian:~$ sudo nano /etc/udev/rules.d/99-com.rules
```
```
SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio; chown -R root:gpio /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio; chown -R root:gpio /sys/devices/platform/soc/*.gpio/gpio && chmod -R 770 /sys/devices/platform/soc/*.gpio/gpio'"
SUBSYSTEM=="input", GROUP="input", MODE="0660"
SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0660"
SUBSYSTEM=="spidev", GROUP="spi", MODE="0660"
SUBSYSTEM=="bcm2835-gpiomem", GROUP="gpio", MODE="0660"
```
## Register fridgecam as a start-up service
Edit `/etc/init.d/fridgecam`:
```
#! /bin/sh
# /etc/init.d/fridgecam
### BEGIN INIT INFO
# Provides:          fridgecam
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     3 4 5
# Default-Stop:      0 1 6
# Short-Description: Fridge cam taking pictures
# Description:       A simple project to listen for MQTT messages and taking pictures.
### END INIT INFO
# If you want a command to always run, put it here
# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting fridgecam"
    # run application you want to start
    su radu -c 'python3 /home/radu/fridgecam.py &'
    ;;
  stop)
    echo "Stopping fridgecam"
    # kill application you want to stop
    pkill -f fridgecam.py
    ;;
  *)
    echo "Usage: /etc/init.d/fridgecam {start|stop}"
    exit 1
    ;;
esac
exit 0
```
Change file permission to make executable:
```
radu@minibian:~$ sudo chmod 755 /etc/init.d/fridgecam
```
Test start and stop:
```
radu@minibian:~$ sudo /etc/init.d/fridgecam start
radu@minibian:~$ sudo /etc/init.d/fridgecam stop
```
Register for start-up:
```
radu@minibian:~$ sudo update-rc.d fridgecam defaults
```
