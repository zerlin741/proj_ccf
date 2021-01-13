#!/bin/bash

sudo rabbitmq-plugins enable rabbitmq_management

flower -A celery_app.app --broker=amqp://guest:guest@localhost:5672/celery  --broker_api=http://guest:guest@localhost:15672/api/
