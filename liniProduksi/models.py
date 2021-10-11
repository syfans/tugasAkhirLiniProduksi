from django.db import models
from django.contrib.auth.models import User
from produk.models import Material, Varian
import datetime


# Create your models here.
class LiniProduksi(models.Model):
    idLiniProduksi = models.CharField(max_length=255, unique=True)
    waktuSiklus = models.IntegerField()
    jumlahStasiunKerja = models.IntegerField()

    def save(self, *args, **kwargs):
        super(LiniProduksi, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idLiniProduksi)


class ProduksiHarian(models.Model):
    liniProduksi = models.ForeignKey('LiniProduksi', to_field='idLiniProduksi', on_delete=models.CASCADE)
    tanggalProduksi = models.DateField(unique=True)
    waktuMulaiProduksiAktual = models.TimeField(null=True, blank=True)
    waktuSelesaiProduksiAktual = models.TimeField(null=True, blank=True)
    waktuMulaiProduksi = models.TimeField(null=True, blank=True)
    waktuSelesaiProduksi = models.TimeField(null=True, blank=True)
    downtime = models.IntegerField(default=0)
    lembur_CHOICES = [
        ('Lembur', 'Lembur'),
        ('Tidak lembur', 'Tidak lembur'),
    ]
    is_lembur = models.CharField(null=True, blank=True, max_length=200, choices=lembur_CHOICES)
    libur_CHOICES = [
        ('Libur', 'Libur'),
        ('Tidak libur', 'Tidak libur'),
    ]
    is_libur = models.CharField(default="Tidak libur", max_length=200, choices=libur_CHOICES)
    alasanLibur = models.TextField(default="Tidak libur")
    kondisi_CHOICES = [
        ('Normal', 'Normal'),
        ('Customize', 'Customize'),
    ]
    kondisiIstirahat = models.CharField(default="Normal",max_length=200, choices=kondisi_CHOICES)

    def save(self, *args, **kwargs):
        self.waktuMulaiProduksiAktual = self.waktuMulaiProduksi
        # self.waktuSelesaiProduksiAktual = self.get_waktuSelesaiAktual
        self.waktuSelesaiProduksiAktual = self.waktuMulaiProduksi
        super(ProduksiHarian, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class WaktuIstirahat(models.Model):
    produksiHarian = models.ForeignKey('ProduksiHarian', on_delete=models.CASCADE, null=True, blank=True)
    waktuMulaiIstirahat = models.TimeField()
    waktuSelesaiIstirahat = models.TimeField()
    kondisi = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(WaktuIstirahat, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class TargetHarian(models.Model):
    varian = models.ForeignKey('produk.Varian', on_delete=models.CASCADE, to_field='idVarian')
    produksiHarian = models.ForeignKey('ProduksiHarian', on_delete=models.CASCADE, null=True)
    target = models.IntegerField()
    capaian = models.IntegerField(default=0)
    tanggal = models.DateField(null=True)
    waktuMulaiProduksi = models.TimeField()
    waktuSelesaiProduksi = models.TimeField()
    waktuMulaiProduksiAktual = models.TimeField(null=True, blank=True)
    waktuSelesaiProduksiAktual = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.waktuMulaiProduksiAktual = self.waktuMulaiProduksi
        self.waktuSelesaiProduksiAktual = self.waktuMulaiProduksi
        super(TargetHarian, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class TargetMingguan(models.Model):
    varian = models.ForeignKey('produk.Varian', on_delete=models.CASCADE, to_field='idVarian')
    liniProduksi = models.ForeignKey('LiniProduksi', to_field='idLiniProduksi', on_delete=models.CASCADE)
    target = models.IntegerField()
    minggu = models.IntegerField(null=True)
    tahun = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(TargetMingguan, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class TargetBulanan(models.Model):
    varian = models.ForeignKey('produk.Varian', on_delete=models.CASCADE, to_field='idVarian')
    liniProduksi = models.ForeignKey('LiniProduksi', to_field='idLiniProduksi', on_delete=models.CASCADE)
    target = models.IntegerField()
    bulan = models.IntegerField(null=True)
    tahun = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(TargetBulanan, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class TargetTahunan(models.Model):
    varian = models.ForeignKey('produk.Varian', on_delete=models.CASCADE, to_field='idVarian')
    liniProduksi = models.ForeignKey('LiniProduksi', to_field='idLiniProduksi', on_delete=models.CASCADE)
    target = models.IntegerField()
    tahun = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(TargetTahunan, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class StasiunKerja(models.Model):
    liniProduksi = models.ForeignKey('LiniProduksi', to_field='idLiniProduksi', on_delete=models.CASCADE)
    idStasiunKerja = models.CharField(max_length=255, unique=True)
    nomorStasiunKerja = models.IntegerField()
    list_sisi = (
        ('Kanan', 'Kanan'),
        ('Kiri', 'Kiri'),
    )
    sisiStasiunKerja = models.CharField(
        max_length=255,
        choices=list_sisi,
    )

    def save(self, *args, **kwargs):
        super(StasiunKerja, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idStasiunKerja)


class Proses(models.Model):
    stasiunKerja = models.ForeignKey('StasiunKerja', to_field='idStasiunKerja', on_delete=models.CASCADE)
    idProses = models.CharField(max_length=255, unique=True)
    namaProses = models.CharField(max_length=255)
    durasiProses = models.IntegerField()
    is_berlaku = models.BooleanField(default=True)
    tanggalMulaiBerlaku = models.DateField(null=True, blank=True)
    tanggalSelesaiBerlaku = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Proses, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idProses)


class KebutuhanMaterial(models.Model):
    stasiunKerja = models.ForeignKey('StasiunKerja', to_field='idStasiunKerja', on_delete=models.CASCADE)
    proses = models.ForeignKey('Proses', to_field='idProses', on_delete=models.CASCADE)
    material = models.OneToOneField('produk.Material', on_delete=models.CASCADE, related_name='kebutuhanMaterial')
    jumlahMaterialPerCycleTime = models.IntegerField(default=0)
    jumlahMaterialKumulatif = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(KebutuhanMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class PeralatanProduksi(models.Model):
    stasiunKerja = models.ForeignKey('StasiunKerja', to_field='idStasiunKerja', on_delete=models.CASCADE)
    proses = models.ForeignKey('Proses', to_field='idProses', on_delete=models.CASCADE)
    idPeralatan = models.CharField(max_length=255, unique=True)
    jenisPeralatan = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super(PeralatanProduksi, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class Operator(models.Model):
    proses = models.ForeignKey('Proses', to_field='idProses', on_delete=models.CASCADE)
    stasiunKerja = models.ForeignKey(StasiunKerja, to_field='idStasiunKerja', on_delete=models.CASCADE)
    namaLengkap = models.CharField(max_length=255)
    levelOperator = models.CharField(max_length=255,)

    def save(self, *args, **kwargs):
        super(Operator, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)

class PengirimanMaterial(models.Model):
    kebutuhanMaterial = models.ForeignKey('KebutuhanMaterial', on_delete=models.CASCADE,related_name='pengirimanMaterial')
    stasiunKerja = models.ForeignKey(StasiunKerja, to_field='idStasiunKerja', on_delete=models.CASCADE)
    jumlahMaterialTiapPengiriman = models.IntegerField()

    def save(self, *args, **kwargs):
        super(PengirimanMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.kebutuhanMaterial)


class Gangguan(models.Model):
    stasiunKerja = models.ForeignKey('StasiunKerja', to_field='idStasiunKerja', on_delete=models.CASCADE)
    idGangguan = models.CharField(max_length=255, unique=True, null=True, blank=True)
    waktuMulaiGangguan = models.TimeField(null=True, blank=True)
    waktuSelesaiGangguan = models.TimeField(null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    durasiGangguan = models.IntegerField(null=True, blank=True)
    tanggalGangguan = models.DateField(null=True, blank=True)
    waktuMulaiLiniProduksiTerhenti = models.TimeField(null=True, blank=True)
    waktuSelesaiLiniProduksiTerhenti = models.TimeField(null=True, blank=True)
    durasiLiniProduksiTerhenti = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Gangguan, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.idGangguan)