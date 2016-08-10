# RaspiRobot-Webcontrol
Some files and an instruction how to use and change the Dawn Robotics Camera-bot Software

Install all the Software like shown [here](http://web.archive.org/web/20151023223534/http://www.dawnrobotics.co.uk/creating-a-dawn-robotics-sd-card/) 
without setting up the Raspi as an Accesspoint (you can do that later). <br/>
Then download this Software by running: <br/>

$git clone https://github.com/BrixInMotion/RaspiRobot-Webcontrol.git <br/>

and add/replace the the programs in raspberry_pi_camera_bot by the Software in RaspiRobot-Webcontrol. <br/>

General setup for the Robot: <br/>
$sudo apt-get install xrdp    # Remote Desktop <br/>
$sudo apt-get install i2c-tools <br/>
$sudo apt-get install python-dev <br/>
§sudo apt-get install python-rpi.gpio <br/>
