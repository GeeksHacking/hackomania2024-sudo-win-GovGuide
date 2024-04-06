# Standard
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime
import requests
from urllib.parse import quote
import aiohttp
import asyncio
from uuid import uuid4


# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ElevenLabs
from elevenlabs.client import ElevenLabs

# FastAPI
from fastapi import FastAPI

# Whisper
import whisper_timestamped as whisper

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

# PEXELS
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


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

    # SRT File
    whisper_audio = whisper.load_audio(srcURL)
    model = whisper.load_model("base")

    result = whisper.transcribe(model, whisper_audio, language="en")

    srt_file = ""

    for i, segment in enumerate(result["segments"]):
        start, end = segment["start"], segment["end"]
        srt_file += f"{i + 1}\n00:00:{str(int(start)).replace('.', ',')} --> 00:00:{str(int(end)).replace('.', ',')}\n{segment['text'].strip()}\n"
    srt_blob_name = f"subtitles_{current_time}_{generate_uuid()}.srt"
    with open(srt_blob_name, 'w') as f:
        f.write(srt_file)
        f.close()
    with open(srt_blob_name, 'rb') as f:
        data = f.read()
        srt_srcURL = uploadFile(data, srt_blob_name, folder='srt', file_type="raw")
        f.close()
    os.remove(srt_blob_name)
    return {"audio": srcURL, "srt_file": srt_srcURL}


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


class VideoBody(BaseModel):
    scene: List[str]


async def fetch_video(session, scene):
    url = f"https://api.pexels.com/videos/search?query={quote(scene)}&per_page=1&orientation=landscape&size=medium"
    async with session.get(url, headers={"Authorization": PEXELS_API_KEY}) as response:
        response_content = await response.json()
        return response_content


async def generate_video(scene):
    async with aiohttp.ClientSession() as session:
        response_content = await fetch_video(session, scene)
        blob_storage_array = []
        if len(response_content["videos"]) > 0:
            video_link = None
            for video in response_content["videos"][0]["video_files"]:
                if video["quality"] == "hd":
                    video_link = video["link"]
                    break
            if not video_link:
                video_link = response_content["videos"][0]["video_files"][0]["link"]
            async with session.get(video_link) as video_response:
                video_data = await video_response.read()
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                blob_name = f"{scene}_{current_time}_{str(uuid4())}"
                src_url = uploadFile(video_data, blob_name, folder='video', file_type="video")
                blob_storage_array.append(src_url)
        return blob_storage_array


@app.post("/generateVideo")
async def generate_video_handler(VideoBody: VideoBody):
    tasks = [generate_video(scene) for scene in VideoBody.scene]
    results = await asyncio.gather(*tasks)
    return {"video": [url for urls in results for url in urls]}
