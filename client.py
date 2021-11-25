# -*-coding:utf8 -*-

from bluedot.btcomm import BluetoothClient
import subprocess
import RPi.GPIO as GPIO     # Import Raspberry Pi GPIO library
from time import sleep       # Import the sleep function from the time modul

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Set GPIO pin numbering as BCM
GPIO.setup(2,GPIO.OUT) #set GPIO pin2 as an output pin 
GPIO.setup(3,GPIO.OUT) #set GPIO pin2 as an output pin

def data_received(data):
    print(data)
    if (data[0] == '1'):
        if (data[2:4] == 'on'):
            GPIO.output(2, GPIO.HIGH)
            c.send('1號插座開啟')
        else :
            GPIO.output(2, GPIO.LOW)
            c.send('1號插座關閉')
    elif (data[0] == '2'):
        if (data[2:4] == 'on'):
            GPIO.output(3, GPIO.HIGH)
            c.send('2號插座開啟')
        else :
            GPIO.output(3, GPIO.LOW)
            c.send('2號插座關閉')
    elif (data[:7] == 'monitor'):
        p = subprocess.check_output('python lab3.py',shell=True)
        p = p.decode('utf-8')
        s = ""
        for i in p:
            s += i
        c.send(s)
        print(s)

c = BluetoothClient("mike", data_received)

while (True):
    pass
