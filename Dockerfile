FROM python:3.13-slim

COPY requirements.txt .

USER root

RUN python3 -m pip install  -r requirements.txt --user 

COPY ./app ./app

WORKDIR /app

CMD ["python3","-u","./jefferson.py"]

