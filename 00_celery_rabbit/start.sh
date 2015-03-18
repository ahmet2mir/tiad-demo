#!/bin/bash

# start celery
fig -f celery.yml -p demo up -d

# start rabbitmq
fig -f rabbitmq.yml -p demo up -d

sleep 3

# create rabbitmq user
docker exec -t demo_broker_1 rabbitmqctl add_user myuser mypassword
docker exec -t demo_broker_1 rabbitmqctl add_vhost myvhost
docker exec -t demo_broker_1 rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

# gui for flower and rabbitmq
fig -f flower.yml -p demo up -d
