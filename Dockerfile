FROM python:3.11-alpine3.19

ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN sed -i 's/https/http/' /etc/apk/repositories
RUN apk update && apk add --no-cache dcron
RUN apk add build-base
RUN apk add libffi-dev

COPY . /diplomaback

WORKDIR /diplomaback

RUN python -m venv venv
RUN source venv/bin/activate
COPY requirements.txt .


ENV PYTHONPATH=/diplomaback
WORKDIR /diplomaback/src
RUN pip install -r ../requirements.txt

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["main.py"]
