#!/bin/sh

cd /home/cst/cst_staging/cst/cst/

python manage.py supervisor --config-file=/home/cststage/cst_staging/cst/cst/settings/staging_supervisor.conf --settings=settings.staging_celery_settings shell
