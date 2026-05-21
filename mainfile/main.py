from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOUR ELEVENLABS API KEY
ELEVENLABS_API_KEY = "sk_d3d8a9d6b6443c9d0d5309899e88279838bbf19de30a7997"

# VOICE ID
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

@app.get("/")
def home():

    return {
        "message": "AI Voice Assistant Running"
    }

@app.get("/speak")
def speak(text: str):

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    print("STATUS:", response.status_code)

    if response.status_code != 200:

        print(response.text)

        return {
            "error": response.text
        }

    with open("voice.mp3", "wb") as f:

        f.write(response.content)

    return FileResponse(
        "voice.mp3",
        media_type="audio/mpeg"
    )