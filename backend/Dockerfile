FROM python:3.10

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get -y update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y imagemagick

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
