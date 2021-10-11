from django.db import models
from django.utils.text import slugify
from liniProduksi.models import LiniProduksi, StasiunKerja, KebutuhanMaterial
import datetime
import time
from django.utils import timezone
# Create your models here.

class JadwalLiniProduksi (models.Model):
    kebutuhanMaterial = models.ForeignKey('liniProduksi.KebutuhanMaterial', on_delete=models.CASCADE, related_name='jadwal')

    tanggal = models.DateField()
    jadwalKedatangan = models.TimeField()
    jumlah_material = models.IntegerField()

    is_konfirmasi = models.BooleanField(default=False)
    jadwalKedatangan_aktual = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.id)