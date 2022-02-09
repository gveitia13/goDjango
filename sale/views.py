import glob
import os
from datetime import datetime

import django_excel as excel
from django.db import transaction
from django.shortcuts import render, redirect
import json

from goDjango.settings import BASE_DIR
from sale.models import Sale


# Create your views here.
def actualizar_ventas(request):
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
    return redirect('/admin/sale/sale')


def exportar_ventas(request):
    if request.method == 'POST':
        if '_excel' in request.POST:
            ventas = Sale.objects.filter(date_creation__range=[request.POST['inicial'], request.POST['final']])
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
                                       file_name=f'Ventas ({request.POST["inicial"]} - {request.POST["final"]}.xlsx')
        if '_filter' in request.POST:
            initial = datetime.strptime(request.POST['inicial'], '%Y-%m-%d').date()
            end = datetime.strptime(request.POST['final'], '%Y-%m-%d').date()
            return redirect(
                f'/admin/sale/sale/?date_creation__range__gte={initial.day}%2F{initial.month}%2F{initial.year}'
                f'&date_creation__range__lte={end.day}%2F{end.month}%2F{end.year}')

    return redirect('/admin/sale/sale')


def refrescar_pagina(request):
    return redirect('/admin/sale/sale')
