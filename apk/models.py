import hashlib
from datetime import datetime

import qrcode
from crum import get_current_user
from django.db import models
from django.utils.safestring import mark_safe

from goDjango import settings
from user.models import User


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


# Create your models here.
class ConfiguracionGodjango(models.Model):
    dns = models.CharField(max_length=500)
    puerto = models.CharField(max_length=500)

    def __str__(self):
        return 'Configuraciones de ámbito global'

    class Meta:
        verbose_name_plural = '*  Configuraciones de ámbito global'
        verbose_name = 'Configuración de ámbito global'
        # app_label = 'godjango'


class Configuration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User.objects.first().pk)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Configuraciones'
        verbose_name = 'Configuración'


class ApkAccess(models.Model):
    cfg = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    point_of_sale = models.CharField(max_length=100, verbose_name='Punto de venta')
    operator = models.CharField(max_length=100, verbose_name='Operador')
    qr = models.CharField(max_length=900, blank=True, null=True)
    state = models.BooleanField(default=True, verbose_name='Habilitado')
    apkidhash = models.CharField(max_length=900, blank=True, null=True)

    def __str__(self):
        return self.point_of_sale

    def qr_tag(self):
        return mark_safe('<img src="/media/%s" width="300" height="300" />' % (str(self.qr)))

    qr_tag.short_description = 'Vista previa'

    def show_url(self):
        return mark_safe("<a download = 'Obtener QR' href='/media/%s'>%s</a>" % (str(self.qr), 'Obtener QR'))

    show_url.short_description = 'Url'

    def save(self, *args, **kwargs):
        if not self.qr:
            user = self.cfg.user
            qr = qrcode.make()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=50,
                border=4,
            )
            apkidhash = hash_string(str(self.operator + self.point_of_sale + str(datetime.utcnow))) + '.sd'
            qr.add_data({
                'dns': str(ConfiguracionGodjango.objects.all()[0].dns),
                'id': str(self.cfg.user.name_hash),
                'apk_id': apkidhash,
                'port': str(ConfiguracionGodjango.objects.all()[0].puerto),
                'punto_venta': self.point_of_sale,
            })
            self.apkidhash = apkidhash

            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            # self.save()
            # if ApkAccess.objects.last() is not None:
            if ApkAccess.objects.last().pk:
                pk = ApkAccess.objects.last().pk + 1
            else:
                pk = 1
            self.qr = "/qr/" + str(pk) + '.png'
            self.save()
            img.save("media/qr/" + str(pk) + '.png')
        super(ApkAccess, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Accesos a APK'
        verbose_name = 'Acceso a APK'


class Product(models.Model):
    cfg = models.ForeignKey(Configuration, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.FloatField(default=0.00, verbose_name='Precio')
    cost = models.FloatField(default=0.00, verbose_name='Costo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     user = get_current_user()
    #     if user is not None:
    #         if not self.pk:
    #             self.user_creation = user
    #         else:
    #             self.user_updated = user
    #     super(Product, self).save()
