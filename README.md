# RaspiRobot-Webcontrol
Some files and an instruction how to use and change the Dawn Robotics Camera-bot Software.

See the Robot in action: https://www.youtube.com/watch?v=14D5h0CcbAE

Download this Software by running: <br/>

$git clone https://github.com/BrixInMotion/RaspiRobot-Webcontrol.git raspberry_pi_camera_bot <br/>

and run: <br/>

$sudo python /home/pi/raspberry_pi_camera_bot/Setup-Camera-bot.py <br/>

This script installs all the software you need to control your Robot via a webpage. <br/>
Alternativ you can install the Software like shown 
[here](http://web.archive.org/web/20151023223534/http://www.dawnrobotics.co.uk/creating-a-dawn-robotics-sd-card/), 
but the script does exactly the same without setting up the Pi as an Access point. <br/>
If you install the Software manually you have to add/replace the the programs in raspberry_pi_camera_bot by the Software in <br/>
RaspiRobot-Webcontrol, otherwise the script does this automatically, it reboots the pi ,if you admit, and afterards you <br/>
can immediately enter the Pi's IP-Address in a Browser on your Tablet (or another computer). <br/>
<br/>
You can also set the Pi up as a Wifi Bridge like I did, so the wlan0 (the internal Wlan if your're using the RPi 3) <br/>
works as an Access Point and wlan1 (a Wlan-USB-Adapter) works as a client. In this configuration you have a wireless Wlan repeater, <br/>
but can also access the Web-server to control the Robot from both sites. To set up like explained, follow
[this](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software) great tutorial
and replace the *eth0* commands in the 3 commands of iptable configuration by *wlan1*.

General setup for the Robot (the Setup-Camera-bot script installs this already): <br/>
$sudo apt-get install xrdp    # Remote Desktop <br/>
$sudo apt-get install i2c-tools <br/>
$sudo apt-get install python-dev <br/>
$sudo apt-get install python-rpi.gpio <br/>

Setup I2C like shown [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c) if it doesn't work.
