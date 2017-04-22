#!/bin/sh


cat ~/scripts/danger.txt

cd /home/cststage/cst_staging/cst/cst/

python manage.py shell --settings=setting.staging_settings
