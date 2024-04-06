FROM python:3.10

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsm6 \
  libxext6 \
  imagemagick \
  fonts-liberation \
  ghostscript \
  locales \
  && rm -rf /var/lib/apt/lists/*

COPY llm_server/requirements.txt llm_server/requirements.txt
RUN pip install --no-cache-dir -r llm_server/requirements.txt

ENV LC_ALL C.UTF-8

RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]