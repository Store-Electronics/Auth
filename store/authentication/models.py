from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    siret = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.username
