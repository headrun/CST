#!/bin/sh

cd /home/cst/cst_production/cst/cst/

python manage.py shell --settings=settings.prod_readonly_settings
