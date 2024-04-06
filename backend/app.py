from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

import json

from fastapi import FastAPI

app = FastAPI()
config = cloudinary.config(secure=True)


@app.get("/")
def index():
    return {"Hello": "World"}


def uploadImage() -> str:
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
