from bluedot.btcomm import BluetoothClient
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import RPi.GPIO as GP
from time import sleep

GP.setmode(GP.BCM)
GP.setup(4,GP.OUT)
 
def data_received(data):
    print(data)
    if data=='True':
        sleep(2)

        # turn on the plug
        GP.output(4,GP.HIGH)
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
        sleep(2)
        # collect the data from the pzem
        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

        voltage = data[0] / 10.0 # [V]
        current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
        power = (data[3] + (data[4] << 16)) / 10.0 # [W]
        energy = data[5] + (data[6] << 16) # [Wh]
        frequency = data[7] / 10.0 # [Hz]
        powerFactor = data[8] / 100.0
        alarm = data[9] # 0 = no alarm

        # print the data information to check 
        # the data received at the server is correct or not
        print('Voltage [V]: ', voltage)
        print('Current [A]: ', current)
        print('Power [W]: ', power) # active power (V * I * power factor)
        print('Energy [Wh]: ', energy)
        print('Frequency [Hz]: ', frequency)
        print('Power factor []: ', powerFactor)
        print('Alarm : ', alarm)
        
        try:
            master.close()
            if sensor.is_open:
                sensor.close()
        except:
            pass
        
        # make the data sent to server as a string
        # or it will be error
        STR = 'Voltage is '+str(voltage)+' [V]\nCurrent is '+str(current)\
                +' [A]\nPower is '+str(power)+' [Watt]\nEnergy is '+str(energy)+' [Watt-hour]\n'

        c.send(STR)
        
    elif(data=='False'):
        # make the pluf shut down.
        GP.output(4,GP.LOW)
        c.send('already shutdown')

# turn on the client
c = BluetoothClient('Pi6', data_received)

# check the Server be able to connect
c.send('Hi!')
while(True):
    pass