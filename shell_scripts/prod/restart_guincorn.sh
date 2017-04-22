#!/bin/sh

cd /home/cst/cst_production/cst/cst/

python manage.py supervisor --config-file=/home/cst/cst_production/cst/cst/settings/prod_supervisor.conf --settings=settings.prod_celery_settings restart tasks:gunicorn_prod
