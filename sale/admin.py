import glob
import json
import os

from django.contrib import admin
from django.db import transaction
from rangefilter.filters import DateRangeFilter

from goDjango.settings import BASE_DIR
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
    actions = ['importJSON']

    def importJSON(self, request, queryset):
        user = request.user

        if os.path.exists(os.path.join(BASE_DIR / f'business/{user.name_hash}/import/')):
            directory = os.path.join(BASE_DIR / f'business/{user.name_hash}/import/')
            for filename in glob.iglob(os.path.join(directory, '*.json'), recursive=True):
                with open(filename) as js:
                    with transaction.atomic():
                        asd = json.load(js)
                        asd = asd[0] if type(asd) == list else asd
                        for v in asd.values():
                            if type(v) == dict:
                                if v.get('name') is not None:
                                    try:
                                        sale = Sale()
                                        sale.name = v['name']
                                        sale.price = v['price']
                                        sale.cost = v['cost']
                                        sale.point_of_sale = v['point_of_sale']
                                        sale.hash = v['hash']
                                        sale.save()
                                    except:
                                        pass
                        js.close()
                        os.remove(filename)

    importJSON.short_description = 'Actualizar Tabla'


# Register your models here.
admin.site.register(Sale, SaleAdmin)
