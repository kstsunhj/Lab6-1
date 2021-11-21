#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys 
try:
	reload         # Python 2
	reload(sys)
	sys.setdefaultencoding('utf8')
except NameError:  # Python 3
	from importlib import reload

import tempfile
from gtts import gTTS
from pygame import mixer
import time

# Control speaker to play given sentence
def speak(sentence, lang='en', loops=1):
	with tempfile.NamedTemporaryFile(delete=True) as fp:
		tts = gTTS(text=sentence, lang=lang)
		tts.save('{}.mp3'.format(fp.name))
		mixer.init()
		mixer.music.load('{}.mp3'.format(fp.name))
		mixer.music.play(loops)
		while mixer.music.get_busy():
			time.sleep(1)

from bluedot.btcomm import BluetoothServer
import speech_recognition as sr

flag = False;
# Callback function for receiving data from client via bluetooth
def data_receive(data):
	global flag
	print(data)
	speak(data)
	flag = False;

s = BluetoothServer(data_receive)
r = sr.Recognizer()

import configparser
import urllib    
import uuid
import json
import requests

# Parameters for TTS
lang = 'zh-tw'
timezone = 'Asia/Taipei'
# Read configurations for NLP
config = configparser.ConfigParser()
config.read('lab6_assignment.conf')
project_id = config.get('dialogflow', 'project_id')
authorization = config.get('dialogflow', 'authorization')
# Valid responds from NLP
valid_commands = ['left_adapter_on', 'right_adapter_on', 'left_adapter_off', 'right_adapter_off', 'data_read']

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source, duration=1)
	while(True):
		# Waiting for previous command complete
		while(flag):
			time.sleep(1)
		# Begin to receive speech command
		print("Say something...")
		audio=r.listen(source)
		try:
			# Speech to text
			speech_text = r.recognize_google(audio, language="zh-TW")
			print(speech_text)
			# Nature language processing
			session_id = str(uuid.uuid1())
			url = 'https://dialogflow.googleapis.com/v2/projects/' + project_id +'/agent/sessions/' + session_id + ':detectIntent'
			headers = {
				"accept": "application/json",
				"authorization": authorization
			}
			payload = {
				"queryInput": {
					"text": {
						"text": speech_text, 
						"languageCode": lang
					}
				}, 
				"queryParams": {
					"timeZone": timezone
				}
			}
			response = requests.post(url, data=json.dumps(payload), headers=headers)
			
			data = json.loads(response.text)
			fulfillment = data['queryResult']['fulfillmentText']
			
			# Send command to client via bluetooth
			if fulfillment in valid_commands:
				cmd = str(valid_commands.index(fulfillment)+1)
				s.send(cmd)
				flag = True
			else:
				print('Unrecongnizable command, please try again.')
			
		except sr.UnknownValueError:
			print('Google Speech Recognition could not understand audio')
		except sr.RequestError as e:
			print('No response from Google Speech Recognition service: {0}'.format(e))
		