#!/bin/bash
service redis-server start
exec "$@"