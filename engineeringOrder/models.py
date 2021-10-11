from django.db import models
from produk.models import Material

# Create your models here.
class EngineeringOrder(models.Model):
    material = models.OneToOneField('produk.Material', on_delete=models.CASCADE, related_name='eo')
    idEO = models.CharField(max_length=255, unique=True)
    namaPengusul = models.CharField(max_length=255,)
    departemenPengusul = models.CharField(max_length=255,)
    keterangan = models.TextField()
    tanggalPengajuan = models.DateField()

    is_disetujui = models.BooleanField(null=True, blank=True)
    tanggalPersetujuan = models.DateField(null=True, blank=True)
    tanggalPerubahanBerlaku = models.DateField(null=True, blank=True)

    is_prosesBaru = models.BooleanField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(EngineeringOrder, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idEO)