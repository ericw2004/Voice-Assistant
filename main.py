from typing import Union, Annotated
from fastapi import FastAPI, HTTPException, File, UploadFile, Form# type: ignore
from pydantic import BaseModel
import requests
import json
import whisper
import smtplib
from email.mime.text import MIMEText


model = whisper.load_model("base")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}@app.get("/items/{item_id}")


def llm(msg):
    res=''
    url = "http://localhost:11434/api/generate" 
    headers = {'Content-Type': 'application/json'} 
    data = { 'model': 'llama3.2:3b', 'prompt': "In a 100 word or less summary: " + msg, 'stream':False } 
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200: 
        response_text = response.text
        data = json.loads(response_text)
        res=actual_response = data["response"]
        print(actual_response)
    else: 
        print("Error Occurred:", response.text)

    return res



@app.get("/llm/{item_id}")
def llm_res(item_id: str, q: Union[str, None] = None):
    prompt = "In a 100 or less word summary: "
    prompt = prompt + item_id
    try:
        msg=llm(prompt)
        return {"generated_text": msg}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")
    # response: ChatResponse = chat(model='llama3.2:1b', messages=[
    # {
    #     'role': 'user',
    #     'content': prompt,
    # },
    # ])
    res = ""#(response['message']['content'])
    return {"item_id": item_id, "q": res}

class Item(BaseModel):
    type: str
    name: str

def process(audioFile):
    audio = whisper.load_audio(audioFile)
    result = model.transcribe(audioFile)
    text = result["text"]
    print(text)
    text = text.lower()
    return text

@app.post("/transcribe")
async def upload_mp3(file: UploadFile = File(...)):
    file_path = "song.mp3"  # Choose your desired file name and path
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    text = process(file_path)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("ericwaterhouse36@gmail.com", "uteq zwwx vnzl fvyg")
    s.sendmail("ericwaterhouse36@gmail.com", "eric.waterhouse26@houghton.edu", text)
    s.quit()
    return {"message": "Email sent..."}

@app.post("/generate_text")
async def upload_mp3(file: UploadFile = File(...)):
    file_path = "audio.mp3"  # Choose your desired file name and path
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    m2=(f"MP3 file saved to {file_path}")
    text = process(file_path)
    res = llm(text)
    return {"message": res, "m2":m2}

@app.post("/summary")
async def upload_mp3(file: UploadFile = File(...)):
    file_path = "audio.mp3"  # Choose your desired file name and path
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    m2=(f"MP3 file saved to {file_path}")
    text = process(file_path)
    res = llm("Generate a short summary of this lecture: " + text)
    return {"message": text}

@app.post("/study_questions")
async def upload_mp3(file: UploadFile = File(...)):
    file_path = "audio.mp3"  # Choose your desired file name and path
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    m2=(f"MP3 file saved to {file_path}")
    text = process(file_path)
    res = llm("Generate 10 study questions based on this lecture: " + text)
    return {"message": text}



@app.post("/all")
async def upload_mp3(file: UploadFile = File(...)):
    file_path = "audio.mp3"  # Choose your desired file name and path
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    m2=(f"MP3 file saved to {file_path}")
    text = process(file_path)
    summary = llm("Generate a short summary of this lecture: " + text)
    study = llm("Generate 10 study questions based on this lecture: " + text)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("ericwaterhouse36@gmail.com", "uteq zwwx vnzl fvyg")
    s.sendmail("ericwaterhouse36@gmail.com", "eric.waterhouse26@houghton.edu", summary)
    s.sendmail("ericwaterhouse36@gmail.com", "eric.waterhouse26@houghton.edu", study)
    s.quit()
    return {"message": "Emails sent. Hopefully this works!"}