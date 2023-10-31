FROM python:3.9-slim

RUN apt-get update && apt-get install -y fail2ban

EXPOSE 8042

WORKDIR /opt

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /opt

HEALTHCHECK --interval=30s --timeout=15s --start-period=5s --retries=3 CMD python3 health.py

ENV IN_DOCKER_CONTAINER 1
LABEL name="bonsai_server"

ENTRYPOINT [ "python3", "-u", "fail2ban-exporter.py" ]
