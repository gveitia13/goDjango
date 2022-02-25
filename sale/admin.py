from django.conf.locale.es import formats as es_formats
import django_excel as excel
from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from sale.models import Sale

es_formats.DATETIME_FORMAT = "d - M - Y"


class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ventas_change_list.html'
    list_display = ('name', 'cost', 'price', 'point_of_sale', 'date_creation')
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
    actions = ['Exportar_Seleccionadas_a_Excel', ]

    list_filter = (('date_creation', DateRangeFilter),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def Exportar_Seleccionadas_a_Excel(self, request, queryset):
        ventas = queryset
        export = []
        export.append([
            'Nombre',
            'Punto de venta',
            'Precio',
            'Costo',
            'Fecha de creación',
        ])
        for v in ventas:
            export.append([
                v.name,
                v.point_of_sale,
                v.price,
                v.cost,
                v.date_creation.strftime('%Y-%m-%d'),
            ])
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, 'xlsx',
                                   file_name='Ventas Seleccionadas.xlsx')


# Register your models here.
admin.site.register(Sale, SaleAdmin)
