from django.urls import path

from apk.admin import ProductAdmin
from .views import *

app_name = 'sale'
urlpatterns = [
    path('resultados/', abdel, name='abdel'),
    path('sale/exportar/', exportar_ventas, name='exportar'),
    path('actualizar/', actualizar_ventas, name='actualizar'),
    path('sale/sale/', refrescar_pagina, name='refrescar'),
]
