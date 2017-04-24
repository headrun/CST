import datetime
import factory

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone

from factory.django import DjangoModelFactory

from accounts import models


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'test_{}'.format(n))
    password = make_password('my_password')
    email = factory.LazyAttribute(lambda o: '{}@example.org'.format(o.username))
    is_active = True
    is_superuser = False
    is_staff = False


class EmptyUserProfileFactory(DjangoModelFactory):
    FACTORY_FOR = models.Profile

    user = factory.SubFactory(UserFactory)


class UserProfileFactory(DjangoModelFactory):
    FACTORY_FOR = models.Profile
    
    user = factory.SubFactory(UserFactory)
    dob = datetime.date(1990, 01, 01)
