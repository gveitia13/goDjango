from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


def Index(request):
    return HttpResponse('<h1><a href=/admin site style="text-decoration: none">GoDjango go to admin site</a></h1> ')
