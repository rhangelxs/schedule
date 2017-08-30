#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

celery -A schedule.taskapp worker -l INFO
