# Generated by Django 2.1.5 on 2021-08-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liniProduksi', '0002_auto_20210809_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kebutuhanmaterial',
            name='jumlahMaterialPerCycleTime',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]