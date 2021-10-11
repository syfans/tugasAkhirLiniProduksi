from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import PeralatanProduksi, Proses, StasiunKerja
from .forms import PeralatanProduksiForm


def newPeralatanProduksi(request):
    peralatanProduksi_form = PeralatanProduksiForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        id = request.POST.get('id')
        proses = request.POST.get('proses')
        idPeralatan = request.POST.get('idPeralatan')
        jenisPeralatan = request.POST.get('jenisPeralatan')

        proses_sk = Proses.objects.get(idProses=proses)
        p_sk = str(proses_sk.stasiunKerja)
        stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)
        PeralatanProduksi.objects.create(id=id, stasiunKerja=stasiunKerja, proses=proses_sk, idPeralatan=idPeralatan, jenisPeralatan=jenisPeralatan)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Peralatan Produksi',
        'peralatanProduksi_form': peralatanProduksi_form,
    }
    return render(request, 'liniProduksi/newPeralatanProduksi.html', context)

def deletePeralatanProduksi(request, delete_id):
    #cara delete
    PeralatanProduksi.objects.filter(id=delete_id).delete()
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updatePeralatanProduksi(request, update_id):
    #cara edit Produk
    peralatanProduksi_update = PeralatanProduksi.objects.get(id=update_id)

    data = {
        'proses': peralatanProduksi_update.proses,
        'jenisPeralatan': peralatanProduksi_update.jenisPeralatan,
    }

    peralatanProduksi_form = PeralatanProduksiForm(request.POST or None, initial=data, instance=peralatanProduksi_update)

    if request.method == 'POST':
        #validasi data
        if peralatanProduksi_form.is_valid():
            peralatanProduksi_form.save()
            #menyimpan ke database
            peralatanProduksi_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Peralatan Produksi',
        'peralatanProduksi_form': peralatanProduksi_form,
    }

    return render(request,'liniProduksi/newPeralatanProduksi.html',context)