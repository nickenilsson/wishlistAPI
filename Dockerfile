FROM ubuntu:14.04

RUN apt-get update && apt-get install \
		git \
		python-pip \
		python-dev
		rabbitmq-server
		redis-server -y

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /code
RUN pip install -e /code
EXPOSE 8080


CMD ["python", "code/wl_api/api.py"]
ENTRYPOINT ["/docker-entrypoint.sh"]