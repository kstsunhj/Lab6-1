from bluedot.btcomm import BluetoothClient
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
from signal import pause
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
GCD = 0
def sendAC():
    print("\n connected and recieved \n")
    # Connect to the sensor
    
    sensor = serial.Serial(
    #                       port='/dev/PZEM_sensor',
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
    AC = 'Voltage [V]: ' + str(voltage) + '\n' + 'Current [A]: ' + str(current) + '\n' + 'Power [W]: ' + str(power) + '\n' + 'Energy [Wh]: ' + str(energy) + '\n' + 'Frequency [Hz]: ' + str(frequency) + '\n' + 'Power factor []: ' + str(powerFactor) + '\n' + 'Alarm : ' + str(alarm)
    # Changing power alarm value to 100 W
    # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)

    try:
        master.close()
        if sensor.is_open:
            sensor.close()
    except:
        pass

    c.send('AC: ' + AC)

def data_received(data):
    print("data:",data)
    if(data == 'turn_on_light_OK'):
        print("connected and data = on")
        GCD = 1
        if(GCD == 1):
            GCD = 0
            sendAC()
c = BluetoothClient("pi0315", data_received)
c.send("hello server")

    



while(True):

    pass


