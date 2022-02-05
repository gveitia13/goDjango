import random

from django.test import TestCase
# Create your tests here.
# def index(request):
#     context = {}
#     if request.method == "POST":
#         factory = qrcode.image.svg.SvgImage
#         img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
#         stream = BytesIO()
#         img.save(stream)
#         context["svg"] = stream.getvalue().decode()
#
#     return render(request, "index.html", context=context)
import string
import random

number_of_strings = 5
length_of_string = 8
from apk.models import Product

for x in Product.objects.all():
    x.name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    x.save()
