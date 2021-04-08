# RaspiRobot-Webcontrol
Some files and an instruction how to use and change the Dawn Robotics Camera-bot Software.
* this Repository is for the Basis-platform only.
* for motor control setupt and software visit https://github.com/BrixInMotion/RaspiRobot
* for claw control setup and software visit: (coming soon)

See the Robot in action: https://www.youtube.com/watch?v=14D5h0CcbAE

## 1. Hardware
* Raspberry Pi 3 or 4
* Wide angle Raspberry Pi camera
* Adafruit 16Ch PWM Servo Hat
* [Infineon XMC1100 Boot kit](https://www.infineon.com/cms/en/product/evaluation-boards/kit_xmc11_boot_001/)
* 3 * [Infineon BTN8982 DC Motor-Control Shield](https://www.infineon.com/cms/en/product/evaluation-boards/dc-motorcontr_btn8982/)

## 2. Software installation
Download this software by running:

```
$git clone https://github.com/BrixInMotion/RaspiRobot-Webcontrol.git raspberry_pi_camera_bot
```
and run: <br/>
```
$sudo python /home/pi/raspberry_pi_camera_bot/Setup-Camera-bot.py
```
This script installs all the software you need to control your Robot via a webpage. Alternatively you can install the Software [like shown here](http://web.archive.org/web/20151023223534/http://www.dawnrobotics.co.uk/creating-a-dawn-robotics-sd-card/), 
but the script does exactly the same without setting up the Pi as an Access point. If you install the Software manually you have to add/replace the the programs in raspberry_pi_camera_bot by the Software in RaspiRobot-Webcontrol, otherwise the script does this automatically. It reboots the Pi, if you admit, and afterards you 
can immediately enter the Pi's IP-Address in a Browser on your Tablet (or another computer).


You can also set the Pi up as a Wifi Bridge like I did, so the wlan0 (the internal Wlan if your're using the RPi 3)
works as an Access Point and wlan1 (a Wlan-USB-Adapter) works as a client. In this configuration you have a wireless Wlan repeater,
but can also access the Web-server to control the Robot from both sites. To set up like explained, follow
[this great tutorial](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software) and replace the *eth0* commands in the 3 commands of iptable configuration by *wlan1*. Use the *etc-network_interfaces.txt* as an example for configuration to have normal Wifi by wlan1.

General setup for the Robot (the Setup-Camera-bot script installs this already):
```
$sudo apt-get install xrdp      # Remote Desktop
$sudo apt-get install i2c-tools
$sudo apt-get install python-dev
$sudo apt-get install python-rpi.gpio
```

Setup I2C [like shown here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c) if it doesn't work.
