FROM python:3.8

WORKDIR /app

#RUN echo "America/Mexico_City" > /etc/timezone
#RUN dpkg-reconfigure -f noninteractive tzdata
RUN sudo timedatectl set-timezone America/Mexico_City

RUN pip install -r requirements.txt



CMD [ "python" , "api.py"]