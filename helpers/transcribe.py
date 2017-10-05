import speech_recognition_custom.speech_recognition as sr
import json

from watson_developer_cloud import SpeechToTextV1

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


def transcribe_watson(wav_file):
    '''Uses IBM Watson speech to text API for input WAV file'''
    stt = SpeechToTextV1(username=ibm_username, password=ibm_password)
    audio_file = open(wav_file, "rb")

    #keywords = ['Erin']
    with open('transcript_result.json', 'w') as fp:
        result = stt.recognize(audio_file, 
                               #keywords= str(keywords),
                               #keywords_threshold= 0.01,
                               speaker_labels= True,
                               content_type="audio/wav",
                               timestamps=True,
                               max_alternatives=1)
        json.dump(result, fp, indent=2)
        return result