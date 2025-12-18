FROM python:3.12.10-slim
LABEL authors="Crocussys"

ENV SECTRETS_ENV_FILES=${SECTRETS_ENV_FILES}
ENV CUSTOMER_FILE=${CUSTOMER_FILE}
ENV WORK_DIR=/usr/src/app

WORKDIR ${WORK_DIR}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD [ "python", "./runserver.py" ]