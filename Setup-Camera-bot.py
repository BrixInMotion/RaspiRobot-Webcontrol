import os
import sys

if __name__=='__main__':
    print('-------------------------------------------------------------------')
    print('Setup camera streaming...')
    print('-------------------------------------------------------------------')
    os.system('sudo apt-get install gcc build-essential cmake vlc')
    os.system('git clone https://bitbucket.org/DawnRobotics/raspberry_pi_camera_streamer.git')
    os.system('mkdir /home/pi/raspberry_pi_camera_streamer/build')
    os.system('cmake -B/home/pi/raspberry_pi_camera_streamer/build/ -H/home/pi/raspberry_pi_camera_streamer/')
    os.system('make -C /home/pi/raspberry_pi_camera_streamer/build/')
    os.system('sudo make -C /home/pi/raspberry_pi_camera_streamer/build/ install')
    print('-------------------------------------------------------------------')
    print('...done')
    print('Install libs, tornado, sockjs...')
    print('-------------------------------------------------------------------')
    os.system('sudo apt-get install python-pip python-dev python-serial arduino')
    os.system('sudo pip install tornado ino')
    os.system('git clone https://github.com/mrjoes/sockjs-tornado.git')
    os.system('sudo python /home/pi/sockjs-tornado/setup.py install')
    print('-------------------------------------------------------------------')
    print('...done')
    print('Install pi co-op...')
    print('-------------------------------------------------------------------')
    os.system('git clone https://bitbucket.org/DawnRobotics/pi_co-op.git')
    os.system('sudo python /home/pi/pi_co-op/setup_pi_co-op.py install')
    print('-------------------------------------------------------------------')
    print('...done')
    print('Install robot web server and change skripts...')
    print('-------------------------------------------------------------------')
    os.system('git clone https://DawnRobotics@bitbucket.org/DawnRobotics/raspberry_pi_camera_bot.git')
    os.system('git clone https://github.com/BrixInMotion/RaspiRobot-Webcontrol.git')
    os.system('cp /home/pi/RaspiRobot-Webcontrol/Adafruit_I2C.py /home/pi/raspberry_pi_camera_bot/')
    os.system('cp /home/pi/RaspiRobot-Webcontrol/Adafruit_PWM_Servo_Driver.py /home/pi/raspberry_pi_camera_bot/')
    os.system('cp /home/pi/RaspiRobot-Webcontrol/DrivebyXMC.py /home/pi/raspberry_pi_camera_bot/')
    os.system('cp /home/pi/RaspiRobot-Webcontrol/mini_driver.py /home/pi/raspberry_pi_camera_bot/')
    os.system('cp /home/pi/RaspiRobot-Webcontrol/robot_controller.py /home/pi/raspberry_pi_camera_bot/')
    print('-------------------------------------------------------------------')
    print('...done')
    if raw_input('Do you want the Server to start automatically? (y/n)') == "y":
        os.system('sudo cp /home/pi/raspberry_pi_camera_bot/init.d/robot_web_server /etc/init.d/robot_web_server')
        os.system('sudo chmod a+x /etc/init.d/robot_web_server')
        os.system('sudo update-rc.d robot_web_server defaults')
        print('..done')
    else:
        print('Server does not start automatically, type $sudo python /home/pi/raspberry_pi_camera_bot/robot_web_server.py')
    if raw_input('Setup finished, do you want to reboot now? (y/n)') == "y":
        os.system('sudo reboot')
