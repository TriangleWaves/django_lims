FROM python:2.7

RUN mkdir /code
RUN mkdir /code/static
WORKDIR /code
COPY . /code

RUN pip install --upgrade pip

RUN pip install -r requirements.txt