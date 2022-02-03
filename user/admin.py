from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from user.models import User


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'name_hash')
    search_fields = ('username', 'email')


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
