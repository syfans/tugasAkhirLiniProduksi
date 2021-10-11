from django.shortcuts import render, redirect

from .models import StasiunKerja, Proses, PeralatanProduksi, KebutuhanMaterial, Operator, PengirimanMaterial
from django.contrib.auth.models import User
from django.db.models import Count, Q
import datetime


def stasiunKerjaDetail(request, idLiniProduksiInput, idStasiunKerjaInput):
    stasiunkerja = StasiunKerja.objects.filter(idStasiunKerja=idStasiunKerjaInput)

    liniProduksi = StasiunKerja.objects.filter(liniProduksi_id=idLiniProduksiInput)
    list_liniProduksi = list(liniProduksi)

    proses = Proses.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput).filter((Q(tanggalSelesaiBerlaku__gt=datetime.datetime.today()) & Q(tanggalMulaiBerlaku__lte=datetime.datetime.today()))|(Q(tanggalSelesaiBerlaku__isnull=True) & Q(tanggalMulaiBerlaku__lte=datetime.datetime.today())))
    peralatanProduksi = PeralatanProduksi.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput, proses__is_berlaku=True)
    operator = Operator.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput, proses__is_berlaku=True)

    material = KebutuhanMaterial.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput).filter((Q(material__tanggalGanti__gt=datetime.datetime.today()) & Q(material__tanggalMulaiBerlaku__lte=datetime.datetime.today()))|(Q(material__tanggalGanti__isnull=True) & Q(material__tanggalMulaiBerlaku__lte=datetime.datetime.today())))
    km = material.values('material__idMaterial','proses','jumlahMaterialKumulatif', 'material__varian').annotate(jumlahKumulatif=Count('proses')).order_by('material__varian','material__idMaterial')
    pengirimanMaterial = PengirimanMaterial.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput, kebutuhanMaterial__material__is_berlaku=True)


    context = {
        'Judul': 'Detail Stasiun Kerja',
        'liniProduksi': list_liniProduksi,
        'stasiunKerja': stasiunkerja,
        'proses': proses,
        'peralatanProduksi': peralatanProduksi,
        'material': material,
        'km': km,
        'operator': operator,
        'pengirimanMaterial':pengirimanMaterial,
    }

    return render(request, 'liniProduksi/stasiunKerjaDetail.html', context)