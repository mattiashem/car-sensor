from python:3.4-alpine
RUN apk add g++
RUN apk add musl-dev
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt


CMD python main.py