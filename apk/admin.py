import os

import qrcode
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas

from apk.forms import ApkAccessForm, ProductForm
from apk.models import ApkAccess, Product, Configuration, ConfiguracionGodjango
from goDjango.settings import MEDIA_ROOT


# inlines
class ApkAccessInLine(admin.StackedInline):
    fieldsets = [
        ('Datos', {
            'fields': ('operator', 'point_of_sale', ('qr_tag', 'show_url'), 'state')
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


# model admins
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cost',)
    fieldsets = [
        ('Datos del producto', {
            'fields': ('name', 'price', 'cost',)
        })
    ]
    search_fields = ('name',)
    actions = ['Exportar_Productos_a_PDF', ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        cfgs = Configuration.objects.filter(user_id=request.user.pk)
        prods = Product.objects.filter(cfg__in=cfgs)
        return prods

    def Exportar_Productos_a_PDF(self, request, queryset):
        for q in queryset:
            qr = qrcode.make()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=50,
                border=4,
            )
            qr.add_data({
                'Nombre': q.name,
                'Precio': q.price,
                'Costo': q.cost,
            })
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            img.save("media/prodTemp/" + str(q.pk) + '.png')

        PDF_ROOT = MEDIA_ROOT + 'pdf/'
        c = canvas.Canvas(PDF_ROOT + 'products.pdf')
        c.setFont('Helvetica', 12)
        xImg = 25
        xText = 35
        yText = 800
        yImg = 675
        cont = 0
        cant = 0
        for r in queryset:
            c.drawString(xText, yText, (r.name[:14] + '..') if len(r.name) > 14 else r.name)
            c.drawImage(os.path.join(MEDIA_ROOT + f'prodTemp/{r.pk}.png'), xImg, yImg, 100, 100)
            xImg += 110
            xText += 110
            cont += 1
            if cont == 5:
                xImg = 25
                xText = 35
                yText -= 150
                yImg -= 150
                cont = 0
            cant += 1
            if cant == 25:
                c.showPage()
                cant = 0
                xImg = 25
                xText = 35
                yText = 800
                yImg = 675

        c.save()
        for f in queryset:
            if os.path.exists(MEDIA_ROOT + f'prodTemp/{f.pk}.png'):
                os.remove(MEDIA_ROOT + f'prodTemp/{f.pk}.png')
        return HttpResponseRedirect('/media/pdf/products.pdf')


class ApkAccessAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Datos', {
            'fields': ('operator', 'point_of_sale', ('qr_tag', 'show_url'), 'state')
        }),
    ]
    readonly_fields = ('qr_tag', 'show_url')
    list_display = ('point_of_sale', 'operator', 'state',)

    # form = ApkAccessForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        cfgs = Configuration.objects.filter(user_id=request.user.pk)
        return qs.filter(cfg__in=cfgs)


class ConfiguracionAdmin(admin.ModelAdmin):
    inlines = [ApkAccessInLine, ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


# Register your models here.
admin.site.register(ApkAccess, ApkAccessAdmin)
admin.site.register(Configuration, ConfiguracionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ConfiguracionGodjango)
