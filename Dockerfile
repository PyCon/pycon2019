FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements /code/requirements
RUN pip install -r /code/requirements/dev.txt
ADD . /code/
