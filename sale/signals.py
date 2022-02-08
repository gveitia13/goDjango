import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from apk.models import hash_string
from sale.models import Sale

# @receiver(post_save, sender=Sale)
# def save_hash(sender, instance, created, **kwargs):
#     if created:
#         sale = instance
#         hash = hash_string(sale.name + str(sale.price) + str(sale.cost) + str(sale.date_creation) + sale.point_of_sale)
#         sale.hash = hash
#         sale.save()
