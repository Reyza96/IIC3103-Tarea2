# Generated by Django 3.0.5 on 2020-05-04 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honestomiguel', '0003_auto_20200503_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='hamburguesa',
            name='ingredientes',
            field=models.ManyToManyField(blank=True, default='', to='honestomiguel.Ingrediente'),
        ),
    ]
