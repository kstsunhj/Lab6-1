#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys 
import subprocess
from bluedot.btcomm import BluetoothServer

def data_received(data):
    print(data)
    message_from_server = "received" + data
    pp = subprocess.check_output("python3 tts.py "+data,shell=True)

s = BluetoothServer(data_received)

try:
    reload         # Python 2
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:  # Python 3
    from importlib import reload

import speech_recognition as sr

r = sr.Recognizer()
while(1):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something: ")
        audio=r.listen(source)

    try:
        print("Google Speech Recognition thinks you said: ")
        sent = r.recognize_google(audio, language="zh-TW")
        try:
            p = subprocess.check_output('python3 nlu.py {}'.format(sent),shell=True)
            p = p.decode('ascii')
            s.send(p)
            print("{}".format(p))
        except:
            print('Please say again')
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('No response from Google Speech Recognition service: {0}'.format(e))
