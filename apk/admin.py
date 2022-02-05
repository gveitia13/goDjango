import os
from io import StringIO

import qrcode
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from reportlab.pdfgen import canvas

from apk.forms import ApkAccessForm, ProductForm
from apk.models import ApkAccess, Product, Configuration, ConfiguracionGodjango
from goDjango.settings import MEDIA_ROOT


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


# def Exportar_Productos_a_PDF(modeladmin, request, queryset):
#     queryset = queryset
#     qrs = []
#     for q in queryset:
#         print(ApkAccess.objects.filter(cfg=q.cfg))
#         qr = qrcode.make()
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_H,
#             box_size=50,
#             border=4,
#         )
#         qr.add_data({
#             'Usuario': str(q.cfg.user),
#             'Nombre': q.name,
#             'Precio': q.price,
#             'Costo': q.cost,
#         })
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
#
#     print('---------------------')
#
#     # Generar PDF
#     context = {
#         'title': 'Invoice details',
#         'company': {'name': 'GoDjango'},
#         'products': queryset,
#         # 'qr': [q.qr for q in ApkAccess.objects.all()],
#         'qr': ApkAccess.objects.first().qr,
#         # 'list_url': reverse_lazy('startpage:cart_list')
#     }
#     html = render_to_string('product/pdf.html', context)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; pdf.pdf'
#
#     font_config = FontConfiguration()
#     HTML(string=html, base_url=request.build_absolute_uri()) \
#         .write_pdf(response, font_config=font_config)
#     return response


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cost',)
    fieldsets = [
        ('Datos del producto', {
            'fields': ('name', 'price', 'cost', 'cfg')
        })
    ]
    search_fields = ('name',)
    actions = ['Exportar_Productos_a_PDF', ]

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('admin/apk/product/prodcuts.pdf', self.Exportar_Productos_a_PDF),
    #     ]
    #     return custom_urls + urls

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

        c = canvas.Canvas('products.pdf')
        c.setFont('Helvetica', 12)
        x = 25
        yText = 800
        yImg = 675
        cont = 0
        cant = 0
        for r in queryset:
            c.drawString(x, yText, r.name)
            c.drawImage(os.path.join(MEDIA_ROOT + f'prodTemp/{r.pk}.png'), x, yImg, 100, 100)
            x += 110
            cont += 1
            if cont == 5:
                x = 25
                yText -= 150
                yImg -= 150
                cont = 0
            cant += 1
            if cant == 25:
                c.showPage()
                cant = 0
                x = 25
                yText = 800
                yImg = 675

        c.save()
        for f in queryset:
            if os.path.exists(MEDIA_ROOT + f'prodTemp/{f.pk}.png'):
                os.remove(MEDIA_ROOT + f'prodTemp/{f.pk}.png')


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
