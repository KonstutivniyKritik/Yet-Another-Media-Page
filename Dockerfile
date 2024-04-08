FROM python:3.11

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y


COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python", "TelegramBot.py"]