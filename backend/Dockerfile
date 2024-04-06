FROM python:3.10

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get -y update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y imagemagick

RUN apt-get -y install fonts-liberation

RUN apt-get install -y locales && \
  locale-gen C.UTF-8 && \
  /usr/sbin/update-locale LANG=C.UTF-8

ENV LC_ALL C.UTF-8

RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
