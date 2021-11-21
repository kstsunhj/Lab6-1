import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

import RPi.GPIO as GPIO #for adapter control
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)#set on pin 2
GPIO.setup(3,GPIO.OUT)#set on pin 3
from time import sleep

from bluedot.btcomm import BluetoothClient

# Connect to the sensor
sensor = serial.Serial(
						port='/dev/ttyUSB0',
						baudrate=9600,
						bytesize=8,
						parity='N',
						stopbits=1,
						xonxoff=0
					)

master = modbus_rtu.RtuMaster(sensor)
master.set_timeout(2.0)
master.set_verbose(True)


def readData():
	data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

	voltage = data[0] / 10.0 # [V]
	current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
	power = (data[3] + (data[4] << 16)) / 10.0 # [W]
	energy = data[5] + (data[6] << 16) # [Wh]
	frequency = data[7] / 10.0 # [Hz]
	powerFactor = data[8] / 100.0
	alarm = data[9] # 0 = no alarm

	print('Voltage [V]: ', voltage)
	print('Current [A]: ', current)
	print('Power [W]: ', power) # active power (V * I * power factor)
	print('Energy [Wh]: ', energy)
	print('Frequency [Hz]: ', frequency)
	print('Power factor []: ', powerFactor)
	print('Alarm : ', alarm)

	response = 'Voltage : {} , Current : {} , Power : {} , Energy : {} , Frequency : {} , Power factor : {} , Alarm : {}'.format(
			voltage, current, power, energy, frequency, powerFactor, alarm)
	
	return response

def data_received(data):
	command = data
	if command == "1":
		print("left adapter has been turned on")
		GPIO.output(2, GPIO.HIGH)

		response = 'left adapter has been turned on'

	elif command == "2":
		print("right adapter has been turned on")
		GPIO.output(3, GPIO.HIGH)

		response = 'right adapter has been turned on'
		
	elif command == "3":
		print("left adapter has been turned off")
		GPIO.output(2, GPIO.LOW)

		response = 'left adapter has been turned off'

	elif command == "4":
		print("right adapter has been turned off")
		GPIO.output(3, GPIO.LOW)

		response = 'right adapter has been turned off'

	elif command == "5":
		print("Server ask for detection")

		response = readData()
	else:
		response = "Command error, please insert next command..."
			
	c.send(response)

c = BluetoothClient("109062581_Pi", data_received)

while (True):
	pass

try:
	master.close()
	if sensor.is_open:
		sensor.close()
except:
	pass
