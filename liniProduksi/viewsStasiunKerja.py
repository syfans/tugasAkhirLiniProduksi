from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import LiniProduksi, StasiunKerja
from .forms import LiniProduksiForm, StasiunKerjaForm


def stasiunKerja(request, idLiniProduksiInput):
    liniProduksi = LiniProduksi.objects.filter(idLiniProduksi=idLiniProduksiInput)
    stasiun_kerja = StasiunKerja.objects.filter(liniProduksi__idLiniProduksi=idLiniProduksiInput)

    context = {
        'Judul': 'Stasiun Kerja',
        'semua_stasiunKerja': stasiun_kerja,
        'liniProduksi': liniProduksi,
        'css': 'liniProduksi/css/styles_table.css',
    }
    return render(request, 'liniProduksi/stasiunKerja.html', context)

def newStasiunKerja(request):
    stasiunkerja_form = StasiunKerjaForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        # validasi data
        if stasiunkerja_form.is_valid():
            # menyimpan ke database
            stasiunkerja_form.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Stasiun Kerja',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request, 'liniProduksi/newStasiunKerja.html', context)

def deleteStasiunKerja(request, delete_id):
    #cara delete
    StasiunKerja.objects.filter(id=delete_id).delete()
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updateStasiunKerja(request, update_id):
    #cara edit Produk
    stasiunkerja_update = StasiunKerja.objects.get(id=update_id)

    data = {
        'liniProduksi': stasiunkerja_update.liniProduksi,
        'nomorStasiunKerja': stasiunkerja_update.nomorStasiunKerja,
        'sisiStasiunKerja': stasiunkerja_update.sisiStasiunKerja,
    }

    stasiunkerja_form = StasiunKerjaForm(request.POST or None, initial=data, instance=stasiunkerja_update)

    if request.method == 'POST':
        #validasi data
        if stasiunkerja_form.is_valid():
            #menyimpan ke database
            stasiunkerja_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Stasiun Kerja',
        'stasiunkerja_form': stasiunkerja_form,
    }

    return render(request,'liniProduksi/newStasiunKerja.html',context)