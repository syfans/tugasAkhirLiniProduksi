# Generated by Django 2.1.5 on 2021-09-07 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jadwal', '0003_auto_20210905_0208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jadwalliniproduksi',
            name='jumlahMaterialTersedia',
        ),
    ]
