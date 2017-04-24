import datetime
import math
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from accounts import mod

def login(request):
    user = request.user
    dob = datetime(request.POST.get('dob'))
    mod.update_dob(user, dob)
	return render(request, 'accounts/login.html')
