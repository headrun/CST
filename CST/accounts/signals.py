from django.contrib.auth.models import User 
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tastypie.models import create_api_key 

# create api for user when a user is created
models.signals.post_save.connect(create_api_key, sender=User)
