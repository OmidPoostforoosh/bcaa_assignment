FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add --update python python-dev py-pip build-base postgresql-dev gcc python3-dev musl-dev \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/* \
  && pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install -r requirements.txt
CMD python ./arxiv_cron.py
