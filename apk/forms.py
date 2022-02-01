from .models import *
from django.forms import *


class ApkAccessForm(ModelForm):
    class Meta:
        model = ApkAccess
        fields = [
            'operator',
            'point_of_sale',
        ]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['cfg', ]
