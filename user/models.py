from django.contrib.auth.models import AbstractUser
from django.db import models


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
        super(User, self).save()

    class Meta:
        permissions = [
            ('add_product', 'can add product'),
            ('can_change_product', 'can change product'),
            ('can_delete_product', 'can delete product'),
            ('can_view_product', 'can view product'),
        ]
