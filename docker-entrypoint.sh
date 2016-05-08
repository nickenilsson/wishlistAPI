#!/bin/bash
service redis-server start
service rabbitmq-server start
exec "$@"