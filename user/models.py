from crum import get_current_request
from django.contrib.auth.models import AbstractUser, Group
from django.db import models, transaction


# Create your models here.
class User(AbstractUser):
    name_hash = models.CharField(max_length=900, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print(self)
        passw = self.password
        if self.pk is None:
            self.set_password(passw)
        else:
            user = User.objects.get(pk=self.pk)
            if user.password != passw:
                self.set_password(passw)
        transaction.on_commit(lambda: self.groups.add(Group.objects.first()))
        super(User, self).save()
