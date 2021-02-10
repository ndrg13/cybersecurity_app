FROM python:latest

COPY . /src

RUN apt update && apt install -y vim git && pip install Flask requests flask-cors pyOpenSSL bcrypt

EXPOSE 5000

CMD export FLASK_APP=/src/run && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=5000 --cert=/src/cert.pem --key=/src/key.pem


