import speech_recognition_custom.speech_recognition as sr
import json

#r = sr.Recognizer()

# Credentials for Watson Bluemix
ibm_username = '92ee7dca-6255-4648-bcca-d329515ee00a' #Skip-cred
ibm_password = 'Jole1aBC3vHp' #Skip-cred

def transcribe(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file
    return r.recognize_ibm_custom(audio, ibm_username, ibm_password)

def transcribe_json(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file
    return r.recognize_ibm_custom(audio, ibm_username, ibm_password, show_all=True)
