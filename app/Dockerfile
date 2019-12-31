FROM python:3.7-alpine

WORKDIR /app/src

COPY ./src .

RUN apk update && apk upgrade && apk add gcc musl-dev libffi-dev openssl-dev \
    && pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]