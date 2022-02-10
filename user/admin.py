from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from user.models import User


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'name_hash')
    search_fields = ('username', 'email')
    fieldsets = [
        ('Datos del usuario', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        },),
        ('Estados del usuario', {
            'fields': ('is_staff', 'is_superuser', 'is_active',)
        },),
    ]


admin.site.register(User, MyUserAdmin)
# admin.site.register(Permission)
# admin.site.unregister(Group)
