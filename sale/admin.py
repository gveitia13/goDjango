import datetime

from django.contrib import admin

# Register your models here.
from rangefilter.filters import DateRangeFilter

from sale.models import Sale


class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'point_of_sale', 'price', 'cost', 'date_creation')
    search_fields = ('point_of_sale',)
    list_filter = (
        ('date_creation', DateRangeFilter),)
    fieldsets = [
        ('Datos del producto', {
            'fields': ('name', 'price', 'cost')
        },),
        ('Datos de la venta', {
            'fields': ('point_of_sale',)
        },),
    ]
    exclude = ['hash', ]


admin.site.register(Sale, SaleAdmin)
