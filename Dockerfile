FROM ubuntu:latest

RUN apt update && apt upgrade -y

CMD ln -snf /usr/share/zoneinfo/Europe/Kiev /etc/localtime && echo "Europe/Kiev" > /etc/timezone

RUN apt install git wget python3 python3-pip nano -y

RUN pip install -r requirements.txt

COPY main.py /home

CMD ['python', 'main.py']
