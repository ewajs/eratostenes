FROM python:3.7-alpine

WORKDIR /app/src

RUN apk update && apk upgrade && apk add gcc musl-dev libffi-dev openssl-dev

COPY ./src .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["./entrypoint.sh"]