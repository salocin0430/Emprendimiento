# Generated by Django 2.0.4 on 2018-05-19 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LunaMiel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='descripcion',
            field=models.TextField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='plan',
            name='descripcion',
            field=models.TextField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
    ]
