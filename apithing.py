import requests 
import json
import numpy
import sounddevice as sd
from scipy.io.wavfile import write

freq = 44100
duration = 5

print("Recording...")
recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
sd.wait()
print("Done!")
write("testrecording.mp3", freq, recording)

url = "http://localhost:8000/uploadmp3"
filepath = "testrecording.mp3"

with open(filepath, 'rb') as audio_file:
    files = {'file': (filepath, audio_file, 'audio/mpeg')}
    response = requests.post(url, files=files)

if response.status_code == 200:
    print('Success!')
    print(response.text)
else:
    print('Error:', response.status_code)
    print(response.text)