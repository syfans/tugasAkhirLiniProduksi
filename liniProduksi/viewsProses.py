from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Proses, Operator, KebutuhanMaterial, PeralatanProduksi, PengirimanMaterial
from .forms import ProsesForm


def newProses(request):
    proses_form = ProsesForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        # validasi data
        if proses_form.is_valid():
            # menyimpan ke database
            proses_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Proses',
        'proses_form': proses_form,
    }
    return render(request, 'liniProduksi/newProses.html', context)

def deleteProses(request, delete_id):
    #cara delete
    Proses.objects.filter(id=delete_id).delete()
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updateProses(request, update_id):
    #cara edit Produk
    proses_update = Proses.objects.get(id=update_id)

    data = {
        'stasiunKerja': proses_update.stasiunKerja,
        'idProses': proses_update.idProses,
        'namaProses':proses_update.namaProses,
        'durasiProses':proses_update.durasiProses,
    }

    proses_form = ProsesForm(request.POST or None, initial=data, instance=proses_update)

    if request.method == 'POST':
        #validasi data
        if proses_form.is_valid():
            p = proses_form.save()
            operator = Operator.objects.all()
            for o in operator:
                if o.proses_id == p.idProses:
                    Operator.objects.filter(id = o.id).update(stasiunKerja_id = p.stasiunKerja_id)
            km = KebutuhanMaterial.objects.all()
            for km in km:
                if km.proses_id == p.idProses:
                    KebutuhanMaterial.objects.filter(id=km.id).update(stasiunKerja_id=p.stasiunKerja_id)
                    k = KebutuhanMaterial.objects.get(id=km.id)
                    PengirimanMaterial.objects.filter(kebutuhanMaterial_id=k.id).update(stasiunKerja_id=k.stasiunKerja_id)
            per = PeralatanProduksi.objects.all()
            for per in per:
                if per.proses_id == p.idProses:
                    PeralatanProduksi.objects.filter(id=per.id).update(stasiunKerja_id=p.stasiunKerja_id)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Proses',
        'proses_form': proses_form,
    }

    return render(request,'liniProduksi/newProses.html',context)