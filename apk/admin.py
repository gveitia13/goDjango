from django.contrib import admin
from apk.forms import ApkAccessForm, ProductForm
from apk.models import ApkAccess, Product, Configuration, ConfiguracionGodjango


# inilines
class ApkAccessInLine(admin.StackedInline):
    fieldsets = [
        ('Datos', {
            'fields': (('operator', 'point_of_sale'), ('qr_tag', 'show_url'), 'state')
        }),
    ]
    readonly_fields = ('qr_tag', 'show_url')
    model = ApkAccess
    form = ApkAccessForm
    extra = 0


class ProductInline(admin.StackedInline):
    model = Product
    form = ProductForm
    extra = 0


def Exportar_Productos_a_PDF(modeladmin, request, queryset):
    queryset = queryset
    for q in queryset:
        print(ApkAccess.objects.filter(cfg=q.cfg))

    print('---------------------')
    for a in ApkAccess.objects.all():
        pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cost',)
    fieldsets = [
        ('Datos del producto', {
            'fields': ('name', 'price', 'cost', 'cfg')
        })
    ]
    search_fields = ('name',)
    actions = [Exportar_Productos_a_PDF]
    # exclude = ['cfg', ]


# model admins
class ConfiguracionAdmin(admin.ModelAdmin):
    inlines = [ApkAccessInLine, ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


# Register your models here.
admin.site.register(Configuration, ConfiguracionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ConfiguracionGodjango)
