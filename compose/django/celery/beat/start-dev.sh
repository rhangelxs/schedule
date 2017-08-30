#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

rm -f './celerybeat.pid'
celery -A schedule.taskapp beat -l INFO
