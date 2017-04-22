#!/bin/sh

cd /home/cststage/cst_staging/cst/cst/

python manage.py shell --settings=settings.staging_readonly_settings
