from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


def Index(request):
    # return HttpResponse('<h1><a href=/admin site style="text-decoration: none">by GoDjango</a></h1> ')
    return redirect('/admin')
