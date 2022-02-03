from django.db import models


# Create your models here.


class Sale(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio')
    cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Costo')
    point_of_sale = models.CharField(max_length=900, verbose_name='Punto de venta')
    hash = models.CharField(max_length=900, primary_key=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Fecha de creación')
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Venta'
        ordering = ['-date_creation']
