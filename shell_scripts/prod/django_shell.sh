#!/bin/sh


cat ~/scripts/danger.txt

cd /home/cst/cst_production/cst/cst/

python manage.py shell --settings=settings.prod_settings
