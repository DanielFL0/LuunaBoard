FROM centos:8

RUN dnf install python38 nginx -y 

WORKDIR /LuunaBoard

COPY . /LuunaBoard

RUN pip3 install -r requirements.txt 

RUN chmod +x startup.sh

EXPOSE 8000

CMD ["./startup.sh"]