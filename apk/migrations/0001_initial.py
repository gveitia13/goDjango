# Generated by Django 3.2 on 2022-02-01 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionGodjango',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns', models.CharField(max_length=500)),
                ('puerto', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Configuración de ámbito global',
                'verbose_name_plural': '*  Configuraciones de ámbito global',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': '01 - Configuraciones',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('price', models.FloatField(default=0.0, verbose_name='Precio')),
                ('cost', models.FloatField(default=0.0, verbose_name='Costo')),
                ('cfg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apk.configuration')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': '03 - Productos',
            },
        ),
    ]
