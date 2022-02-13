import rangefilter
from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

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
    # list_filter = (('date_creation', DateRangeFilter),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


# Register your models here.
admin.site.register(Sale, SaleAdmin)
