# Standard
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime, timedelta
import requests

# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ElevenLabs
from elevenlabs.client import ElevenLabs

# FastAPI
from fastapi import FastAPI

load_dotenv()

# Setup
app = FastAPI()
config = cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# HUGGINGFACE
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_CLIENT = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def generate_uuid():
    # Generate a random UUID
    uuid = "{:08x}-{:04x}-{:04x}-{:04x}-{:012x}".format(
        random.getrandbits(32),
        random.getrandbits(16),
        (random.getrandbits(12) & 0x0FFF) | 0x4000,
        (random.getrandbits(12) & 0x3FFF) | 0x8000,
        random.getrandbits(48),
    )
    return uuid


@app.get("/")
def index():
    return {"Hello": "World"}


def uploadFile(file: bytes, file_name: str, folder: str = "", file_type: str = 'auto') -> str:
    '''
    Use Cloudinary Upload to upload
    '''
    file_upload = cloudinary.uploader.upload(
        file, public_id=file_name, unique_filename=False, overwrite=True, folder=folder, resource_type=file_type
    )
    srcURL = file_upload['url']
    return srcURL


@app.post("/")
def upload():
    srcURL = uploadFile(
        "https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg", 'quickstart_butterfly'
    )
    return {"image": srcURL}


class VoiceBody(BaseModel):
    subtitles: List[str]


@app.post("/generateVoice")
async def generateVoice(VoiceBody: VoiceBody):
    allText = "\n".join(VoiceBody.subtitles)
    voiceList = ELEVENLABS_CLIENT.voices.get_all().voices
    selectedVoice = random.choices(voiceList)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio = ELEVENLABS_CLIENT.generate(text=allText, voice=selectedVoice[0])
    blob_name = f"audio_{current_time}_{generate_uuid()}.mp3"

    srcURL = uploadFile(b''.join(audio), blob_name, folder='audio', file_type="raw")
    return {"voice": srcURL}


@app.post("/generateMusic")
async def generateMusic():
    music_style = ["slow pace loopable advertisement music"]
    random_music = music_style[random.randint(0, len(music_style) - 1)]
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    audio_bytes = query(
        {
            "inputs": random_music,
        }
    )
    print(audio_bytes)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blob_name = f"music_{current_time}_{generate_uuid()}.mp3"
    srcURL = uploadFile(audio_bytes, blob_name, folder='music', file_type="raw")

    return {"music": srcURL}
