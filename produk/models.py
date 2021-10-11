from django.db import models

class Brand(models.Model):
    idBrand = models.CharField(max_length=255,)
    namaBrand = models.CharField(max_length=255,)


class Model(Brand):
    idModel = models.CharField(max_length=255,)
    namaModel = models.CharField(max_length=255)


class Varian(Model):
    idVarian = models.CharField(max_length=255, unique=True)
    namaVarian = models.CharField(max_length=255,)
    namaAtribut = models.CharField(max_length=255,)
    nilaiAtribut = models.CharField(max_length=255,)

    def save(self, *args, **kwargs):
        super(Varian, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idVarian)


class Material(models.Model):
    varian = models.ForeignKey('Varian', on_delete=models.CASCADE, to_field='idVarian')
    idMaterial = models.CharField(max_length=255,)
    namaMaterial = models.CharField(max_length=255,)
    namaSupplier = models.CharField(max_length=255, null=True, blank=True)
    penyusunProduk = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='penyusunProduk_material_set')

    is_berlaku = models.BooleanField(default=True, null=True, blank=True)
    tanggalMulaiBerlaku = models.DateField(null=True, blank=True)
    tanggalGanti = models.DateField(null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    penggantiMaterial = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='penggantiMaterial_material_set')

    def save(self, *args, **kwargs):
        super(Material, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idMaterial)