# Standard
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime, timedelta

# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ElevenLabs
from elevenlabs import generate as generate_voice, set_api_key, voices

# FastAPI
from fastapi import FastAPI

load_dotenv()

# Setup
app = FastAPI()
config = cloudinary.config(secure=True)

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
set_api_key(ELEVENLABS_API_KEY)


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


def uploadImage() -> str:
    '''
    Use Cloudinary Upload to upload
    '''
    cloudinary.uploader.upload(
        "https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg",
        public_id="quickstart_butterfly",
        unique_filename=False,
        overwrite=True,
    )
    srcURL = cloudinary.CloudinaryImage("quickstart_butterfly").build_url()
    print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
    return srcURL


@app.post("/")
def upload():
    srcURL = uploadImage()
    return {"image": srcURL}


class VoiceBody(BaseModel):
    subtitles: List[str]


@app.post("/generateVoice")
async def generateVoice(VoiceBody: VoiceBody):
    allText = "\n".join(VoiceBody.subtitles)
    voiceList = voices()
    print(voiceList)
    selectedVoice = random.choices(voiceList)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # audio = generate_voice(text=allText, voice=selectedVoice[0])
    # blob_name = f"audio_{current_time}_{generate_uuid()}.mp3"
    return "Hi"
    # blob_client = blob_service_client.get_blob_client(container="audio", blob=blob_name)
    # blob_client.upload_blob(audio, overwrite=True)
    # blob_uri = blob_client.url
