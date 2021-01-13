#!/bin/bash

celery -A celery_app.app worker --loglevel=INFO -Q celery -E -n celery1@%h -Ofair&
celery -A celery_app.app worker --loglevel=INFO -Q celery -E -n celery2@%h -Ofair&
celery -A celery_app.app worker --loglevel=INFO -Q high_priority -E -n high_priority@%h&
tail -f /dev/null
