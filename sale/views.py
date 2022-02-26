import glob
import os
from datetime import datetime, timedelta

import django_excel as excel
from django.db import transaction
from django.shortcuts import render, redirect
import json

from django.urls import reverse

from goDjango.settings import BASE_DIR
from sale.models import Sale


# Create your views here.
def actualizar_ventas(request):
    user = request.user
    if os.path.exists(os.path.join(BASE_DIR / f'business/{user.name_hash}/import/')):
        directory = os.path.join(BASE_DIR / f'business/{user.name_hash}/import/')
        for filename in glob.iglob(os.path.join(directory, '*.json'), recursive=True):
            with open(filename) as js:
                # with transaction.atomic():
                asd = json.load(js)
                asd = asd if type(asd) == list else [asd]
                for dic in asd:
                    # for v in dic.values():
                    # if type(v) == dict:
                    #     if v.get('name') is not None:

                    try:
                        sale = Sale()
                        sale.name = dic['name']
                        sale.price = dic['price']
                        sale.cost = dic['cost']
                        sale.point_of_sale = dic['point_of_sale']
                        sale.hash = dic['hash']
                        sale.save()
                        timestamp = datetime.fromtimestamp(int(dic['date_creation']) / 1000)
                        sale.date_creation = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        sale.save()
                    except Exception as e:
                        print(e)
                js.close()
                os.remove(filename)
    return redirect('/admin/sale/sale')


def abdel(request, fecha_inicial, fecha_final):
    print(request.method)
    initial = fecha_inicial
    end = fecha_final


def exportar_ventas(request):
    if '_excel' in request.POST:
        ventas = Sale.objects.filter(date_creation__range=[request.POST['inicial'], request.POST['final']],
                                     user=request.user)
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
                                   file_name=f'Ventas ({request.POST["inicial"]} - {request.POST["final"]}).xlsx')

    # Filtro de fecha
    if '_filter' in request.POST:
        inicial = request.POST['inicial']
        final = request.POST['final']
        print(inicial)
        asd = datetime.strptime(inicial, '%Y-%m-%d')
        print(asd)
        asd = asd - timedelta(days=1)
        asd = asd.strftime('%Y-%m-%d')
        print(asd)
        ventas = Sale.objects.filter(date_creation__range=[asd, final], user=request.user)
        # ventas = Sale.objects.filter(date_creation)
        return render(request, 'admin/lista.html', {
            'ventas': ventas,
            'inicial': inicial,
            'final': final,
        })
    return redirect('/admin/sale/sale')


def refrescar_pagina(request):
    return redirect('/admin/sale/sale')
