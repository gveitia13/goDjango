import os

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import *
import shutil


@receiver(post_save, sender=User)
def save_hash(sender, instance, created, **kwargs):
    if created:
        user = instance
        name_hash = hash_string(user.username + user.password + str(datetime.utcnow)) + '.sd'
        user.name_hash = name_hash
        user.save()
        os.mkdir(os.path.join(os.getcwd(), 'business/' + str(name_hash)))
        os.mkdir(os.path.join(os.getcwd(), 'business/' + str(name_hash) + '/apkids/'))
        os.mkdir(os.path.join(os.getcwd(), 'business/' + str(name_hash) + '/import/'))
        f = open(os.path.join(os.getcwd(), 'business/' + str(name_hash) + '/apkids/acl'), "w")


@receiver(pre_delete, sender=User)
def delete_hash(sender, instance, using, **kwargs):
    if True:
        user = instance
        shutil.rmtree(os.path.join(os.getcwd(), 'business/' + str(user.name_hash)))


@receiver(post_save, sender=ApkAccess)
def save_apk_access(sender, instance, created, **kwargs):
    habilitados = ApkAccess.objects.all().filter(cfg=instance.cfg, state=True)
    f = open(os.path.join(os.getcwd(), 'business/' + str(instance.cfg.user.name_hash) + '/apkids/acl'), "w")
    for item in habilitados:
        f.write(item.apkidhash)
        f.write('\n')


@receiver(post_delete, sender=ApkAccess)
def delete_apk_access(sender, instance,using, **kwargs):
    habilitados = ApkAccess.objects.all().filter(cfg=instance.cfg, state=True)
    f = open(os.path.join(os.getcwd(), 'business/' + str(instance.cfg.user.name_hash) + '/apkids/acl'), "w")
    for item in habilitados:
        f.write(item.apkidhash)
        f.write('\n')
