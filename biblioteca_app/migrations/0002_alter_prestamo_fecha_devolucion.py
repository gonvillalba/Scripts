# Generated by Django 5.0.2 on 2024-02-09 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_devolucion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
