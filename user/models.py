from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    pass

class Admin(Group):
    pass

class Author(Group):
    pass

class Reader(Group):
    pass

