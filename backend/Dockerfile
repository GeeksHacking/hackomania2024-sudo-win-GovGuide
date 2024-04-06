FROM python:3.10

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get -y update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y imagemagick

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app"]
