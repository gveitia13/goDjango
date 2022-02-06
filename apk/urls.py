from django.urls import path

from apk.admin import ProductAdmin

app_name = 'apk'
urlpatterns = [
    path('export/products.pdf', ProductAdmin.Exportar_Productos_a_PDF, name='export-pdf'),
]
