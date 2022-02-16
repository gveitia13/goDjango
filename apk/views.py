from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


def Index(request):
    return redirect('/admin')
