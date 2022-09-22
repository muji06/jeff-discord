FROM python:3.10-buster

COPY requirements.txt .

USER root

RUN python3 -m pip install  -r requirements.txt --user 

COPY ./app ./app

WORKDIR /app

CMD ["python3","./jefferson.py"]
