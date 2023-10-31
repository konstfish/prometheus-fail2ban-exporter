FROM python:3.9-slim

RUN apt-get update && apt-get install -y fail2ban

EXPOSE 8042

WORKDIR /opt

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /opt

ENTRYPOINT [ "python3", "-u", "fail2ban-exporter.py" ]
