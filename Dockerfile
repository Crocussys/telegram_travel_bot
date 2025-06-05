FROM python:3.12.10-slim
LABEL authors="Crocussys"

ENV BOT_TOKEN=${BOT_TOKEN}
ENV BOT_PROVIDER_TOKEN=${BOT_PROVIDER_TOKEN}
ENV WORK_DIR=/usr/src/app

WORKDIR ${WORK_DIR}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]