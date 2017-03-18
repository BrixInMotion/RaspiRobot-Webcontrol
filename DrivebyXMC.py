# -*- coding: utf-8 -*-

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import smbus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  #GPIO-Nummerierung
GPIO.setwarnings(False) #Fehlermeldungen unterdruecken

#---------------------------------Variables----------------------------
#MCP23S17 Register
SPI_SLAVE_ADDR = 0x40
SPI_IOCTRL     = 0x0A
SPI_IODIRA     = 0x00
SPI_IODIRB     = 0x01
SPI_GPIOA      = 0x12
SPI_GPIOB      = 0x13

#MCP23S17-Pins
SCLK    = 11
MOSI    = 10
MISO    = 9
CS      = 22

#Variablen Kamera-servos
servoMax_h = 500    #ch8: hoehe, servoMin: unten
servomid_h = 385
servoMin_h = 270

servoMin_s = 320    #ch9: seite, servoMin: links
servomid_s = 435
servoMax_s = 550

#Variables Claw Servos
servoMax_claw = 630
servoMid_claw = 415
servoMin_claw = 200

servoMax_clawneck = 460
servoMid_clawneck = 330
servoMin_clawneck = 200


FrequenzMotor = 300 #300 Hz
FrequenzServo = 60  #60 Hz
servoMin = 0        # 0 for wheels, 350 for servos
servoMax = 700      #700 for wheels, 500 for servos
lastPWM = 300
lastAddr = 0x40

# Addr 0x40 for Adafuit board, 0x55 for XMC board

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)
pwm.setPWMFreq(60)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)
#--------------------------------------------------------------------
address_xmc = 0x55
bus = smbus.SMBus(1)
print("done")
# Registers of XMC:
SpeedLeftMotor = 0x01
SpeedRightMotor = 0x02
SpeedElevator = 0x03
WaitStep = 0x04
SpeedStepPlus = 0x05
SpeedStepMinus = 0x06

#bus.write_byte_data(address_xmc,register,value)
#--------------------------------------------------------------------
#GPIO Initialisierung
GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CS, GPIO.OUT)

GPIO.output(CS, GPIO.HIGH)
GPIO.output(SCLK, GPIO.LOW)
#----------------------------------------------------------
def sendValue(value):
    for i in range(8):
        if (value & 0x80):
            GPIO.output(MOSI, GPIO.HIGH)
        else:
            GPIO.output(MOSI, GPIO.LOW)
        GPIO.output(SCLK, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)
        value <<= 1

#----------------------------------------------------------
def sendSPI(opcode, addr, data):
    GPIO.output(CS, GPIO.LOW)
    sendValue(opcode)
    sendValue(addr)
    sendValue(data)
    GPIO.output(CS, GPIO.HIGH)
#----------------------------------------------------------
#Konfigurieren des MCP23S17
sendSPI(SPI_SLAVE_ADDR, SPI_IODIRA, 0x00)   #A als Ausgaenge
sendSPI(SPI_SLAVE_ADDR, SPI_IODIRB, 0xFF)   #B als Eingaenge
sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0x00)
#--------------------------------------------------------------------
def readSPI(opcode, addr):
    GPIO.output(CS, GPIO.LOW)
    sendValue(opcode|SPI_SLAVE_ADDR)
    sendValue(addr)
    value = 0
    for i in range(8):
        value <<= 1
        if(GPIO.input(MISO)):
            value |= 0x01
        GPIO.output(SCLK, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)
    GPIO.output(CS, GPIO.HIGH)
    return value
#--------------------------------------------------------------------
def initialize_bus():
	print("function")
#--------------------------------------------------------------------
def Drive(leftMotorSpeed, rightMotorSpeed):
    bus.write_byte_data(address_xmc,WaitStep, 0xa0)
    bus.write_byte_data(address_xmc,SpeedStepPlus, 0x02)
    bus.write_byte_data(address_xmc,SpeedStepMinus, 0x04)
    
    if leftMotorSpeed >= 0:
        leftspeed = int(leftMotorSpeed*0.5)      #leftMotor Speed: 0-80, Max Geschw.:40 -> speed*0.5
    elif leftMotorSpeed < 0:
        leftspeed = int(leftMotorSpeed*0.5*(-1)+127)
    if rightMotorSpeed >= 0:
        rightspeed = int(rightMotorSpeed*0.5)
    elif rightMotorSpeed < 0:
        rightspeed = int(rightMotorSpeed*0.5*(-1)+127)
    bus.write_byte_data(address_xmc,SpeedLeftMotor, leftspeed)
    bus.write_byte_data(address_xmc,SpeedRightMotor,rightspeed)
