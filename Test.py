import sounddevice as sd
import torch
import numpy
from scipy.io.wavfile import write
import whisper
import webbrowser
from AppOpener import open
import pyttsx3

model = whisper.load_model("base")
freq = 44100
duration = 5
cont = 'y'
engine = pyttsx3.init()

while(cont != 'n'):

    print("Say Something...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    write("recording0.mp3", freq, recording)

    audioFile = "recording0.mp3"
    audio = whisper.load_audio(audioFile)
    result = model.transcribe(audioFile)
    text = result["text"]
    print(text)
    text = text.lower()

    #Open YouTube
    index = text.find("open youtube")
    if(index != -1):
        engine.say("opening youtube.")
        webbrowser.open("https://www.youtube.com")
        engine.runAndWait()
        cont = input("Do Something Else? (y/n): ").lower()
        continue
    
    #Open Google
    index = text.find("open google")
    if(index != -1):
        engine.say("opening google.")
        webbrowser.open("https://www.google.com")
        engine.runAndWait()
        cont = input("Do Something Else? (y/n): ").lower()
        continue
    
    #Open App
    index = text.find("open")
    #print(index)
    if(index != -1):
        open(text[5:len(text) - 1], match_closest=True)
    cont = input("Do Something Else? (y/n): ").lower()

    pipe(text)