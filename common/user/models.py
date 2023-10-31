from django.contrib.auth.models import AbstractUser
from django.db import models

from common.user.base import BaseModel


class UserRole(models.IntegerChoices):
    ADMIN = 1, "ADMIN"
    WAITER = 2, "WAITER"
    CLIENT = 3, "CLIENT"


class User(AbstractUser, BaseModel):
    first_name = None
    last_name = None
    role = models.IntegerField(choices=UserRole.choices, default=UserRole.CLIENT)
    name = models.CharField("Name of User", max_length=100)

    def __str__(self):
        return "USER:" + ' ' + str(self.username)
