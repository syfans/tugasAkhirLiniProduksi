# Generated by Django 2.1.5 on 2021-09-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liniProduksi', '0046_auto_20210903_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetharian',
            name='capaian',
            field=models.IntegerField(default=0),
        ),
    ]
