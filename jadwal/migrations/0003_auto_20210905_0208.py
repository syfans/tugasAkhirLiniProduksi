# Generated by Django 2.1.5 on 2021-09-04 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jadwal', '0002_auto_20210811_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jadwalliniproduksi',
            name='liniProduksi',
        ),
        migrations.RemoveField(
            model_name='jadwalliniproduksi',
            name='stasiunKerja',
        ),
    ]
