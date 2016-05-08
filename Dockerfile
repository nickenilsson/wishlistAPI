FROM ubuntu:14.04

RUN apt-get update && apt-get install \
		git \
		python-pip \
		python-dev \
		redis-server -y

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /code
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
RUN pip install -e /code
EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "code/wl_api/api.py"]
