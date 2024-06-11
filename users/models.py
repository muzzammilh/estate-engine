from django.db import models
from django.contrib.auth.models import AbstractUser

from config.models import BasedModel
from .managers import UserManager


class User(AbstractUser, BasedModel):
    LANDLORD = 1
    TENANT = 2

    USER_ROLES = [
        (LANDLORD, 'Landlord'),
        (TENANT, 'Tenant'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=USER_ROLES, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
