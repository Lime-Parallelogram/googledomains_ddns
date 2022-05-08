# Must use python 3.10 or above because of match-case statement
FROM python:3.10

ENV USERNAME="UNSET"
ENV PASSWORD="UNSET"
ENV HOSTNAME="UNSET"
ENV TIMEOUT=8
#Allows printed output to be shown in logs
ENV PYTHONUNBUFFERED=1

RUN pip install requests

WORKDIR /usr/src/app
COPY ddns_update.py .

CMD ["python", "ddns_update.py"]