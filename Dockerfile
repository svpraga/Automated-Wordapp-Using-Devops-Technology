FROM python:3.8-alpine

RUN mkdir -p /application

COPY requirements.txt /application

WORKDIR /application

RUN pip install -r requirements.txt

COPY . /application

EXPOSE 4000

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]



