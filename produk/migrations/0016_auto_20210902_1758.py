# Generated by Django 2.1.5 on 2021-09-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produk', '0015_auto_20210831_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='varian',
        ),
        migrations.AddField(
            model_name='material',
            name='varian',
            field=models.ManyToManyField(to='produk.Varian'),
        ),
    ]