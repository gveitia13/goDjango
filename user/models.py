from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    name_hash = models.CharField(max_length=900,blank=True,null=True)

    def __str__(self):
        return self.username
