# Generated by Django 2.0.4 on 2018-05-13 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pareja', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.BigIntegerField(default=0)),
                ('Enamorado1', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Enamorado1', to='Pareja.Enamorado')),
                ('Enamorado2', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Enamorado2', to='Pareja.Enamorado')),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('capacidad', models.IntegerField()),
                ('imagen', models.ImageField(blank=True, default=None, null=True, upload_to='Domain/Lugar')),
                ('tipo', models.CharField(choices=[('ceremonia', 'Ceremonia'), ('fiesta', 'Fiesta')], default=None, max_length=50)),
                ('precio', models.BigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Lugar',
                'verbose_name_plural': 'Lugares',
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('precio', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TransporteCarrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Boda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Domain.Boda')),
                ('Transporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Domain.Transporte')),
            ],
        ),
    ]
