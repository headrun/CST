[DO NOT RENAME THE FILES in nginx_config folder]
IMP: Files contains Symbolic linke in /etc/nginx/sites-enabled/

PROD
----
create symbolic link
run :
sudo ln -s /home/cst/cst_production/cst/nginx_config/prod/cst_prod.conf /etc/nginx/site-enabled/cst_prod.conf



STAGING
-------
create symbolic link
run :
sudo ln -s /home/cst/cst_staging/cst/nginx_config/staging/cst_staging.conf /etc/nginx/site-enabled/cst_staging.conf
