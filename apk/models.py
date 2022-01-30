import hashlib

from django.db import models

from user.models import User


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


# Create your models here.
class ConfiguracionGodlango(models.Model):
    dns = models.CharField(max_length=500)
    puerto = models.CharField(max_length=500)

    def __str__(self):
        return 'Configuraciones de ámbito global'

    class Meta:
        verbose_name_plural = '*  Configuraciones de ámbito global'
        verbose_name = 'Configuración de ámbito global'
        app_label = 'godjango'


class Configuration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '01 - Configuraciones'
        verbose_name = 'Configuración'
