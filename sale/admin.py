from django.contrib import admin

from sale.models import Sale


class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ventas_change_list.html'
    list_display = ('name', 'point_of_sale', 'price', 'cost', 'date_creation')
    search_fields = ('point_of_sale',)
    fieldsets = [
        ('Datos del producto', {
            'fields': ('name', 'price', 'cost')
        },),
        ('Datos de la venta', {
            'fields': ('point_of_sale',)
        },),
    ]
    exclude = ['hash', ]


# Register your models here.
admin.site.register(Sale, SaleAdmin)
