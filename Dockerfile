FROM ubuntu:14.04

RUN apt-get update && apt-get install \
		git \
		python-pip \
		python-dev -y

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /code

CMD ["python", "code/api.py"]
