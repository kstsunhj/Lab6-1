from bluedot.btcomm import BluetoothServer
from time import sleep
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
import speech_recognition as sr

def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(loops)
        
def data_received(data):
    
    try:
        print(data)
        sentence = data
        speak(sentence, 'en')
        
    except Exception as e:
        print(e)
    

s = BluetoothServer(data_received)

while (True):

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something: ")
        audio=r.listen(source)
    
    try:
        print("Google Speech Recognition thinks you said: ")
        sent = r.recognize_google(audio, language="en")
        print("{}".format(sent))
        if sent=='open':
            s.send('True')
            sleep(15)
        elif sent=='shutdown':
            s.send('False')
            sleep(5)

    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('No response from Google Speech Recognition service: {0}'.format(e))
    


