# Generated by Django 2.1.5 on 2021-08-29 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liniProduksi', '0037_produksiharian_is_libur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produksiharian',
            name='is_libur',
        ),
        migrations.RemoveField(
            model_name='produksiharian',
            name='keterangan',
        ),
    ]