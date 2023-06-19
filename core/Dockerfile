FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 0.0.0.0:8000


# rn  command 
# docker-compose build
# if want to run docker locally then 
# docker-compose up
# if want to cleanup resource then
# then from docker delete all the   
