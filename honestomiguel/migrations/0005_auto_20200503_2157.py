# Generated by Django 3.0.5 on 2020-05-04 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honestomiguel', '0004_hamburguesa_ingredientes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hamburguesa',
            name='imagen',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]