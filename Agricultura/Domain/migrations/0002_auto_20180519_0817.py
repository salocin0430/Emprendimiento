# Generated by Django 2.0.4 on 2018-05-19 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Domain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugar',
            name='direccion',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
    ]
