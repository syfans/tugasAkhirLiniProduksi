# Generated by Django 2.1.5 on 2021-08-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineeringOrder', '0006_auto_20210804_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engineeringorder',
            name='is_disetujui',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
