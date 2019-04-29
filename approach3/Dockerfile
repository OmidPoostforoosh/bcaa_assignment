FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python ./arxiv_s3.py