#--------------------------------------------------------------------
def Elevator_clawturn(Xclaw, Yelevator):
    #print (Yelevator)
    bus.write_byte_data(address_xmc,WaitStep, 0xa0)
    bus.write_byte_data(address_xmc,SpeedStepPlus, 0x02)
    bus.write_byte_data(address_xmc,SpeedStepMinus, 0x04)
	
    maxSpeedup = 100
    maxSpeeddown = 90
	
    if Yelevator >= 0:				#up
        bus.write_byte_data(address_xmc,SpeedElevator, int(maxSpeedup*Yelevator))
    elif Yelevator < 0:				#down
        bus.write_byte_data(address_xmc,SpeedElevator, int(0x80 - maxSpeeddown*Yelevator))
#--------------------------------------------------------------------
def Light(onoff):
    if onoff == 1:
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b10000000) 	#Light on
    elif onoff == 0:
	sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000) 	#Light off
#--------------------------------------------------------------------
def Relais(onoff):
    if onoff == 1:
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000010) #Relais on
        time.sleep(0.5)
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000)
    elif onoff == 0:
	sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000001) #Relais off
        time.sleep(0.5)
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000)
#--------------------------------------------------------------------		
def CentreCamera():
    pwm.setPWM(8, 0, servomid_h)	#Hoehe
    pwm.setPWM(9, 0, servomid_s)        #Seite

#--------------------------------------------------------------------		   
def Camera_servos(Xpos, Ypos):
    servo_seite = int(servomid_s + (servoMax_s - servomid_s)*Xpos)
    servo_hoehe = int(servomid_h + (servoMax_h - servomid_h)*Ypos)

    pwm.setPWM(8, 0, servo_hoehe)	#Hoehe
    pwm.setPWM(9, 0, servo_seite)	#Seite
#--------------------------------------------------------------------		
def Claw_servos(Xpos, Ypos):
    servo_clawNeck = int(servoMid_clawneck + (servoMax_clawneck - servoMid_clawneck)*(Ypos*(-1)) )
    servo_claw = int(servoMid_claw + (servoMax_claw - servoMid_claw)*Xpos)

    pwm.setPWM(10, 0, servo_claw)	#claw
    pwm.setPWM(11, 0, servo_clawNeck)	#clawNeck
#--------------------------------------------------------------------
##    if Ypos > 0.8: #vorwaerts (MSD 0: 0x01..0x7F)
##        bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x28)
##        bus.write_byte_data(address_xmc,SpeedRightMotor,0x28)
##    elif Ypos == 0 and Xpos == 0: #Stopp
##        bus.write_byte_data(address_xmc,SpeedLeftMotor,0)
##        bus.write_byte_data(address_xmc,SpeedRightMotor,0)
##    elif Ypos < -0.8: #Rueckwaerts (MSD gesetzt: 0x81..0xFF) 
##        bus.write_byte_data(address_xmc,SpeedLeftMotor, 0xa8)
##        bus.write_byte_data(address_xmc,SpeedRightMotor,0xa8)
##    if Xpos < -0.8: #links drehen
##        bus.write_byte_data(address_xmc,SpeedLeftMotor, (0x80 + 0x20))
##        bus.write_byte_data(address_xmc,SpeedRightMotor,0x20)
##    elif Xpos > 0.8: #rechts drehen
##        bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x20)
##        bus.write_byte_data(address_xmc,SpeedRightMotor,(0x80 + 0x20))
	     
    # elif Richtung=="u": #Plattform rauf
        # bus.write_byte_data(address_xmc,SpeedElevator, 0x40)
    # elif Richtung=="m": #Plattform runter
        # bus.write_byte_data(address_xmc,SpeedElevator, (0x80 + 0x40))
    # elif Richtung=="j": #Platform halt
        # bus.write_byte_data(address_xmc,SpeedElevator, 0x00)
